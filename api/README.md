# WhatsThatAgain API

This is the FastAPI backend for the WhatsThatAgain application.

## Project Structure

```
api/
├── app/                    # Main application package
│   ├── __init__.py         # Package initialization
│   ├── main.py             # FastAPI application instance
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   └── schemas.py      # Pydantic models
│   ├── routers/            # API endpoints
│   │   ├── __init__.py
│   │   ├── search.py       # Search endpoint
│   │   └── static.py       # Static file serving
│   ├── services/           # Business logic
│   │   ├── __init__.py
│   │   ├── ai_service.py   # AI interaction logic
│   │   └── usage_service.py # Usage tracking
│   └── utils/              # Utility functions
│       └── __init__.py
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── usage_count.txt         # Usage tracking file
```

## Running the API

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the API:
```
python main.py
```

Or with uvicorn directly:
```
uvicorn main:app --reload
```

## API Endpoints

- `GET /`: Root endpoint with API information
- `POST /search`: Main search endpoint for querying the AI
- `GET /{path}`: Serves static files from the frontend build

## Environment Variables

Create a `.env` file with:
```
ANTHROPIC_API_KEY=your-key-here
``` 