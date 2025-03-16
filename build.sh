#!/bin/bash

# Exit on any error
set -e

echo "Installing backend dependencies..."
pip install -r api/requirements.txt

echo "Building frontend with Bun..."
cd frontend
bun install
bun run build

echo "Build complete. Listing frontend directory contents..."
ls -la