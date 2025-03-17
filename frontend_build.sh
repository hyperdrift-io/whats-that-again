#!/bin/bash
set -e
echo "Building frontend with Bun at $(date)"
cd frontend || { echo "cd frontend failed"; exit 1; }
bun install || { echo "bun install failed"; exit 1; }
bun run build || { echo "bun run build failed"; exit 1; }
echo "Frontend build complete at $(date)"
ls -la
if [ -d "dist" ]; then
    echo "Frontend build output found in dist/"
else
    echo "Error: dist/ directory not found"
    exit 1
fi
exit 0