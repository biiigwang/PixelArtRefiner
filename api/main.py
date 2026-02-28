"""
Pixel Art Refiner - Main Application
FastAPI-based API for processing pixel art images using Perfect Pixel algorithm.

Author: biiigwang
Date: 2026-02-26
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import tempfile
import cv2
import numpy as np
import sys
from pathlib import Path

# Add project root and perfect-pixel src directory to Python path for module resolution
PROJECT_ROOT = Path(__file__).parent.parent
SUBMODULE_SRC_DIR = PROJECT_ROOT / "perfectPixel" / "src"

if str(SUBMODULE_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SUBMODULE_SRC_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(1, str(PROJECT_ROOT))

import uuid

try:
    from perfect_pixel import get_perfect_pixel

    import perfect_pixel

    print(f"✅ Perfect Pixel module imported from: {perfect_pixel.__file__}")
except Exception as e:
    print(f"❌ Import error: {e}")
    print(f"Python path: {sys.path}")
    raise

# Create application instance
app = FastAPI(
    title="Pixel Art Refiner API",
    description="API service for processing pixel art images using Perfect Pixel algorithm",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
app.mount(
    "/app",
    StaticFiles(
        directory=str(PROJECT_ROOT / "frontend"), html=True
    ),
    name="frontend",
)

# Create temporary directories for file handling
UPLOAD_DIR = tempfile.mkdtemp(prefix="pixel-art-refiner-uploads-")
RESULT_DIR = tempfile.mkdtemp(prefix="pixel-art-refiner-results-")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up temporary directories on shutdown"""
    import shutil

    try:
        if os.path.exists(UPLOAD_DIR):
            shutil.rmtree(UPLOAD_DIR)
        if os.path.exists(RESULT_DIR):
            shutil.rmtree(RESULT_DIR)
    except Exception as e:
        print(f"Error during cleanup: {e}")


# Health check endpoint
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0", "service": "Pixel Art Refiner API"}


# Image processing endpoint
@app.post("/api/v1/process")
async def process_image(
    image: UploadFile = File(...),
    sample_method: str = Form("center"),
    grid_size: str = Form(None),
    min_size: float = Form(..., ge=1.0, le=20.0),
    peak_width: int = Form(..., ge=1, le=20),
    refine_intensity: float = Form(..., ge=0.0, le=1.0),
    fix_square: bool = Form(True),
):
    """
    Process an uploaded image using Perfect Pixel algorithm.

    Args:
        image: Uploaded image file
        sample_method: Sampling method - "center", "median", or "majority"
        grid_size: Manual grid size as JSON string "[width, height]"
        min_size: Minimum pixel size to consider valid
        peak_width: Minimum peak width for peak detection
        refine_intensity: Intensity for grid line refinement
        fix_square: Whether to enforce output to be square when almost square

    Returns:
        Dictionary containing processing results and download URL
    """
    # Save uploaded file temporarily
    filename = str(uuid.uuid4())
    file_ext = os.path.splitext(image.filename)[1].lower() if image.filename else ".png"
    temp_path = os.path.join(UPLOAD_DIR, f"{filename}{file_ext}")

    with open(temp_path, "wb") as buffer:
        buffer.write(await image.read())

    # Read and preprocess image
    bgr = cv2.imread(temp_path, cv2.IMREAD_COLOR)

    if bgr is None:
        raise HTTPException(status_code=400, detail="Failed to read image file")

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    # Process grid size if provided
    grid_size_tuple = None
    if grid_size:
        try:
            import json

            grid_size_tuple = tuple(map(int, json.loads(grid_size)))
            if (
                len(grid_size_tuple) != 2
                or grid_size_tuple[0] <= 0
                or grid_size_tuple[1] <= 0
            ):
                raise ValueError("Invalid grid size")
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid grid size format: {str(e)}"
            )

    # Process image
    try:
        refined_width, refined_height, output_image = get_perfect_pixel(
            rgb,
            sample_method=sample_method,
            grid_size=grid_size_tuple,
            min_size=min_size,
            peak_width=peak_width,
            refine_intensity=refine_intensity,
            fix_square=fix_square,
        )

        if refined_width is None or refined_height is None or output_image is None:
            raise HTTPException(
                status_code=400, detail="无法确定图像的像素网格大小。请尝试调整 min_size 参数或使用更清晰的像素风格图像。"
            )

        # Save output
        output_filename = f"{filename}_result.png"
        output_path = os.path.join(RESULT_DIR, output_filename)
        output_bgr = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, output_bgr)

        # Calculate pixel size
        original_h, original_w = rgb.shape[:2]
        pixel_size = round(
            (original_w / refined_width + original_h / refined_height) / 2, 2
        )

        # Return results
        return {
            "status": "success",
            "request_id": filename,
            "original_size": [original_w, original_h],
            "refined_size": [refined_width, refined_height],
            "pixel_size": pixel_size,
            "download_url": f"/api/v1/download/{output_filename}",
            "processing_time": None,  # TODO: Calculate actual processing time
        }
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="无法确定图像的像素网格大小。请尝试调整 min_size 参数或使用更清晰的像素风格图像。"
        )


# Download endpoint
@app.get("/api/v1/download/{filename}")
async def download_result(filename: str):
    """
    Download processed result image.

    Args:
        filename: Filename of the processed image
    """
    file_path = os.path.join(RESULT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type="image/png", filename=filename)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - provides basic API information"""
    return {
        "service": "Pixel Art Refiner API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
