"""
NASA API service for ExoScout Backend.

Provides functions to interact with NASA Exoplanet Archive API,
TESSCut API, and other NASA data sources.
"""

import os
import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import quote

import httpx
import pandas as pd
from dotenv import load_dotenv

from utils.cache import cached

load_dotenv()

logger = logging.getLogger(__name__)

# API URLs
NASA_EXOPLANET_ARCHIVE_URL = os.getenv("NASA_EXOPLANET_ARCHIVE_URL", "https://exoplanetarchive.ipac.caltech.edu/TAP/sync")
TESSCUT_API_URL = os.getenv("TESSCUT_API_URL", "https://mast.stsci.edu/tesscut/api/v0.1/astrocut")

# HTTP client configuration
HTTP_TIMEOUT = 30.0


class NASAAPIError(Exception):
    """Raised when NASA API calls fail."""
    pass


def detect_mission_and_id(target: str) -> Tuple[str, str, Optional[str]]:
    """
    Detect mission type and extract ID from target string.
    
    Args:
        target (str): Target identifier (e.g., "TOI-1019.01", "K00752.01", "TIC 307210830")
        
    Returns:
        Tuple[str, str, Optional[str]]: (mission, id, original_target)
        
    Raises:
        ValueError: If target format is not recognized
    """
    target = target.strip()
    
    # TOI patterns
    toi_patterns = [
        r'^TOI[-\s]?(\d+(?:\.\d+)?)$',
        r'^(\d+(?:\.\d+)?)$'  # Just numbers for TOI
    ]
    
    # KOI patterns  
    koi_patterns = [
        r'^KOI[-\s]?(\d+(?:\.\d+)?)$',
        r'^K(\d+(?:\.\d+)?)$'
    ]
    
    # K2 patterns
    k2_patterns = [
        r'^K2[-\s]?(\d+(?:\.\d+)?)$',
        r'^EPIC[-\s]?(\d+)$'
    ]
    
    # TIC patterns
    tic_patterns = [
        r'^TIC[-\s]?(\d+)$',
        r'^TESS[-\s]?(\d+)$'
    ]
    
    # Kepler patterns
    kepler_patterns = [
        r'^KIC[-\s]?(\d+)$',
        r'^Kepler[-\s]?(\d+)(?:\s*[a-z])?$'
    ]
    
    # Check TOI
    for pattern in toi_patterns:
        match = re.match(pattern, target, re.IGNORECASE)
        if match:
            return "TESS", match.group(1), target
    
    # Check KOI
    for pattern in koi_patterns:
        match = re.match(pattern, target, re.IGNORECASE)
        if match:
            return "Kepler", match.group(1), target
    
    # Check K2
    for pattern in k2_patterns:
        match = re.match(pattern, target, re.IGNORECASE)
        if match:
            return "K2", match.group(1), target
    
    # Check TIC
    for pattern in tic_patterns:
        match = re.match(pattern, target, re.IGNORECASE)
        if match:
            return "TESS", match.group(1), target
    
    # Check Kepler
    for pattern in kepler_patterns:
        match = re.match(pattern, target, re.IGNORECASE)
        if match:
            return "Kepler", match.group(1), target
    
    raise ValueError(f"Unrecognized target format: {target}")


@cached("nasa_tap_query", ttl=3600)
async def query_nasa_tap(query: str) -> List[Dict[str, Any]]:
    """
    Execute a TAP query against NASA Exoplanet Archive.
    
    Args:
        query (str): SQL query string
        
    Returns:
        List[Dict[str, Any]]: Query results
        
    Raises:
        NASAAPIError: If API call fails
    """
    params = {
        "query": query,
        "format": "json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.get(NASA_EXOPLANET_ARCHIVE_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"NASA TAP query returned {len(data)} results")
            return data
            
    except httpx.HTTPError as e:
        logger.error(f"NASA TAP query failed: {e}")
        raise NASAAPIError(f"NASA TAP query failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in NASA TAP query: {e}")
        raise NASAAPIError(f"Unexpected error: {e}")


async def resolve_toi_to_tic(toi_id: str) -> Dict[str, Any]:
    """
    Resolve TOI ID to TIC ID and metadata.
    
    Args:
        toi_id (str): TOI identifier (e.g., "1019.01")
        
    Returns:
        Dict[str, Any]: TOI data including TIC ID
        
    Raises:
        NASAAPIError: If resolution fails
    """
    query = f"select * from toi where toi={toi_id}"
    results = await query_nasa_tap(query)
    
    if not results:
        raise NASAAPIError(f"TOI {toi_id} not found")
    
    return results[0]


async def resolve_koi_to_kepid(koi_id: str) -> Dict[str, Any]:
    """
    Resolve KOI ID to Kepler ID and metadata.
    
    Args:
        koi_id (str): KOI identifier (e.g., "752.01")
        
    Returns:
        Dict[str, Any]: KOI data including Kepler ID
        
    Raises:
        NASAAPIError: If resolution fails
    """
    query = f"select * from cumulative where kepoi_name='K{koi_id:0>8}'"
    results = await query_nasa_tap(query)
    
    if not results:
        # Try alternative format
        query = f"select * from cumulative where kepoi_name='{koi_id}'"
        results = await query_nasa_tap(query)
    
    if not results:
        raise NASAAPIError(f"KOI {koi_id} not found")
    
    return results[0]


async def get_tess_features(tic_id: str) -> Dict[str, Any]:
    """
    Get TESS features for a TIC ID.
    
    Args:
        tic_id (str): TIC identifier
        
    Returns:
        Dict[str, Any]: TESS features
        
    Raises:
        NASAAPIError: If data not found
    """
    query = f"select * from toi where tid={tic_id}"
    results = await query_nasa_tap(query)
    
    if not results:
        raise NASAAPIError(f"TIC {tic_id} not found in TOI table")
    
    return results[0]


async def get_kepler_features(kepid: str) -> Dict[str, Any]:
    """
    Get Kepler features for a Kepler ID.
    
    Args:
        kepid (str): Kepler ID
        
    Returns:
        Dict[str, Any]: Kepler features
        
    Raises:
        NASAAPIError: If data not found
    """
    query = f"select * from cumulative where kepid={kepid}"
    results = await query_nasa_tap(query)
    
    if not results:
        raise NASAAPIError(f"Kepler ID {kepid} not found")
    
    return results[0]


async def get_k2_features(epic_id: str) -> Dict[str, Any]:
    """
    Get K2 features for an EPIC ID.
    
    Args:
        epic_id (str): EPIC ID
        
    Returns:
        Dict[str, Any]: K2 features
        
    Raises:
        NASAAPIError: If data not found
    """
    query = f"select * from k2targets where epic_number={epic_id}"
    results = await query_nasa_tap(query)
    
    if not results:
        raise NASAAPIError(f"EPIC {epic_id} not found")
    
    return results[0]


@cached("tesscut_sector_info", ttl=3600)
async def get_tesscut_sector_info(ra: float, dec: float) -> List[Dict[str, Any]]:
    """
    Get TESS sector information for coordinates.
    
    Args:
        ra (float): Right ascension in degrees
        dec (float): Declination in degrees
        
    Returns:
        List[Dict[str, Any]]: Sector information
        
    Raises:
        NASAAPIError: If API call fails
    """
    url = f"{TESSCUT_API_URL}/sector"
    params = {
        "ra": ra,
        "dec": dec
    }
    
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"TESSCut sector query returned {len(data)} sectors")
            return data
            
    except httpx.HTTPError as e:
        logger.error(f"TESSCut sector query failed: {e}")
        raise NASAAPIError(f"TESSCut sector query failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in TESSCut sector query: {e}")
        raise NASAAPIError(f"Unexpected error: {e}")


