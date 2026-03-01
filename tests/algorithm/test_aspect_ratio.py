#!/usr/bin/env python3
"""
测试宽高比归一化功能的脚本
"""

import cv2
import numpy as np
import sys
from pathlib import Path

# Add project root and perfect-pixel src directory to Python path
PROJECT_ROOT = Path(__file__).parent
SUBMODULE_SRC_DIR = PROJECT_ROOT / "perfectPixel" / "src"

if str(SUBMODULE_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SUBMODULE_SRC_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(1, str(PROJECT_ROOT))

from perfect_pixel import get_perfect_pixel

def test_aspect_ratio():
    # 读取测试图片
    img_path = PROJECT_ROOT / "img" / "test_img.png"
    bgr = cv2.imread(str(img_path), cv2.IMREAD_COLOR)

    if bgr is None:
        print(f"❌ 无法读取图片: {img_path}")
        return

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    original_h, original_w = rgb.shape[:2]
    original_ratio = original_w / original_h

    print(f"📸 原始图片: {original_w} × {original_h} (宽高比: {original_ratio:.3f})")
    print("-" * 70)

    # 测试 1: 启用宽高比归一化
    print("\n🧪 测试 1: 启用宽高比归一化 (normalize_ratio=True)")
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
        print(f"   输出尺寸: {refined_w1} × {refined_h1} (宽高比: {ratio1:.3f})")
        print(f"   与原比例差异: {abs(ratio1 - original_ratio) / original_ratio * 100:.2f}%")
        cv2.imwrite(str(PROJECT_ROOT / "output_with_normalization.png"),
                    cv2.cvtColor(output_img1, cv2.COLOR_RGB2BGR))

    # 测试 2: 禁用宽高比归一化
    print("\n🧪 测试 2: 禁用宽高比归一化 (normalize_ratio=False)")
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
        print(f"   输出尺寸: {refined_w2} × {refined_h2} (宽高比: {ratio2:.3f})")
        print(f"   与原比例差异: {abs(ratio2 - original_ratio) / original_ratio * 100:.2f}%")
        cv2.imwrite(str(PROJECT_ROOT / "output_without_normalization.png"),
                    cv2.cvtColor(output_img2, cv2.COLOR_RGB2BGR))

    print("-" * 70)
    print("\n✅ 测试完成！")
    print("   结果已保存到:")
    print(f"   - {PROJECT_ROOT / 'output_with_normalization.png'}")
    print(f"   - {PROJECT_ROOT / 'output_without_normalization.png'}")

if __name__ == "__main__":
    test_aspect_ratio()
