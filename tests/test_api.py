#!/usr/bin/env python3
"""Test script for the Pixel Art Refiner API."""

import requests
import os
import tempfile
from PIL import Image
import numpy as np


def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check endpoint...")
    response = requests.get("http://localhost:8000/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "version" in data
    assert "service" in data
    print("✅ Health check passed")


def test_process_image():
    """Test the image processing endpoint with a simple test image."""
    print("Testing image processing endpoint...")

    # Create a simple test image (32x32 pixel with black and white squares)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img = Image.new('RGB', (32, 32), color='white')
        pixels = img.load()

        for i in range(32):
            for j in range(32):
                if (i // 8 + j // 8) % 2 == 0:
                    pixels[i, j] = (0, 0, 0)

        img.save(tmp, format='PNG')
        test_image_path = tmp.name

    try:
        # Send test image to API
        with open(test_image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'sample_method': 'center',
                'min_size': 4.0,
                'peak_width': 6,
                'refine_intensity': 0.25,
                'fix_square': True
            }

            response = requests.post(
                "http://localhost:8000/api/v1/process",
                files=files,
                data=data
            )

        assert response.status_code == 200

        result = response.json()
        print("✅ Image processing response:")
        print(f"  Status: {result.get('status')}")
        print(f"  Request ID: {result.get('request_id')}")
        print(f"  Original size: {result.get('original_size')}")
        print(f"  Refined size: {result.get('refined_size')}")
        print(f"  Pixel size: {result.get('pixel_size')}")
        print(f"  Download URL: {result.get('download_url')}")

        # Check if the download URL is accessible
        download_url = result.get('download_url')
        assert download_url is not None

        download_response = requests.get(f"http://localhost:8000{download_url}")
        assert download_response.status_code == 200
        assert download_response.headers.get('content-type') == 'image/png'
        print("✅ Download endpoint working correctly")

    finally:
        # Clean up test image file
        os.unlink(test_image_path)


def test_download_invalid_file():
    """Test download endpoint with invalid filename."""
    print("Testing download endpoint with invalid filename...")

    response = requests.get("http://localhost:8000/api/v1/download/invalid_file.png")
    assert response.status_code == 404
    assert "File not found" in response.json().get("detail")
    print("✅ Invalid file download handled correctly")


def run_all_tests():
    """Run all test cases."""
    print("=" * 60)
    print("Pixel Art Refiner API Tests")
    print("=" * 60)

    tests = [
        test_health_check,
        test_process_image,
        test_download_invalid_file
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            print(traceback.format_exc())
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        raise Exception(f"{failed} tests failed")


if __name__ == "__main__":
    try:
        run_all_tests()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        import sys
        sys.exit(1)
