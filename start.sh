#!/bin/bash
set -e
echo "Starting process at $(date)"

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r api/requirements.txt || { echo "pip install failed"; exit 1; }

# Build frontend
echo "Building frontend with Bun..."
cd frontend || { echo "cd frontend failed"; exit 1; }
bun install || { echo "bun install failed"; exit 1; }
bun run build || { echo "bun run build failed"; exit 1; }
if [ ! -d "dist" ]; then
    echo "Error: dist/ not found after build"
    exit 1
fi
cd ..

# Start the server
echo "Starting Uvicorn server..."
cd api
exec uvicorn main:app --host 0.0.0.0 --port $PORT