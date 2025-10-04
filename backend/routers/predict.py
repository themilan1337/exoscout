"""
Predict router for ExoScout Backend.

Handles ML-based exoplanet classification using trained XGBoost models.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from services.model import get_model_info, ModelError, get_available_missions
from services.nasa_api import get_tess_features, get_kepler_features, get_k2_features
from utils.cache import cached

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/predict", tags=["predict"])

# Cache predictions for 1 hour
CACHE_TTL = 3600


async def get_feature_data(mission: str, target_id: str) -> Dict[str, Any]:
    """
    Get features for a specific mission and target.
    
    Args:
        mission (str): Mission name
        target_id (str): Target ID
        
    Returns:
        Dict[str, Any]: Feature dictionary
        
    Raises:
        HTTPException: If features cannot be retrieved
    """
    try:
        mission = mission.upper()
        target_id_int = int(target_id)
        
        if mission == "TESS":
            features = await get_tess_features(target_id_int)
        elif mission == "KEPLER":
            features = await get_kepler_features(target_id_int)
        elif mission == "K2":
            features = await get_k2_features(target_id_int)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported mission: {mission}"
            )
        
        return features
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid target ID format: {target_id}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting features for {mission} {target_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve features: {str(e)}"
        )


@router.get("/models/status")
async def get_models_status() -> Dict[str, Any]:
    """
    Get status of available ML models.
    
    Returns:
        Dict[str, Any]: Model status information
    """
    try:
        available_missions = get_available_missions()
        
        model_info = {}
        
        for mission in available_missions:
            try:
                info = await run_in_threadpool(get_model_info, mission)
                model_info[mission] = {
                    "available": True,
                    "features_count": len(info["features"]),
                    "threshold": info["threshold"],
                    "model_type": str(type(info["model"]).__name__)
                }
            except Exception as e:
                model_info[mission] = {
                    "available": False,
                    "error": str(e)
                }
        
        return {
            "available_missions": available_missions,
            "models": model_info,
            "total_available": len([m for m in model_info.values() if m.get("available", False)])
        }
        
    except Exception as e:
        logger.error(f"Error getting model status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model status: {str(e)}"
        )


@router.get("/{mission}/{target_id}")
@cached("predict", ttl=CACHE_TTL)
async def predict_exoplanet(mission: str, target_id: str) -> Dict[str, Any]:
    """
    Run ML inference for the specified mission and target.
    Uses pre-trained Calibrated XGBoost models.
    
    Args:
        mission (str): Mission name (TESS, Kepler, K2)
        target_id (str): Target ID (TIC ID, Kepler ID, EPIC ID)
        
    Returns:
        Dict[str, Any]: Prediction results including probability and classification
        
    Raises:
        HTTPException: If prediction fails
    """
    try:
        mission = mission.upper()
        
        # Load model + metadata
        info = await run_in_threadpool(get_model_info, mission)
        model, features, tau = info["model"], info["features"], info["threshold"]
        
        logger.info(f"Making prediction for {mission} {target_id}")
        
        # Get feature dictionary for the target
        feature_data = await get_feature_data(mission, target_id)
        
        if not feature_data:
            raise HTTPException(
                status_code=404,
                detail=f"No features found for {mission} {target_id}"
            )
        
        # Assemble feature vector with exact feature order
        x = pd.DataFrame([[feature_data.get(f, np.nan) for f in features]], columns=features)
        
        # Predict (offloaded to thread)
        proba = await run_in_threadpool(lambda: model.predict_proba(x)[:, 1][0])
        classification = "CONFIRMED" if proba >= tau else "FALSE_POSITIVE"
        
        result = {
            "mission": mission.upper(),
            "target_id": target_id,
            "probability": round(float(proba), 4),
            "threshold": tau,
            "classification": classification,
            "used_features": {f: feature_data.get(f, None) for f in features},
        }
        
        logger.info(
            f"Prediction complete for {mission} {target_id}: "
            f"{classification} (p={proba:.4f})"
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in prediction for {mission} {target_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")


@router.get("/{mission}/{target_id}/features")
async def get_prediction_features(mission: str, target_id: str) -> Dict[str, Any]:
    """
    Get features used for prediction for a specific target.
    
    Args:
        mission (str): Mission name (TESS, Kepler, K2)
        target_id (str): Target identifier
        
    Returns:
        Dict[str, Any]: Feature data for the target
    """
    try:
        # Validate mission
        if mission.upper() not in get_available_missions():
            raise ValueError(f"Mission {mission} not supported. Available: {get_available_missions()}")
        
        # Get model info to know which features are needed
        info = await run_in_threadpool(get_model_info, mission)
        required_features = info["features"]
        
        # Get feature data for the target
        feature_data = await get_feature_data(mission, target_id)
        
        # Filter to only include features used by the model
        filtered_features = {f: feature_data.get(f, None) for f in required_features}
        
        return {
            "mission": mission.upper(),
            "target_id": target_id,
            "features": filtered_features,
            "feature_count": len(required_features),
            "available_features": len([f for f in filtered_features.values() if f is not None])
        }
        
    except ValueError as e:
        logger.error(f"Validation error for {mission}/{target_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting features for {mission}/{target_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get features: {str(e)}"
        )


@router.get("/{mission}/{target_id}/custom")
async def predict_with_custom_features(
    mission: str,
    target_id: str,
    features: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Make prediction with custom feature values.
    
    Args:
        mission (str): Mission name
        target_id (str): Target ID
        features (Dict[str, float]): Custom feature dictionary
        
    Returns:
        Dict[str, Any]: Prediction results
    """
    try:
        mission = mission.upper()
        
        # Load model + metadata
        info = await run_in_threadpool(get_model_info, mission)
        model, feature_names, tau = info["model"], info["features"], info["threshold"]
        
        logger.info(f"Making custom prediction for {mission} {target_id}")
        
        # Use provided features or get from API
        if features is None:
            feature_data = await get_feature_data(mission, target_id)
        else:
            feature_data = features
        
        # Assemble feature vector with exact feature order
        x = pd.DataFrame([[feature_data.get(f, np.nan) for f in feature_names]], columns=feature_names)
        
        # Predict (offloaded to thread)
        proba = await run_in_threadpool(lambda: model.predict_proba(x)[:, 1][0])
        classification = "CONFIRMED" if proba >= tau else "FALSE_POSITIVE"
        
        result = {
            "mission": mission.upper(),
            "target_id": target_id,
            "probability": round(float(proba), 4),
            "threshold": tau,
            "classification": classification,
            "used_features": {f: feature_data.get(f, None) for f in feature_names},
            "custom_prediction": features is not None
        }
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in custom prediction for {mission} {target_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Custom prediction failed: {str(e)}"
        )


