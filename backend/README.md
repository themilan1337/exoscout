# ExoScout Backend

AI-powered backend for exoplanet detection using NASA data (NASA Space Apps Challenge 2025).

## Quick Start

### Option 1: Virtual Environment

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

### Option 2: Docker

1. Build the Docker image:
```bash
docker build -t exoscout-backend .
```

2. Run the container:
```bash
docker run -p 8000:8000 exoscout-backend
```

## API Endpoints

- **Root**: `GET /` - Returns welcome message
- **Health Check**: `GET /health` - Returns service status

## Example Requests

```bash
# Check if service is running
curl http://127.0.0.1:8000/

# Health check
curl http://127.0.0.1:8000/health
```

## API Documentation

Once running, visit:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Project Structure

```
backend/
├── main.py              # FastAPI entrypoint
├── routers/             # API route modules
│   └── health.py        # Health check endpoints
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
└── README.md           # This file
```