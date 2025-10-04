"""
ML Models module for ExoScout Backend.

Handles loading and using trained XGBoost CalibratedClassifierCV models
for exoplanet classification.
"""

import os
import logging
from typing import Dict, List, Any, Tuple
import pickle

import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Model configuration
MODELS_DIR = os.getenv("MODELS_DIR", "models")


class ModelError(Exception):
    """Raised when ML model operations fail."""
    pass


class ExoplanetClassifier:
    """Exoplanet classifier using trained XGBoost models."""
    
    def __init__(self, mission: str):
        """
        Initialize classifier for a specific mission.
        
        Args:
            mission (str): Mission name (TESS, Kepler, K2)
        """
        self.mission = mission.upper()
        self.model = None
        self.feature_order = None
        self.threshold = None
        self._load_model()
    
    def _get_model_files(self) -> Tuple[str, str, str]:
        """
        Get model file paths for the mission.
        
        Returns:
            Tuple[str, str, str]: (model_path, feature_order_path, threshold_path)
        """
        mission_lower = self.mission.lower()
        
        if self.mission == "TESS":
            model_file = "toi_model.calibrated.pkl"
            feature_file = "toi_feature_order.pkl"
            threshold_file = "toi_threshold.pkl"
        elif self.mission == "KEPLER":
            model_file = "koi_model.calibrated.pkl"
            feature_file = "koi_feature_order.pkl"
            threshold_file = "koi_threshold.pkl"
        elif self.mission == "K2":
            model_file = "k2_model.calibrated.pkl"
            feature_file = "k2_feature_order.pkl"
            threshold_file = "k2_threshold.pkl"
        else:
            raise ModelError(f"Unsupported mission: {self.mission}")
        
        model_path = os.path.join(MODELS_DIR, model_file)
        feature_path = os.path.join(MODELS_DIR, feature_file)
        threshold_path = os.path.join(MODELS_DIR, threshold_file)
        
        return model_path, feature_path, threshold_path
    
    def _load_model(self):
        """Load model, feature order, and threshold from files."""
        try:
            model_path, feature_path, threshold_path = self._get_model_files()
            
            # Load model
            if not os.path.exists(model_path):
                raise ModelError(f"Model file not found: {model_path}")
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            logger.info(f"Loaded {self.mission} model from {model_path}")
            
            # Load feature order
            if not os.path.exists(feature_path):
                raise ModelError(f"Feature order file not found: {feature_path}")
            
            with open(feature_path, 'rb') as f:
                self.feature_order = pickle.load(f)
            logger.info(f"Loaded {self.mission} feature order: {len(self.feature_order)} features")
            
            # Load threshold
            if not os.path.exists(threshold_path):
                raise ModelError(f"Threshold file not found: {threshold_path}")
            
            with open(threshold_path, 'rb') as f:
                self.threshold = pickle.load(f)
            logger.info(f"Loaded {self.mission} threshold: {self.threshold}")
            
        except Exception as e:
            logger.error(f"Failed to load {self.mission} model: {e}")
            raise ModelError(f"Failed to load {self.mission} model: {e}")
    
    def prepare_features(self, features: Dict[str, Any]) -> np.ndarray:
        """
        Prepare feature vector from feature dictionary.
        
        Args:
            features (Dict[str, Any]): Feature dictionary
            
        Returns:
            np.ndarray: Feature vector ready for prediction
            
        Raises:
            ModelError: If feature preparation fails
        """
        try:
            # Create feature vector in correct order
            feature_vector = []
            missing_features = []
            
            for feature_name in self.feature_order:
                if feature_name in features:
                    value = features[feature_name]
                    
                    # Handle None/null values
                    if value is None or value == "" or (isinstance(value, str) and value.lower() in ['nan', 'null']):
                        value = 0.0  # Default value for missing features
                    
                    # Convert to float
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        logger.warning(f"Could not convert feature {feature_name} value {value} to float, using 0.0")
                        value = 0.0
                    
                    feature_vector.append(value)
                else:
                    missing_features.append(feature_name)
                    feature_vector.append(0.0)  # Default value for missing features
            
            if missing_features:
                logger.warning(f"Missing features for {self.mission}: {missing_features}")
            
            return np.array(feature_vector).reshape(1, -1)
            
        except Exception as e:
            logger.error(f"Feature preparation failed for {self.mission}: {e}")
            raise ModelError(f"Feature preparation failed: {e}")
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make prediction for given features.
        
        Args:
            features (Dict[str, Any]): Feature dictionary
            
        Returns:
            Dict[str, Any]: Prediction results
            
        Raises:
            ModelError: If prediction fails
        """
        try:
            # Prepare features
            feature_vector = self.prepare_features(features)
            
            # Get prediction probability
            probability = self.model.predict_proba(feature_vector)[0][1]  # Probability of positive class
            
            # Apply threshold for classification
            classification = "CONFIRMED" if probability >= self.threshold else "FALSE_POSITIVE"
            
            logger.info(f"{self.mission} prediction: {probability:.4f} -> {classification}")
            
            return {
                "mission": self.mission,
                "probability": float(probability),
                "classification": classification,
                "threshold": float(self.threshold),
                "features_used": len(self.feature_order),
                "features_available": len([f for f in self.feature_order if f in features])
            }
            
        except Exception as e:
            logger.error(f"Prediction failed for {self.mission}: {e}")
            raise ModelError(f"Prediction failed: {e}")


# Global model cache
_model_cache: Dict[str, ExoplanetClassifier] = {}


def get_classifier(mission: str) -> ExoplanetClassifier:
    """
    Get classifier for mission (cached).
    
    Args:
        mission (str): Mission name
        
    Returns:
        ExoplanetClassifier: Classifier instance
    """
    mission = mission.upper()
    
    if mission not in _model_cache:
        _model_cache[mission] = ExoplanetClassifier(mission)
    
    return _model_cache[mission]


def get_available_missions() -> List[str]:
    """
    Get list of available missions with trained models.
    
    Returns:
        List[str]: Available mission names
    """
    available = []
    
    for mission in ["TESS", "KEPLER", "K2"]:
        try:
            classifier = ExoplanetClassifier(mission)
            available.append(mission)
        except ModelError:
            logger.warning(f"Model not available for mission: {mission}")
    
    return available


def get_feature_order(mission: str) -> List[str]:
    """
    Get feature order for a mission.
    
    Args:
        mission (str): Mission name
        
    Returns:
        List[str]: Feature names in order
        
    Raises:
        ModelError: If mission not supported
    """
    classifier = get_classifier(mission)
    return classifier.feature_order.copy()