#!/usr/bin/env python3
"""
直接测试 detect_grid_scale 函数的宽高比功能
"""

import cv2
import numpy as np
import sys
from pathlib import Path
import importlib.util

# 直接从源文件导入
spec = importlib.util.spec_from_file_location(
    "perfect_pixel",
    str(Path(__file__).parent / "perfectPixel" / "src" / "perfect_pixel" / "perfect_pixel.py")
)
perfect_pixel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(perfect_pixel)

detect_grid_scale = perfect_pixel.detect_grid_scale
estimate_grid_fft = perfect_pixel.estimate_grid_fft
estimate_grid_gradient = perfect_pixel.estimate_grid_gradient
get_perfect_pixel = perfect_pixel.get_perfect_pixel

def test_grid_scale():
    # 读取测试图片
    img_path = Path(__file__).parent / "img" / "test_img.png"
    bgr = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    H, W = rgb.shape[:2]
    original_ratio = W / H

    print("=" * 70)
    print(f"📸 原始图片: {W} × {H} (宽高比: {original_ratio:.3f})")
    print("=" * 70)

    # 测试完整流程 - normalize_ratio=True
    print("\n🧪 测试 1: normalize_ratio=True (启用归一化)")
    print("-" * 50)
    refined_w1, refined_h1, output_img1 = get_perfect_pixel(
        rgb,
        sample_method="center",
        min_size=4.0,
        peak_width=6,
        refine_intensity=0.25,
        fix_square=False,
        normalize_ratio=True
    )

    if refined_w1 and refined_h1:
        ratio1 = refined_w1 / refined_h1
        diff1 = abs(ratio1 - original_ratio) / original_ratio * 100
        print(f"   输出尺寸: {refined_w1} × {refined_h1}")
        print(f"   宽高比: {ratio1:.3f} (原始: {original_ratio:.3f})")
        print(f"   与原始比例差异: {diff1:.2f}%")
        cv2.imwrite(str(Path(__file__).parent / "output_normalize_true.png"),
                    cv2.cvtColor(output_img1, cv2.COLOR_RGB2BGR))

    # 测试完整流程 - normalize_ratio=False
    print("\n🧪 测试 2: normalize_ratio=False (禁用归一化，保持原始比例)")
    print("-" * 50)
    refined_w2, refined_h2, output_img2 = get_perfect_pixel(
        rgb,
        sample_method="center",
        min_size=4.0,
        peak_width=6,
        refine_intensity=0.25,
        fix_square=False,
        normalize_ratio=False
    )

    if refined_w2 and refined_h2:
        ratio2 = refined_w2 / refined_h2
        diff2 = abs(ratio2 - original_ratio) / original_ratio * 100
        print(f"   输出尺寸: {refined_w2} × {refined_h2}")
        print(f"   宽高比: {ratio2:.3f} (原始: {original_ratio:.3f})")
        print(f"   与原始比例差异: {diff2:.2f}%")
        cv2.imwrite(str(Path(__file__).parent / "output_normalize_false.png"),
                    cv2.cvtColor(output_img2, cv2.COLOR_RGB2BGR))

    print("\n" + "=" * 70)
    print("💡 总结:")
    print("=" * 70)
    if refined_w1 and refined_h1 and refined_w2 and refined_h2:
        diff1 = abs(refined_w1/refined_h1 - original_ratio) / original_ratio * 100
        diff2 = abs(refined_w2/refined_h2 - original_ratio) / original_ratio * 100

        print(f"\n   normalize_ratio=True:  比例差异 {diff1:.2f}%")
        print(f"   normalize_ratio=False: 比例差异 {diff2:.2f}%")

        if diff2 < diff1:
            print("\n   ✅ normalize_ratio=False 更好地保持了原始图片的宽高比！")
        else:
            print("\n   ⚠️ 两种模式的差异相似")

    print("\n   输出文件:")
    print(f"   - output_normalize_true.png (normalize_ratio=True)")
    print(f"   - output_normalize_false.png (normalize_ratio=False)")

if __name__ == "__main__":
    test_grid_scale()
