"""
Resolve router for ExoScout Backend.

Handles target resolution and mission detection for various exoplanet identifiers.
"""

import logging
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from services.nasa_api import (
    detect_mission_and_id,
    resolve_toi_to_tic,
    resolve_koi_to_kepid,
    NASAAPIError
)

logger = logging.getLogger(__name__)

router = APIRouter()


class ResolveResponse(BaseModel):
    """Response model for resolve endpoint."""
    mission: str
    target: str
    original_target: str
    numeric_id: str
    ra: float = None
    dec: float = None
    metadata: Dict[str, Any] = {}


@router.get("/resolve/{target}", response_model=ResolveResponse)
async def resolve_target(
    target: str = Path(..., description="Target identifier (e.g., TOI-1019.01, K00752.01, TIC 307210830)")
) -> ResolveResponse:
    """
    Resolve target identifier to mission, numeric ID, and coordinates.
    
    This endpoint detects which mission a target belongs to (TESS, K2, Kepler)
    and resolves TOI/KOI identifiers to their corresponding TIC/KepID using
    the NASA Exoplanet Archive API.
    
    Args:
        target (str): Target identifier
        
    Returns:
        ResolveResponse: Resolved target information
        
    Raises:
        HTTPException: If target format is not recognized or resolution fails
    """
    try:
        # Detect mission and extract ID
        mission, numeric_id, original_target = detect_mission_and_id(target)
        logger.info(f"Detected mission: {mission}, ID: {numeric_id} for target: {target}")
        
        # Initialize response
        response = ResolveResponse(
            mission=mission,
            target=target,
            original_target=original_target or target,
            numeric_id=numeric_id
        )
        
        # Resolve to TIC/KepID if needed and get metadata
        if mission == "TESS":
            if target.upper().startswith(("TOI", "TOI-")):
                # Resolve TOI to TIC
                try:
                    toi_data = await resolve_toi_to_tic(numeric_id)
                    response.numeric_id = str(toi_data.get("tid", numeric_id))
                    response.ra = toi_data.get("ra")
                    response.dec = toi_data.get("dec")
                    response.metadata = {
                        "toi": toi_data.get("toi"),
                        "tid": toi_data.get("tid"),
                        "tfopwg_disp": toi_data.get("tfopwg_disp"),
                        "pl_orbper": toi_data.get("pl_orbper"),
                        "pl_rade": toi_data.get("pl_rade"),
                        "st_tmag": toi_data.get("st_tmag"),
                        "st_teff": toi_data.get("st_teff"),
                        "st_rad": toi_data.get("st_rad")
                    }
                    # Clean None values
                    response.metadata = {k: v for k, v in response.metadata.items() if v is not None}
                    
                except NASAAPIError as e:
                    logger.warning(f"Could not resolve TOI {numeric_id}: {e}")
                    # Continue with original numeric_id
            
        elif mission == "Kepler":
            if target.upper().startswith(("KOI", "KOI-", "K")):
                # Resolve KOI to KepID
                try:
                    koi_data = await resolve_koi_to_kepid(numeric_id)
                    response.numeric_id = str(koi_data.get("kepid", numeric_id))
                    response.ra = koi_data.get("ra")
                    response.dec = koi_data.get("dec")
                    response.metadata = {
                        "kepoi_name": koi_data.get("kepoi_name"),
                        "kepid": koi_data.get("kepid"),
                        "koi_disposition": koi_data.get("koi_disposition"),
                        "koi_period": koi_data.get("koi_period"),
                        "koi_prad": koi_data.get("koi_prad"),
                        "koi_kepmag": koi_data.get("koi_kepmag"),
                        "koi_steff": koi_data.get("koi_steff"),
                        "koi_srad": koi_data.get("koi_srad")
                    }
                    # Clean None values
                    response.metadata = {k: v for k, v in response.metadata.items() if v is not None}
                    
                except NASAAPIError as e:
                    logger.warning(f"Could not resolve KOI {numeric_id}: {e}")
                    # Continue with original numeric_id
        
        logger.info(f"Successfully resolved {target} to {mission} ID {response.numeric_id}")
        return response
        
    except ValueError as e:
        logger.error(f"Invalid target format: {target} - {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Unrecognized target format: {target}. "
                   f"Supported formats: TOI-1019.01, K00752.01, TIC 307210830, "
                   f"Kepler-227 b, EPIC 123456789"
        )
    except NASAAPIError as e:
        logger.error(f"NASA API error resolving {target}: {e}")
        raise HTTPException(
            status_code=502,
            detail=f"Failed to resolve target {target}: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error resolving {target}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal error resolving target {target}"
        )