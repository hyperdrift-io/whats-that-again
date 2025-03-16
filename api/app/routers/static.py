"""
Static file router for the WhatsThatAgain API
"""

import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

# Path to the frontend build directory
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                           "..", "frontend", "dist")


@router.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """
    Serve the SPA (Single Page Application) frontend
    """
    # Check if the file exists
    file_path = os.path.join(FRONTEND_DIR, full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    # If file doesn't exist, serve index.html for SPA routing
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    # If index.html doesn't exist, return 404
    raise HTTPException(status_code=404, detail="File not found")
