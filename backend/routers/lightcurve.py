"""
Lightcurve router for ExoScout Backend.

Handles downloading and caching light-curve data from TESS (via TESSCut),
Kepler, and K2 missions (via astroquery).
"""

import os
import logging
from typing import Dict, List, Any, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.concurrency import run_in_threadpool
import httpx
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np

from utils.cache import cached, get_cached, set_cached
from services.nasa_api import get_coordinates_from_archive

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lightcurve", tags=["lightcurve"])

# Configuration
TESSCUT_BASE_URL = "https://mast.stsci.edu/tesscut/api/v0.1"
CACHE_TTL = 3600  # 1 hour


class LightcurveError(Exception):
    """Raised when lightcurve operations fail."""
    pass


async def download_tess_lightcurve(tic_id: int, ra: float, dec: float, sector: Optional[int] = None) -> Dict[str, Any]:
    """
    Download TESS lightcurve data using TESSCut API.
    
    Args:
        tic_id (int): TIC ID
        ra (float): Right ascension in degrees
        dec (float): Declination in degrees
        sector (Optional[int]): Specific sector to download
        
    Returns:
        Dict[str, Any]: Lightcurve data
        
    Raises:
        LightcurveError: If download fails
    """
    try:
        # Create coordinate string
        coord_str = f"{ra},{dec}"
        
        # TESSCut astrocut endpoint
        url = f"{TESSCUT_BASE_URL}/astrocut"
        
        params = {
            "ra": ra,
            "dec": dec,
            "y": 5,  # Cutout size in pixels
            "x": 5,
            "units": "px",  # pixels (21 arcseconds/pixel)
            "format": "fits"
        }
        
        if sector:
            params["sector"] = sector
        
        logger.info(f"Downloading TESS lightcurve for TIC {tic_id} at {coord_str}")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            if response.headers.get("content-type", "").startswith("application/json"):
                # Error response
                error_data = response.json()
                raise LightcurveError(f"TESSCut API error: {error_data}")
            
            # Save FITS data temporarily and process
            fits_data = response.content
            
            # Process FITS data in thread pool
            lightcurve_data = await run_in_threadpool(_process_tess_fits, fits_data, tic_id)
            
            return lightcurve_data
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error downloading TESS lightcurve for TIC {tic_id}: {e}")
        raise LightcurveError(f"Failed to download TESS lightcurve: {e}")
    except Exception as e:
        logger.error(f"Error downloading TESS lightcurve for TIC {tic_id}: {e}")
        raise LightcurveError(f"Failed to process TESS lightcurve: {e}")


def _process_tess_fits(fits_data: bytes, tic_id: int) -> Dict[str, Any]:
    """
    Process TESS FITS data to extract lightcurve.
    
    Args:
        fits_data (bytes): FITS file data
        tic_id (int): TIC ID
        
    Returns:
        Dict[str, Any]: Processed lightcurve data
    """
    try:
        # Parse FITS data
        from io import BytesIO
        fits_file = BytesIO(fits_data)
        
        with fits.open(fits_file) as hdul:
            # Get lightcurve data from first extension
            if len(hdul) < 2:
                raise LightcurveError("Invalid FITS file structure")
            
            data = hdul[1].data
            header = hdul[1].header
            
            # Extract time and flux
            time = data['TIME']
            flux = data['FLUX']
            
            # Remove NaN values
            valid_mask = ~(np.isnan(time) | np.isnan(flux))
            time = time[valid_mask]
            flux = flux[valid_mask]
            
            if len(time) == 0:
                raise LightcurveError("No valid data points found")
            
            # Calculate basic statistics
            flux_mean = np.mean(flux)
            flux_std = np.std(flux)
            flux_median = np.median(flux)
            
            # Normalize flux
            flux_normalized = (flux - flux_median) / flux_median
            
            logger.info(f"Processed TESS lightcurve for TIC {tic_id}: {len(time)} points")
            
            return {
                "mission": "TESS",
                "target_id": tic_id,
                "data_points": len(time),
                "time_range": {
                    "start": float(np.min(time)),
                    "end": float(np.max(time)),
                    "duration": float(np.max(time) - np.min(time))
                },
                "flux_stats": {
                    "mean": float(flux_mean),
                    "median": float(flux_median),
                    "std": float(flux_std),
                    "min": float(np.min(flux)),
                    "max": float(np.max(flux))
                },
                "time_series": {
                    "time": time[:1000].tolist(),  # Limit to first 1000 points for API response
                    "flux": flux[:1000].tolist(),
                    "flux_normalized": flux_normalized[:1000].tolist()
                },
                "sector": header.get('SECTOR', 'unknown'),
                "camera": header.get('CAMERA', 'unknown'),
                "ccd": header.get('CCD', 'unknown')
            }
            
    except Exception as e:
        logger.error(f"Error processing TESS FITS data for TIC {tic_id}: {e}")
        raise LightcurveError(f"Failed to process FITS data: {e}")


