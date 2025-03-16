"""
WhatsThatAgain - FastAPI Main Application
Helps you remember things that are on the tip of your tongue by directly querying AI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers directly
from app.routers.search import router as search_router
from app.routers.static import router as static_router

# Create FastAPI app
app = FastAPI(
    title="WhatsThatAgain API",
    description="API for the WhatsThatAgain application"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search_router, tags=["search"])
app.include_router(static_router, tags=["static"])

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - redirects to docs
    """
    return {
        "message": "Welcome to WhatsThatAgain API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
