"""
Features router for ExoScout Backend.

Handles feature extraction from NASA Exoplanet Archive for different missions.
"""

import logging
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from services.nasa_api import (
    get_tess_features,
    get_kepler_features,
    get_k2_features,
    clean_features_for_mission,
    NASAAPIError
)

logger = logging.getLogger(__name__)

router = APIRouter()


class FeaturesResponse(BaseModel):
    """Response model for features endpoint."""
    mission: str
    target_id: str
    features: Dict[str, Any]
    feature_count: int


@router.get("/features/{mission}/{target_id}", response_model=FeaturesResponse)
async def get_features(
    mission: str = Path(..., description="Mission name (TESS, Kepler, K2)"),
    target_id: str = Path(..., description="Target ID (TIC ID, KepID, or EPIC ID)")
) -> FeaturesResponse:
    """
    Get feature values from NASA Exoplanet Archive for the specified mission and target.
    
    This endpoint pulls feature values directly from NASA Exoplanet Archive
    for the specified mission (TOI → TESS, KOI → Kepler, K2 table for K2).
    Returns a JSON dict containing the feature columns used in training.
    
    Args:
        mission (str): Mission name (TESS, Kepler, K2)
        target_id (str): Target identifier
        
    Returns:
        FeaturesResponse: Feature data for the target
        
    Raises:
        HTTPException: If mission is not supported or data not found
    """
    mission = mission.upper()
    
    if mission not in ["TESS", "KEPLER", "K2"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported mission: {mission}. Supported missions: TESS, Kepler, K2"
        )
    
    try:
        logger.info(f"Fetching features for {mission} target {target_id}")
        
        # Get features based on mission
        if mission == "TESS":
            raw_features = await get_tess_features(target_id)
        elif mission == "KEPLER":
            raw_features = await get_kepler_features(target_id)
        elif mission == "K2":
            raw_features = await get_k2_features(target_id)
        
        # Clean and standardize features
        features = clean_features_for_mission(raw_features, mission)
        
        logger.info(f"Retrieved {len(features)} features for {mission} target {target_id}")
        
        return FeaturesResponse(
            mission=mission,
            target_id=target_id,
            features=features,
            feature_count=len(features)
        )
        
    except NASAAPIError as e:
        logger.error(f"NASA API error getting features for {mission} {target_id}: {e}")
        raise HTTPException(
            status_code=404,
            detail=f"Features not found for {mission} target {target_id}: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error getting features for {mission} {target_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal error getting features for {mission} target {target_id}"
        )