@router.post("/{mission}/{target_id}/custom")
async def predict_with_custom_features(
    mission: str, 
    target_id: str, 
    custom_features: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Make prediction with custom feature values.
    
    Args:
        mission (str): Mission name
        target_id (str): Target ID
        custom_features (Dict[str, Any]): Custom feature dictionary
        
    Returns:
        Dict[str, Any]: Prediction results
    """
    try:
        mission = mission.upper()
        
        # Load model + metadata
        info = await run_in_threadpool(get_model_info, mission)
        model, features, tau = info["model"], info["features"], info["threshold"]
        
        logger.info(f"Making custom prediction for {mission} {target_id}")
        
        # Assemble feature vector with exact feature order
        x = pd.DataFrame([[custom_features.get(f, np.nan) for f in features]], columns=features)
        
        # Predict (offloaded to thread)
        proba = await run_in_threadpool(lambda: model.predict_proba(x)[:, 1][0])
        classification = "CONFIRMED" if proba >= tau else "FALSE_POSITIVE"
        
        result = {
            "mission": mission.upper(),
            "target_id": target_id,
            "probability": round(float(proba), 4),
            "threshold": tau,
            "classification": classification,
            "used_features": {f: custom_features.get(f, None) for f in features},
            "custom_prediction": True
        }
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in custom prediction for {mission} {target_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Custom prediction failed: {str(e)}"
        )