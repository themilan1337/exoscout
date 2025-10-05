# ExoScout Backend API Documentation

## Overview

ExoScout is a FastAPI-based backend service for exoplanet detection and analysis using machine learning. The API provides endpoints for exoplanet prediction, feature extraction, lightcurve data retrieval, and target resolution across three NASA missions: TESS, Kepler, and K2.

## Base URL

```
http://localhost:8000
```

## API Version

All endpoints are prefixed with `/api/v1`

## Authentication

Currently, no authentication is required for API access.

## Response Format

All API responses follow a consistent JSON format:

### Success Response
```json
{
  "data": {...},
  "status": "success"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## Endpoints

### 1. Health Check

#### `GET /health`
Check if the API is running.

**Response:**
```json
{
  "status": "ok"
}
```

### 2. Root Endpoint

#### `GET /`
Get basic API information.

**Response:**
```json
{
  "message": "ExoScout Backend is running 🚀"
}
```

---

## Prediction Endpoints

### 3. Predict Exoplanet

#### `GET /api/v1/predict/{mission}/{target_id}`
Get ML-based exoplanet classification for a specific target.

**Parameters:**
- `mission` (string): Mission name - `TESS`, `KEPLER`, or `K2`
- `target_id` (string): Target identifier (TIC ID for TESS, KepID for Kepler, EPIC ID for K2)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/predict/TESS/307210830"
```

**Example Response:**
```json
{
  "mission": "TESS",
  "target_id": "307210830",
  "probability": 0.9137,
  "threshold": 0.4,
  "classification": "CONFIRMED",
  "used_features": {
    "pl_orbper": 3.6906759,
    "pl_trandurh": 1.107,
    "pl_trandep": 1657.0,
    "pl_rade": 1.36751,
    "pl_insol": 8.77401,
    "pl_eqt": 479.0,
    "st_teff": 3469.0,
    "st_logg": 4.9401,
    "st_rad": 0.31,
    "st_tmag": 9.41242
  }
}
```

**Response Fields:**
- `mission`: Mission name (TESS, KEPLER, K2)
- `target_id`: Target identifier
- `probability`: ML model confidence score (0.0 - 1.0)
- `threshold`: Decision threshold for classification
- `classification`: Either "CONFIRMED" or "FALSE_POSITIVE"
- `used_features`: Dictionary of features used in prediction

### 4. Get Prediction Features

#### `GET /api/v1/predict/{mission}/{target_id}/features`
Get the features that would be used for prediction without running the model.

**Parameters:**
- `mission` (string): Mission name
- `target_id` (string): Target identifier

**Example Response:**
```json
{
  "mission": "TESS",
  "target_id": "307210830",
  "features": {
    "pl_orbper": 3.6906759,
    "pl_trandurh": 1.107,
    "pl_trandep": 1657.0,
    "pl_rade": 1.36751,
    "pl_insol": 8.77401,
    "pl_eqt": 479.0,
    "st_teff": 3469.0,
    "st_logg": 4.9401,
    "st_rad": 0.31,
    "st_tmag": 9.41242
  },
  "feature_count": 10,
  "available_features": 10
}
```

### 5. Custom Prediction

#### `GET /api/v1/predict/{mission}/{target_id}/custom`
Make prediction with custom feature values (uses API features if none provided).

**Parameters:**
- `mission` (string): Mission name
- `target_id` (string): Target identifier
- `features` (optional): Custom feature dictionary

### 6. Models Status

#### `GET /api/v1/predict/models/status`
Get status of all available ML models.

**Example Response:**
```json
{
  "available_missions": ["TESS", "K2", "KEPLER"],
  "models": {
    "TESS": {
      "available": true,
      "features_count": 10,
      "threshold": 0.4,
      "model_type": "CalibratedClassifierCV"
    },
    "K2": {
      "available": true,
      "features_count": 12,
      "threshold": 0.6,
      "model_type": "CalibratedClassifierCV"
    },
    "KEPLER": {
      "available": true,
      "features_count": 11,
      "threshold": 0.4,
      "model_type": "CalibratedClassifierCV"
    }
  },
  "total_available": 3
}
```

---

## Feature Endpoints

### 7. Get Features by Mission

#### `GET /api/v1/features/{mission}/{target_id}`
Get detailed feature data for a specific target.

**Parameters:**
- `mission` (string): Mission name
- `target_id` (string): Target identifier

**Example Response:**
```json
{
  "mission": "TESS",
  "target_id": "307210830",
  "features": {
    "pl_orbper": 3.6906759,
    "pl_trandurh": 1.107,
    "pl_trandep": 1657.0,
    "pl_rade": 1.36751,
    "pl_insol": 8.77401,
    "pl_eqt": 479.0,
    "st_teff": 3469.0,
    "st_logg": 4.9401,
    "st_rad": 0.31,
    "st_tmag": 9.41242
  },
  "source": "NASA Exoplanet Archive",
  "last_updated": "2024-01-15T10:30:00Z"
}
```

---

## Lightcurve Endpoints