async def download_tesscut_data(ra: float, dec: float, size: str = "5x5") -> bytes:
    """
    Download TESS cutout data.
    
    Args:
        ra (float): Right ascension in degrees
        dec (float): Declination in degrees
        size (str): Cutout size (e.g., "5x5")
        
    Returns:
        bytes: FITS file data
        
    Raises:
        NASAAPIError: If download fails
    """
    url = f"{TESSCUT_API_URL}/download"
    params = {
        "ra": ra,
        "dec": dec,
        "size": size
    }
    
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT * 3) as client:  # Longer timeout for downloads
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            logger.info(f"Downloaded TESSCut data for RA={ra}, Dec={dec}")
            return response.content
            
    except httpx.HTTPError as e:
        logger.error(f"TESSCut download failed: {e}")
        raise NASAAPIError(f"TESSCut download failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in TESSCut download: {e}")
        raise NASAAPIError(f"Unexpected error: {e}")


@cached("coordinates_from_archive", ttl=3600)
async def get_coordinates_from_archive(mission: str, target_id: int) -> Dict[str, Any]:
    """
    Get coordinates for a target from NASA Exoplanet Archive.
    
    Args:
        mission (str): Mission name (TESS, Kepler, K2)
        target_id (int): Target ID
        
    Returns:
        Dict[str, Any]: Coordinates and metadata
        
    Raises:
        NASAAPIError: If coordinates cannot be retrieved
    """
    try:
        mission = mission.upper()
        
        if mission == "TESS":
            # Query TIC catalog for coordinates
            query = f"""
            SELECT tic_id, ra, dec, pmra, pmdec, plx, gaia_mag, tess_mag
            FROM tic 
            WHERE tic_id = {target_id}
            """
        elif mission == "KEPLER":
            # Query Kepler Input Catalog
            query = f"""
            SELECT kepid, ra, dec, kepmag
            FROM kic 
            WHERE kepid = {target_id}
            """
        elif mission == "K2":
            # Query K2 EPIC catalog
            query = f"""
            SELECT epic_id, ra, dec, kepmag
            FROM k2targets 
            WHERE epic_id = {target_id}
            """
        else:
            raise NASAAPIError(f"Unsupported mission for coordinates: {mission}")
        
        results = await query_nasa_tap(query)
        
        if not results:
            raise NASAAPIError(f"No coordinates found for {mission} {target_id}")
        
        result = results[0]
        
        return {
            "mission": mission,
            "target_id": target_id,
            "ra": result.get("ra"),
            "dec": result.get("dec"),
            "pmra": result.get("pmra"),
            "pmdec": result.get("pmdec"),
            "parallax": result.get("plx"),
            "magnitude": result.get("tess_mag") or result.get("kepmag"),
            "gaia_mag": result.get("gaia_mag")
        }
        
    except Exception as e:
        logger.error(f"Error getting coordinates for {mission} {target_id}: {e}")
        raise NASAAPIError(f"Failed to get coordinates: {e}")


def clean_features_for_mission(features: Dict[str, Any], mission: str) -> Dict[str, Any]:
    """
    Clean and standardize features for a specific mission.
    
    Args:
        features (Dict[str, Any]): Raw features from NASA API
        mission (str): Mission name (TESS, Kepler, K2)
        
    Returns:
        Dict[str, Any]: Cleaned features
    """
    cleaned = {}
    
    for key, value in features.items():
        # Skip null values
        if value is None or value == "":
            continue
            
        # Convert string numbers to float
        if isinstance(value, str):
            try:
                value = float(value)
            except (ValueError, TypeError):
                pass
        
        # Store cleaned value
        cleaned[key] = value
    
    return cleaned