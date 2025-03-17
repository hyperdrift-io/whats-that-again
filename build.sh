#!/bin/bash
set -e
echo "Starting build process at $(date)"
pip install -r api/requirements.txt
cd frontend
bun install
bun run build
echo "Build complete at $(date)"
ls -la
exit 0