### 8. Get Lightcurve Data

#### `GET /api/v1/lightcurve/{mission}/{target_id}`
Get lightcurve data for a specific target.

**Parameters:**
- `mission` (string): Mission name
- `target_id` (string): Target identifier
- `sector` (optional, int): Specific sector for TESS data
- `quarter` (optional, int): Specific quarter for Kepler data
- `campaign` (optional, int): Specific campaign for K2 data

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/lightcurve/TESS/307210830?sector=1"
```

**Example Response:**
```json
{
  "mission": "TESS",
  "target_id": "307210830",
  "sector": 1,
  "data_points": 18000,
  "time_range": {
    "start": 1325.0,
    "end": 1352.0
  },
  "lightcurve": {
    "time": [1325.0, 1325.1, 1325.2, ...],
    "flux": [0.999, 1.001, 0.998, ...],
    "flux_err": [0.001, 0.001, 0.001, ...]
  },
  "metadata": {
    "cadence": "2-minute",
    "pipeline": "SPOC",
    "quality_flags": "applied"
  }
}
```

---

## Error Handling

### HTTP Status Codes

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (target not found)
- `422`: Validation Error
- `500`: Internal Server Error

### Common Error Responses

#### Target Not Found
```json
{
  "detail": "Target 999999999 not found in TESS mission",
  "status_code": 404
}
```

#### Invalid Mission
```json
{
  "detail": "Mission INVALID not supported. Available: ['TESS', 'K2', 'KEPLER']",
  "status_code": 400
}
```

#### Model Error
```json
{
  "detail": "Model prediction failed: insufficient features",
  "status_code": 500
}
```

---

## Rate Limiting & Caching

### Caching
- Prediction results are cached for 1 hour
- Feature data is cached for 6 hours
- Lightcurve data is cached for 24 hours

### Rate Limiting
Currently no rate limiting is implemented, but consider implementing client-side throttling for production use.

---

## Data Sources

### NASA Exoplanet Archive
- **TESS**: TOI (TESS Objects of Interest) catalog
- **Kepler**: KOI (Kepler Objects of Interest) catalog  
- **K2**: K2 confirmed planets catalog

### MAST (Mikulski Archive for Space Telescopes)
- Lightcurve data for all missions
- Target coordinates and metadata

---

## Frontend Integration Examples

### React/JavaScript Example

```javascript
// Predict exoplanet
async function predictExoplanet(mission, targetId) {
  try {
    const response = await fetch(
      `http://localhost:8000/api/v1/predict/${mission}/${targetId}`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Prediction failed:', error);
    throw error;
  }
}

// Get lightcurve data
async function getLightcurve(mission, targetId, options = {}) {
  const params = new URLSearchParams();
  
  if (options.sector) params.append('sector', options.sector);
  if (options.quarter) params.append('quarter', options.quarter);
  if (options.campaign) params.append('campaign', options.campaign);
  
  const url = `http://localhost:8000/api/v1/lightcurve/${mission}/${targetId}?${params}`;
  
  const response = await fetch(url);
  return response.json();
}

// Resolve target name
async function resolveTarget(targetName) {
  const response = await fetch(
    `http://localhost:8000/api/v1/resolve/${encodeURIComponent(targetName)}`
  );
  return response.json();
}
```

### Python Example

```python
import requests

class ExoScoutAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def predict_exoplanet(self, mission, target_id):
        """Get exoplanet prediction"""
        url = f"{self.base_url}/api/v1/predict/{mission}/{target_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_features(self, mission, target_id):
        """Get target features"""
        url = f"{self.base_url}/api/v1/features/{mission}/{target_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_lightcurve(self, mission, target_id, **kwargs):
        """Get lightcurve data"""
        url = f"{self.base_url}/api/v1/lightcurve/{mission}/{target_id}"
        response = requests.get(url, params=kwargs)
        response.raise_for_status()
        return response.json()

# Usage
api = ExoScoutAPI()
prediction = api.predict_exoplanet("TESS", "307210830")
print(f"Classification: {prediction['classification']}")
print(f"Probability: {prediction['probability']:.4f}")
```

---

## Development & Testing

### Interactive API Documentation
Visit `http://localhost:8000/docs` for Swagger UI documentation where you can test all endpoints interactively.

### Health Check
Always check `http://localhost:8000/health` to ensure the API is running before making requests.

### Example Test Commands

```bash
# Health check
curl http://localhost:8000/health

# Test prediction
curl "http://localhost:8000/api/v1/predict/TESS/307210830"

# Test with different missions
curl "http://localhost:8000/api/v1/predict/KEPLER/10666592"
curl "http://localhost:8000/api/v1/predict/K2/206103150"

# Get model status
curl "http://localhost:8000/api/v1/predict/models/status"


```

---

## Support & Contact

For technical issues or questions about the API, please refer to the project repository or contact the development team.

**API Version:** 1.0  
**Last Updated:** January 2024  
**FastAPI Version:** 0.104+  
**Python Version:** 3.9+