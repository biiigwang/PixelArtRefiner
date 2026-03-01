# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pixel Art Refiner is a web service that converts AI-generated "fake" pixel art into grid-aligned pixel-perfect artwork using the Perfect Pixel algorithm (FFT-based spectrum analysis for pixel grid detection).

## Environment

**Always use conda environment `perfectpixel`:**
```bash
conda activate perfectpixel
```

## Common Commands

### Development
```bash
# Install dependencies (in conda env)
pip install -r requirements.txt

# Run the API server
python api/main.py

# Run tests
python tests/test_api.py
```

### Building
```bash
# Package as macOS app using PyInstaller
python build.py
```

### API Endpoints
- Web UI: http://localhost:8000/app
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

## Architecture

### Core Components
- **`api/main.py`**: FastAPI application - handles HTTP requests, image upload, and calls the Perfect Pixel algorithm
- **`perfectPixel/src/perfect_pixel/perfect_pixel.py`**: Core algorithm - FFT-based pixel grid detection and refinement
- **`frontend/index.html`**: Simple Bootstrap-based web UI for image upload
- **`tests/test_api.py`**: Integration tests for API endpoints

### Processing Flow
1. User uploads image via Web UI or API
2. API reads image using OpenCV (`cv2.imread`)
3. Converts BGR to RGB
4. Calls `get_perfect_pixel()` from perfectPixel submodule
5. Returns refined image with detected grid dimensions

### Algorithm Details
The Perfect Pixel algorithm uses FFT (Fast Fourier Transform) to detect periodic patterns in images:
1. Compute 2D FFT of grayscale image
2. Detect peaks in frequency spectrum to find pixel grid periodicity
3. Use projection method to find exact grid lines
4. Refine grid using specified intensity
5. Resample image to match detected grid size

## Key Parameters
- `sample_method`: "center" | "median" | "majority" - how to sample pixel colors
- `min_size`: Minimum pixel size (1.0-20.0)
- `peak_width`: FFT peak width for detection (1-20)
- `refine_intensity`: Grid refinement strength (0.0-1.0)
- `fix_square`: Force square output when nearly square

## Submodule
The project uses a git submodule for the Perfect Pixel algorithm:
```bash
# Update submodule
git submodule update --init --recursive
```
