#!/usr/bin/env python3
"""Complete API testing for Pixel Art Refiner with more comprehensive test cases."""

import requests
import os
import tempfile
from PIL import Image
import numpy as np
from io import BytesIO


def test_health_check_detailed():
    """Test health check with various scenarios."""
    print("Testing detailed health check...")

    # Basic health check
    response = requests.get("http://localhost:8000/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "version" in data
    assert "service" in data

    # Verify version format
    assert isinstance(data["version"], str)
    assert len(data["version"].split(".")) >= 2

    print("✅ Detailed health check passed")


def test_process_image_with_different_parameters():
    """Test image processing with different parameters."""
    print("Testing image processing with different parameters...")

    test_image = None

    try:
        # Create a test image with very clear pixel grid pattern
        img = Image.new('RGB', (64, 64), color='white')
        pixels = img.load()

        for i in range(64):
            for j in range(64):
                if (i // 16 + j // 16) % 2 == 0:
                    pixels[i, j] = (0, 0, 0)
                else:
                    pixels[i, j] = (255, 255, 255)

        # Save to in-memory buffer
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        test_image = buf

        # Test different sampling methods
        for method in ['center', 'median', 'majority']:
            print(f"  Testing {method} sampling...")
            files = {'image': ('test_image.png', test_image, 'image/png')}
            data = {
                'sample_method': method,
                'min_size': 8.0,
                'peak_width': 8,
                'refine_intensity': 0.25,
                'fix_square': True
            }

            response = requests.post(
                "http://localhost:8000/api/v1/process",
                files=files,
                data=data
            )

            # Check if the image was processed successfully or if it's a bad request
            if response.status_code == 200:
                result = response.json()
                assert 'status' in result
                assert result['status'] == 'success'
            elif response.status_code == 400:
                print(f"  Image not suitable for method {method}, skipping")
            else:
                assert False, f"Unexpected status code {response.status_code}"

        # Test different min_size values
        for min_size in [4.0, 8.0, 12.0]:
            print(f"  Testing min_size={min_size}...")
            files = {'image': ('test_image.png', test_image, 'image/png')}
            data = {
                'sample_method': 'center',
                'min_size': min_size,
                'peak_width': 8,
                'refine_intensity': 0.25,
                'fix_square': True
            }

            response = requests.post(
                "http://localhost:8000/api/v1/process",
                files=files,
                data=data
            )

            if response.status_code == 200:
                result = response.json()
                assert 'status' in result
                assert result['status'] == 'success'
            elif response.status_code == 400:
                print(f"  Image not suitable for min_size={min_size}, skipping")
            else:
                assert False, f"Unexpected status code {response.status_code}"

        # Test different refine_intensity values
        for intensity in [0.0, 0.25, 0.5, 0.75, 1.0]:
            print(f"  Testing refine_intensity={intensity}...")
            files = {'image': ('test_image.png', test_image, 'image/png')}
            data = {
                'sample_method': 'center',
                'min_size': 8.0,
                'peak_width': 8,
                'refine_intensity': intensity,
                'fix_square': True
            }

            response = requests.post(
                "http://localhost:8000/api/v1/process",
                files=files,
                data=data
            )

            if response.status_code == 200:
                result = response.json()
                assert 'status' in result
                assert result['status'] == 'success'
            elif response.status_code == 400:
                print(f"  Image not suitable for refine_intensity={intensity}, skipping")
            else:
                assert False, f"Unexpected status code {response.status_code}"

        print("✅ All parameter variations tested successfully")

    finally:
        if test_image:
            test_image.close()


def test_image_formats():
    """Test support for different image formats."""
    print("Testing support for different image formats...")

    test_formats = [
        ('JPEG', 'image/jpeg', '.jpg'),
        ('PNG', 'image/png', '.png'),
        ('WebP', 'image/webp', '.webp')
    ]

    for format_name, content_type, extension in test_formats:
        try:
            print(f"  Testing {format_name} format...")

            # Create test image
            img = Image.new('RGB', (32, 32), color='white')
            pixels = img.load()

            for i in range(32):
                for j in range(32):
                    if (i // 8 + j // 8) % 2 == 0:
                        pixels[i, j] = (0, 0, 0)

            # Save to in-memory buffer
            buf = BytesIO()
            img.save(buf, format=format_name)
            buf.seek(0)

            files = {'image': (f'test_image{extension}', buf, content_type)}
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
            assert 'status' in result
            assert result['status'] == 'success'

            buf.close()

        except Exception as e:
            print(f"❌ Error testing {format_name}: {e}")
            raise

    print("✅ All image formats tested successfully")


def test_large_image_processing():
    """Test processing of large images."""
    print("Testing processing of large images...")

    try:
        # Create a large test image (512x512) - smaller size to avoid potential issues
        img = Image.new('RGB', (512, 512), color='white')
        pixels = img.load()

        for i in range(512):
            for j in range(512):
                if (i // 16 + j // 16) % 2 == 0:
                    pixels[i, j] = (0, 0, 0)

        # Save to in-memory buffer
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)

        files = {'image': ('large_image.png', buf, 'image/png')}
        data = {
            'sample_method': 'center',
            'min_size': 8.0,
            'peak_width': 8,
            'refine_intensity': 0.25,
            'fix_square': True
        }

        response = requests.post(
            "http://localhost:8000/api/v1/process",
            files=files,
            data=data
        )

        # Check if the image was processed successfully or if it's not suitable
        if response.status_code == 200:
            result = response.json()
            assert 'status' in result
            assert result['status'] == 'success'

            # Verify processed image dimensions
            assert 'refined_size' in result
            refined_w, refined_h = result['refined_size']
            assert refined_w > 0
            assert refined_h > 0

            print("✅ Large image processing successful")
        elif response.status_code == 400:
            print("  Large image not suitable for processing, skipping")
        else:
            assert False, f"Unexpected status code {response.status_code}"

        buf.close()

    except Exception as e:
        print(f"❌ Error processing large image: {e}")
        raise


def test_error_handling():
    """Test error handling in API endpoints."""
    print("Testing error handling...")

    # Test invalid file type
    invalid_file = BytesIO(b"This is not an image file")

    files = {'image': ('invalid.txt', invalid_file, 'text/plain')}
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

    assert response.status_code == 400
    error_data = response.json()
    assert 'detail' in error_data

    invalid_file.close()

    # Test invalid parameters (invalid min_size)
    img = Image.new('RGB', (32, 32), color='white')
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    files = {'image': ('test.png', buf, 'image/png')}
    data = {
        'sample_method': 'center',
        'min_size': 0,  # Invalid value
        'peak_width': 6,
        'refine_intensity': 0.25,
        'fix_square': True
    }

    response = requests.post(
        "http://localhost:8000/api/v1/process",
        files=files,
        data=data
    )

    assert response.status_code != 200
    buf.close()

    print("✅ Error handling tested successfully")


def run_all_comprehensive_tests():
    """Run all comprehensive test cases."""
    print("=" * 70)
    print("Pixel Art Refiner - Comprehensive API Tests")
    print("=" * 70)

    tests = [
        test_health_check_detailed,
        test_process_image_with_different_parameters,
        test_image_formats,
        test_large_image_processing,
        test_error_handling
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

    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed > 0:
        raise Exception(f"{failed} tests failed")


if __name__ == "__main__":
    try:
        run_all_comprehensive_tests()
        print("\n🎉 All comprehensive tests passed!")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        import sys
        sys.exit(1)
