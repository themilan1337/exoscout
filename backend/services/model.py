"""
Model management service for ExoScout backend.
Handles loading and caching of pre-trained ML models for TESS, Kepler, and K2 missions.
"""

from pathlib import Path
import joblib
import logging
from typing import Dict, Any
from functools import lru_cache

logger = logging.getLogger(__name__)

# Model paths configuration
MODELS = {
    "TESS": {
        "model": Path("models/toi_model.calibrated.pkl"),
        "features": Path("models/feature_order.pkl"),
        "threshold": Path("models/decision_threshold.pkl"),
    },
    "K2": {
        "model": Path("models/k2_model.calibrated.pkl"),
        "features": Path("models/k2_feature_order.pkl"),
        "threshold": Path("models/k2_threshold.pkl"),
    },
    "KEPLER": {
        "model": Path("models/koi_model.calibrated.pkl"),
        "features": Path("models/koi_feature_order.pkl"),
        "threshold": Path("models/koi_threshold.pkl"),
    },
}


class ModelError(Exception):
    """Custom exception for model-related errors."""
    pass


@lru_cache(maxsize=3)
def get_model_info(mission: str) -> Dict[str, Any]:
    """
    Loads model, feature order, and threshold for a given mission.
    
    Args:
        mission: Mission name (TESS, K2, or KEPLER)
        
    Returns:
        Dictionary containing model, features list, and threshold value
        
    Raises:
        ValueError: If mission not supported
        ModelError: If model files cannot be loaded
    """
    mission = mission.upper()
    
    if mission not in MODELS:
        available_missions = list(MODELS.keys())
        raise ValueError(f"Mission {mission} not supported. Available: {available_missions}")
    
    paths = MODELS[mission]
    
    try:
        # Load model
        model_path = paths["model"]
        if not model_path.exists():
            raise ModelError(f"Model file not found: {model_path}")
        model = joblib.load(model_path)
        logger.info(f"Loaded model for {mission}: {model_path}")
        
        # Load feature order
        features_path = paths["features"]
        if not features_path.exists():
            raise ModelError(f"Features file not found: {features_path}")
        features = joblib.load(features_path)
        logger.info(f"Loaded features for {mission}: {len(features)} features")
        
        # Load threshold
        threshold_path = paths["threshold"]
        if not threshold_path.exists():
            raise ModelError(f"Threshold file not found: {threshold_path}")
        threshold_data = joblib.load(threshold_path)
        
        # Handle different threshold file formats
        if isinstance(threshold_data, dict):
            threshold = threshold_data.get("tau", threshold_data.get("threshold", 0.5))
        else:
            threshold = float(threshold_data)
        
        logger.info(f"Loaded threshold for {mission}: {threshold}")
        
        return {
            "model": model,
            "features": features,
            "threshold": threshold
        }
        
    except Exception as e:
        logger.error(f"Failed to load model info for {mission}: {e}")
        raise ModelError(f"Failed to load model for {mission}: {e}")


def get_available_missions() -> list:
    """
    Returns list of available missions.
    
    Returns:
        List of mission names
    """
    return list(MODELS.keys())


def validate_model_files() -> Dict[str, bool]:
    """
    Validates that all required model files exist.
    
    Returns:
        Dictionary mapping mission names to validation status
    """
    validation_results = {}
    
    for mission, paths in MODELS.items():
        mission_valid = True
        missing_files = []
        
        for file_type, path in paths.items():
            if not path.exists():
                mission_valid = False
                missing_files.append(f"{file_type}: {path}")
        
        validation_results[mission] = {
            "valid": mission_valid,
            "missing_files": missing_files
        }
        
        if mission_valid:
            logger.info(f"All model files found for {mission}")
        else:
            logger.warning(f"Missing model files for {mission}: {missing_files}")
    
    return validation_results