async def download_kepler_lightcurve(kep_id: int, mission: str = "Kepler") -> Dict[str, Any]:
    """
    Download Kepler/K2 lightcurve data using astroquery.
    
    Args:
        kep_id (int): Kepler ID or EPIC ID
        mission (str): Mission name (Kepler or K2)
        
    Returns:
        Dict[str, Any]: Lightcurve data
        
    Raises:
        LightcurveError: If download fails
    """
    try:
        # Use astroquery in thread pool (it's synchronous)
        lightcurve_data = await run_in_threadpool(_download_kepler_sync, kep_id, mission)
        return lightcurve_data
        
    except Exception as e:
        logger.error(f"Error downloading {mission} lightcurve for {kep_id}: {e}")
        raise LightcurveError(f"Failed to download {mission} lightcurve: {e}")


def _download_kepler_sync(kep_id: int, mission: str) -> Dict[str, Any]:
    """
    Synchronous Kepler/K2 lightcurve download using astroquery.
    
    Args:
        kep_id (int): Kepler ID or EPIC ID
        mission (str): Mission name
        
    Returns:
        Dict[str, Any]: Lightcurve data
    """
    try:
        from astroquery.mast import Observations
        
        # Search for observations
        if mission.upper() == "KEPLER":
            obs_table = Observations.query_criteria(
                target_name=f"kplr{kep_id:09d}",
                obs_collection="Kepler"
            )
        else:  # K2
            obs_table = Observations.query_criteria(
                target_name=f"ktwo{kep_id:09d}",
                obs_collection="K2"
            )
        
        if len(obs_table) == 0:
            raise LightcurveError(f"No {mission} observations found for {kep_id}")
        
        # Get data products for first observation
        obs_id = obs_table[0]['obsid']
        products = Observations.get_product_list(obs_id)
        
        # Filter for lightcurve files
        lc_products = products[products['productSubGroupDescription'] == 'LC']
        
        if len(lc_products) == 0:
            raise LightcurveError(f"No lightcurve products found for {mission} {kep_id}")
        
        # Download first lightcurve file
        download_result = Observations.download_products(
            lc_products[0:1],
            download_dir="./cache/lightcurves"
        )
        
        if len(download_result) == 0:
            raise LightcurveError(f"Failed to download {mission} lightcurve for {kep_id}")
        
        # Process downloaded FITS file
        fits_path = download_result['Local Path'][0]
        
        with fits.open(fits_path) as hdul:
            data = hdul[1].data
            header = hdul[1].header
            
            # Extract time and flux
            time = data['TIME']
            flux = data['PDCSAP_FLUX']  # Pre-search Data Conditioning flux
            
            # Remove NaN values
            valid_mask = ~(np.isnan(time) | np.isnan(flux))
            time = time[valid_mask]
            flux = flux[valid_mask]
            
            if len(time) == 0:
                raise LightcurveError("No valid data points found")
            
            # Calculate statistics
            flux_mean = np.mean(flux)
            flux_std = np.std(flux)
            flux_median = np.median(flux)
            
            # Normalize flux
            flux_normalized = (flux - flux_median) / flux_median
            
            logger.info(f"Processed {mission} lightcurve for {kep_id}: {len(time)} points")
            
            return {
                "mission": mission.upper(),
                "target_id": kep_id,
                "data_points": len(time),
                "time_range": {
                    "start": float(np.min(time)),
                    "end": float(np.max(time)),
                    "duration": float(np.max(time) - np.min(time))
                },
                "flux_stats": {
                    "mean": float(flux_mean),
                    "median": float(flux_median),
                    "std": float(flux_std),
                    "min": float(np.min(flux)),
                    "max": float(np.max(flux))
                },
                "time_series": {
                    "time": time[:1000].tolist(),  # Limit for API response
                    "flux": flux[:1000].tolist(),
                    "flux_normalized": flux_normalized[:1000].tolist()
                },
                "quarter": header.get('QUARTER', 'unknown'),
                "campaign": header.get('CAMPAIGN', 'unknown')
            }
            
    except Exception as e:
        logger.error(f"Error in sync {mission} download for {kep_id}: {e}")
        raise LightcurveError(f"Failed to download {mission} data: {e}")


