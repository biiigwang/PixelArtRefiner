#!/usr/bin/env python3
"""
调试宽高比问题
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

get_perfect_pixel = perfect_pixel.get_perfect_pixel

def debug_test():
    img_path = Path(__file__).parent / "img" / "test_img.png"
    bgr = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    H, W = rgb.shape[:2]
    original_ratio = W / H

    print("=" * 70)
    print(f"原始图片: {W} × {H}, 宽高比: {original_ratio:.4f}")
    print("=" * 70)

    # 测试 normalize_ratio=False
    print("\n测试: normalize_ratio=False")
    print("-" * 50)

    w, h, img = get_perfect_pixel(
        rgb,
        sample_method="center",
        min_size=4.0,
        peak_width=6,
        refine_intensity=0.25,
        fix_square=False,
        normalize_ratio=False
    )

    if w and h:
        actual_ratio = w / h
        diff = abs(actual_ratio - original_ratio) / original_ratio * 100
        print(f"\n输出尺寸: {w} × {h}")
        print(f"实际宽高比: {actual_ratio:.4f}")
        print(f"原始宽高比: {original_ratio:.4f}")
        print(f"差异: {diff:.2f}%")

        if diff < 1.0:
            print("\n✅ 成功保持原始宽高比！")
        else:
            print("\n❌ 宽高比偏差较大")
            print("\n可能原因：")
            print("1. fix_square=True 强制修改了比例")
            print("2. refine_grids 调整了网格线位置")
            print("3. 采样后的图像被裁剪或调整")

if __name__ == "__main__":
    debug_test()
