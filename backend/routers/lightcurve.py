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
        
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
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
        fits_data (bytes): FITS file data (ZIP archive from TESSCut)
        tic_id (int): TIC ID
        
    Returns:
        Dict[str, Any]: Processed lightcurve data
    """
    try:
        import zipfile
        from io import BytesIO
        
        # TESSCut returns a ZIP file, extract the FITS file
        zip_file = BytesIO(fits_data)
        
        with zipfile.ZipFile(zip_file, 'r') as zf:
            # Find the FITS file in the ZIP
            fits_files = [f for f in zf.namelist() if f.endswith('.fits')]
            if not fits_files:
                raise LightcurveError("No FITS file found in ZIP archive")
            
            # Read the first FITS file
            fits_content = zf.read(fits_files[0])
            fits_file = BytesIO(fits_content)
        
        with fits.open(fits_file) as hdul:
            # Get lightcurve data from first extension
            if len(hdul) < 2:
                raise LightcurveError("Invalid FITS file structure")
            
            data = hdul[1].data
            header = hdul[1].header
            
            # Extract time and flux
            time = data['TIME']
            flux = data['FLUX']
            
            # For TESS cutout data, flux is a 3D array (time, y, x)
            # Sum the flux across the spatial dimensions to get the total flux
            if flux.ndim == 3:
                flux = np.sum(flux, axis=(1, 2))
            elif flux.ndim == 2:
                # If 2D, sum across the spatial dimension
                flux = np.sum(flux, axis=1)
            
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
    Synchronous download of Kepler/K2 lightcurve data with multiple fallback strategies.
    
    Args:
        kep_id (int): Kepler ID or EPIC ID
        mission (str): Mission name (KEPLER or K2)
        
    Returns:
        Dict[str, Any]: Lightcurve data
    """
    # Normalize mission to uppercase
    mission = mission.upper()
    
    logger.info(f"Starting sync download for {mission} {kep_id}")
    
    # Strategy 1: Try lightkurve first
    try:
        import lightkurve as lk
        logger.info(f"lightkurve version: {lk.__version__}")
        
        # Try multiple search patterns for lightkurve
        search_patterns = []
        if mission == "KEPLER":
            search_patterns = [
                f"KIC {kep_id}",
                f"kplr{kep_id:09d}",
                str(kep_id),
                f"Kepler-{kep_id}"
            ]
        else:  # K2
            search_patterns = [
                f"EPIC {kep_id}",
                f"ktwo{kep_id:09d}",
                str(kep_id),
                f"K2-{kep_id}"
            ]
        
        lc = None
        successful_pattern = None
        
        for pattern in search_patterns:
            try:
                logger.info(f"Trying lightkurve search with pattern: {pattern}")
                
                if mission == "KEPLER":
                    search_result = lk.search_lightcurve(pattern, mission="Kepler")
                else:  # K2
                    # Try different approaches for K2 data
                    try:
                        search_result = lk.search_lightcurve(pattern, mission="k2")
                    except Exception as k2_error:
                        logger.warning(f"K2 search failed for pattern '{pattern}': {k2_error}")
                        # Try without specifying mission for K2
                        search_result = lk.search_lightcurve(pattern)
                
                logger.info(f"Search result for '{pattern}': {len(search_result)} files found")
                
                if len(search_result) > 0:
                    logger.info(f"Downloading lightcurve with pattern: {pattern}")
                    
                    try:
                        lc = search_result.download_all()
                    except Exception as download_error:
                        logger.warning(f"Download failed for pattern '{pattern}': {download_error}")
                        # Try downloading individual files if bulk download fails
                        if "K2SC" in str(download_error) or "not supported" in str(download_error):
                            logger.info(f"Trying individual file download for pattern '{pattern}'")
                            try:
                                # Filter out K2SC products and try standard K2 products
                                filtered_results = []
                                for i, result in enumerate(search_result):
                                    if "k2sc" not in str(result).lower():
                                        filtered_results.append(result)
                                
                                if filtered_results:
                                    logger.info(f"Found {len(filtered_results)} non-K2SC products")
                                    # Download all filtered results and create a collection
                                    downloaded_lcs = []
                                    for result in filtered_results:
                                        try:
                                            single_lc = result.download()
                                            downloaded_lcs.append(single_lc)
                                        except Exception as single_error:
                                            logger.warning(f"Failed to download individual file: {single_error}")
                                            continue
                                    
                                    if downloaded_lcs:
                                        # Create a LightCurveCollection from individual downloads
                                        import lightkurve as lk
                                        lc = lk.LightCurveCollection(downloaded_lcs)
                                    else:
                                        logger.warning(f"No files successfully downloaded for pattern '{pattern}'")
                                        continue
                                else:
                                    logger.warning(f"No non-K2SC products found for pattern '{pattern}'")
                                    continue
                            except Exception as individual_error:
                                logger.warning(f"Individual download failed for pattern '{pattern}': {individual_error}")
                                continue
                        else:
                            continue
                    
                    if lc is not None and len(lc) > 0:
                        successful_pattern = pattern
                        logger.info(f"Successfully downloaded with pattern: {pattern}")
                        break
                        
            except Exception as e:
                logger.warning(f"lightkurve search failed for pattern '{pattern}': {e}")
                continue
        
        if lc is not None and len(lc) > 0:
            logger.info(f"Processing lightkurve data (successful pattern: {successful_pattern})")
            
            # Stitch quarters/campaigns together if multiple
            if hasattr(lc, 'stitch'):
                lc = lc.stitch()
            elif len(lc) > 1:
                # If multiple lightcurves, use the first one
                lc = lc[0]
            else:
                lc = lc[0] if isinstance(lc, list) else lc
            
            # Extract data
            time = lc.time.value
            flux = lc.flux.value
            
            # Remove NaN values
            valid_mask = ~(np.isnan(time) | np.isnan(flux))
            time = time[valid_mask]
            flux = flux[valid_mask]
            
            logger.info(f"lightkurve data processed: {len(time)} valid points")
            
            if len(time) > 0:
                # Calculate statistics
                flux_mean = np.mean(flux)
                flux_std = np.std(flux)
                flux_median = np.median(flux)
                
                # Normalize flux
                flux_normalized = (flux - flux_median) / flux_median
                
                logger.info(f"Successfully processed {mission} lightcurve for {kep_id} via lightkurve: {len(time)} points")
                
                return {
                    "mission": mission,
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
                    "method": "lightkurve",
                    "search_pattern": successful_pattern
                }
        
        logger.warning(f"lightkurve returned empty data for {mission} {kep_id}")
        
    except ImportError as e:
        logger.error(f"lightkurve not available: {e}")
    except Exception as e:
        logger.error(f"lightkurve failed for {mission} {kep_id}: {e}")
    
    # Strategy 2: Fallback to astroquery with enhanced search
    logger.info(f"Falling back to astroquery for {mission} {kep_id}")
    try:
        return _download_kepler_astroquery(kep_id, mission)
    except Exception as e:
        logger.error(f"astroquery fallback failed for {mission} {kep_id}: {e}")
    
    # Strategy 3: Final fallback - try alternative target ID formats
    logger.info(f"Trying final fallback strategies for {mission} {kep_id}")
    
    # Try with different ID formats
    alternative_ids = []
    if mission == "KEPLER":
        # Sometimes Kepler IDs need different formatting
        alternative_ids = [
            kep_id + 1,  # Sometimes off by one
            kep_id - 1,
            int(f"{kep_id:09d}"),  # Zero-padded format
        ]
    else:  # K2
        alternative_ids = [
            kep_id + 1,
            kep_id - 1,
        ]
    
    for alt_id in alternative_ids:
        try:
            logger.info(f"Trying alternative ID: {alt_id}")
            return _download_kepler_astroquery(alt_id, mission)
        except Exception as e:
            logger.warning(f"Alternative ID {alt_id} failed: {e}")
            continue
    
    # If all strategies fail, raise the original error
    logger.error(f"All fallback strategies failed for {mission} {kep_id}")
    raise LightcurveError(f"No lightcurve products found for {mission} {kep_id}")