@router.get("/{mission}/{target_id}")
@cached("lightcurve", ttl=CACHE_TTL)
async def get_lightcurve(mission: str, target_id: int) -> Dict[str, Any]:
    """
    Get lightcurve data for a target.
    
    Args:
        mission (str): Mission name (TESS, Kepler, K2)
        target_id (int): Target ID (TIC ID, Kepler ID, EPIC ID)
        
    Returns:
        Dict[str, Any]: Lightcurve data
        
    Raises:
        HTTPException: If lightcurve retrieval fails
    """
    try:
        mission = mission.upper()
        
        if mission not in ["TESS", "KEPLER", "K2"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported mission: {mission}. Supported: TESS, Kepler, K2"
            )
        
        logger.info(f"Getting lightcurve for {mission} {target_id}")
        
        if mission == "TESS":
            # Get coordinates for TESS target
            try:
                coords = await get_coordinates_from_archive(mission, target_id)
                ra = coords.get("ra")
                dec = coords.get("dec")
                
                if ra is None or dec is None:
                    raise LightcurveError("Could not retrieve coordinates for TESS target")
                
                lightcurve_data = await download_tess_lightcurve(target_id, ra, dec)
                
            except Exception as e:
                logger.error(f"Failed to get TESS lightcurve for {target_id}: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to retrieve TESS lightcurve: {str(e)}"
                )
        
        elif mission in ["KEPLER", "K2"]:
            try:
                lightcurve_data = await download_kepler_lightcurve(target_id, mission)
                
            except Exception as e:
                logger.error(f"Failed to get {mission} lightcurve for {target_id}: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to retrieve {mission} lightcurve: {str(e)}"
                )
        
        return lightcurve_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting lightcurve for {mission} {target_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/{mission}/{target_id}/sectors")
async def get_available_sectors(mission: str, target_id: int) -> Dict[str, Any]:
    """
    Get available sectors/quarters/campaigns for a target.
    
    Args:
        mission (str): Mission name
        target_id (int): Target ID
        
    Returns:
        Dict[str, Any]: Available data periods
    """
    try:
        mission = mission.upper()
        
        if mission == "TESS":
            # Query TESSCut for available sectors
            coords = await get_coordinates_from_archive(mission, target_id)
            ra = coords.get("ra")
            dec = coords.get("dec")
            
            if ra is None or dec is None:
                raise HTTPException(status_code=404, detail="Coordinates not found")
            
            url = f"{TESSCUT_BASE_URL}/sector"
            params = {"ra": ra, "dec": dec}
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                sectors_data = response.json()
                
                return {
                    "mission": mission,
                    "target_id": target_id,
                    "available_sectors": sectors_data.get("sectors", []),
                    "coordinates": {"ra": ra, "dec": dec}
                }
        
        else:
            # For Kepler/K2, return basic info
            return {
                "mission": mission,
                "target_id": target_id,
                "note": f"Use main lightcurve endpoint for {mission} data"
            }
            
    except Exception as e:
        logger.error(f"Error getting sectors for {mission} {target_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get available sectors: {str(e)}"
        )