"""Services package for ExoScout Backend.

Contains modules for external API interactions and model management."""

from .nasa_api import (
    detect_mission_and_id,
    query_nasa_tap,
    resolve_toi_to_tic,
    resolve_koi_to_kepid,
    get_tess_features,
    get_kepler_features,
    get_k2_features,
    get_tesscut_sector_info,
    download_tesscut_data,
    clean_features_for_mission,
    NASAAPIError
)

from .model import (
    get_model_info,
    get_available_missions,
    validate_model_files,
    ModelError
)

__all__ = [
    # NASA API functions
    "detect_mission_and_id",
    "query_nasa_tap",
    "resolve_toi_to_tic",
    "resolve_koi_to_kepid",
    "get_tess_features",
    "get_kepler_features",
    "get_k2_features",
    "get_tesscut_sector_info",
    "download_tesscut_data",
    "clean_features_for_mission",
    "NASAAPIError",
    # Model management functions
    "get_model_info",
    "get_available_missions",
    "validate_model_files",
    "ModelError"
]