def _download_kepler_astroquery(kep_id: int, mission: str) -> Dict[str, Any]:
    """
    Fallback method using astroquery for Kepler/K2 data.
    
    Args:
        kep_id (int): Kepler ID or EPIC ID
        mission (str): Mission name
        
    Returns:
        Dict[str, Any]: Lightcurve data
    """
    try:
        from astroquery.mast import Observations
        
        # Normalize mission to uppercase
        mission = mission.upper()
        
        logger.info(f"Attempting astroquery download for {mission} {kep_id}")
        
        # Log astroquery version
        try:
            import astroquery
            logger.info(f"astroquery version: {astroquery.__version__}")
        except:
            logger.warning("Could not determine astroquery version")
        
        # Ensure cache directory exists
        os.makedirs("./cache/lightcurves", exist_ok=True)
        logger.info(f"Cache directory created/verified: ./cache/lightcurves")
        
        # Try multiple search strategies
        search_strategies = []
        
        if mission == "KEPLER":
            search_strategies = [
                {"target_name": f"kplr{kep_id:09d}", "obs_collection": "Kepler"},
                {"target_name": f"KIC {kep_id}", "obs_collection": "Kepler"},
                {"target_name": str(kep_id), "obs_collection": "Kepler"},
            ]
        else:  # K2
            search_strategies = [
                {"target_name": f"ktwo{kep_id:09d}", "obs_collection": "K2"},
                {"target_name": f"EPIC {kep_id}", "obs_collection": "K2"},
                {"target_name": str(kep_id), "obs_collection": "K2"},
            ]
        
        obs_table = None
        successful_strategy = None
        
        # Try each search strategy
        for i, strategy in enumerate(search_strategies):
            try:
                logger.info(f"Search strategy {i+1}: target_name={strategy['target_name']}, obs_collection={strategy['obs_collection']}")
                
                obs_table = Observations.query_criteria(**strategy)
                
                logger.info(f"Strategy {i+1} returned {len(obs_table)} observations")
                
                if len(obs_table) > 0:
                    successful_strategy = strategy
                    break
                    
            except Exception as e:
                logger.warning(f"Search strategy {i+1} failed: {e}")
                continue
        
        if obs_table is None or len(obs_table) == 0:
            logger.error(f"All search strategies failed for {mission} {kep_id}")
            raise LightcurveError(f"No {mission} observations found for {kep_id}")
        
        logger.info(f"Successful search strategy: {successful_strategy}")
        
        # Log observation details
        for i, obs in enumerate(obs_table[:3]):  # Log first 3 observations
            logger.info(f"Observation {i}: obsid={obs.get('obsid', 'N/A')}, "
                       f"target_name={obs.get('target_name', 'N/A')}, "
                       f"obs_collection={obs.get('obs_collection', 'N/A')}")
        
        # Get data products for first observation
        obs_id = obs_table[0]['obsid']
        logger.info(f"Getting products for observation ID: {obs_id}")
        
        products = Observations.get_product_list(obs_id)
        logger.info(f"Found {len(products)} total products")
        
        # Try multiple product filtering strategies
        lc_products = None
        
        # Fix for astropy Table filtering - use proper indexing
        for strategy_name, filter_func in [
            ("LC products", lambda p: p['productSubGroupDescription'] == 'LC'),
            ("lightcurve products", lambda p: 'lightcurve' in str(p.get('productSubGroupDescription', '')).lower()),
            ("LC filename products", lambda p: 'lc' in str(p.get('productFilename', '')).lower()),
            ("SCIENCE products", lambda p: p.get('productType', '') == 'SCIENCE'),
        ]:
            try:
                # Use list comprehension with proper indexing for astropy Table
                filtered_indices = []
                for i, row in enumerate(products):
                    try:
                        if filter_func(row):
                            filtered_indices.append(i)
                    except Exception:
                        continue
                
                if filtered_indices:
                    lc_products = products[filtered_indices]
                    logger.info(f"Found {len(lc_products)} {strategy_name}")
                    logger.info(f"Using {strategy_name} for download")
                    break
                else:
                    logger.info(f"Found 0 {strategy_name}")
                    
            except Exception as e:
                logger.warning(f"Product filtering strategy '{strategy_name}' failed: {e}")
                continue
        
        if lc_products is None or len(lc_products) == 0:
            # Log available product types for debugging
            try:
                unique_types = set(str(p.get('productSubGroupDescription', '')) for p in products)
                unique_filenames = set(str(p.get('productFilename', '')).split('_')[0] for p in products)
                logger.error(f"No lightcurve products found for {mission} {kep_id}. "
                            f"Available product types: {list(unique_types)}, "
                            f"Filename prefixes: {list(unique_filenames)}")
            except Exception as e:
                logger.error(f"Could not log product details: {e}")
            raise LightcurveError(f"No lightcurve products found for {mission} {kep_id}")
        
        # Log lightcurve product details
        for i, product in enumerate(lc_products[:3]):  # Log first 3 products
            logger.info(f"LC Product {i}: "
                       f"productFilename={product.get('productFilename', 'N/A')}, "
                       f"size={product.get('size', 'N/A')}")
        
        # Download first lightcurve file
        logger.info(f"Downloading lightcurve product: {lc_products[0]['productFilename']}")
        
        download_result = Observations.download_products(
            lc_products[0:1],
            download_dir="./cache/lightcurves"
        )
        
        logger.info(f"Download completed. Result: {len(download_result)} files")
        
        if len(download_result) == 0:
            logger.error(f"Failed to download {mission} lightcurve for {kep_id}")
            raise LightcurveError(f"Failed to download {mission} lightcurve for {kep_id}")
        
        # Process downloaded FITS file
        fits_path = download_result['Local Path'][0]
        logger.info(f"Processing FITS file: {fits_path}")
        
        # Check if file exists and get size
        if os.path.exists(fits_path):
            file_size = os.path.getsize(fits_path)
            logger.info(f"FITS file size: {file_size} bytes")
        else:
            logger.error(f"FITS file not found at path: {fits_path}")
            raise LightcurveError(f"Downloaded FITS file not found: {fits_path}")
        
        with fits.open(fits_path) as hdul:
            logger.info(f"FITS file has {len(hdul)} HDUs")
            
            if len(hdul) < 2:
                logger.error(f"FITS file has insufficient HDUs: {len(hdul)}")
                raise LightcurveError("Invalid FITS file structure")
            
            data = hdul[1].data
            header = hdul[1].header
            
            logger.info(f"Data table has {len(data)} rows")
            logger.info(f"Available columns: {list(data.columns.names)}")
            
            # Try multiple flux column strategies
            flux_columns = ['PDCSAP_FLUX', 'SAP_FLUX', 'FLUX']
            flux = None
            flux_column_used = None
            
            for col in flux_columns:
                if col in data.columns.names:
                    flux = data[col]
                    flux_column_used = col
                    logger.info(f"Using flux column: {col}")
                    break
            
            if flux is None:
                logger.error(f"No suitable flux column found. Available columns: {list(data.columns.names)}")
                raise LightcurveError("No suitable flux column found in FITS file")
            
            # Extract time
            time = data['TIME']
            
            logger.info(f"Raw data: {len(time)} time points, {len(flux)} flux points (column: {flux_column_used})")
            
            # Remove NaN values
            valid_mask = ~(np.isnan(time) | np.isnan(flux))
            time = time[valid_mask]
            flux = flux[valid_mask]
            
            logger.info(f"After NaN filtering: {len(time)} valid points")
            
            if len(time) == 0:
                logger.error(f"No valid data points found after filtering for {mission} {kep_id}")
                raise LightcurveError("No valid data points found")
            
            # Calculate statistics
            flux_mean = np.mean(flux)
            flux_std = np.std(flux)
            flux_median = np.median(flux)
            
            # Normalize flux
            flux_normalized = (flux - flux_median) / flux_median
            
            logger.info(f"Successfully processed {mission} lightcurve for {kep_id} via astroquery: {len(time)} points")
            
            return {
                "mission": mission,
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
                "campaign": header.get('CAMPAIGN', 'unknown'),
                "method": "astroquery",
                "flux_column": flux_column_used,
                "search_strategy": successful_strategy
            }
            
    except Exception as e:
        logger.error(f"Error in astroquery download for {mission} {kep_id}: {e}")
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