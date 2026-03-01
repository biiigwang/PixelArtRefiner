#!/usr/bin/env python3
"""
最终测试宽高比功能
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

def final_test():
    img_path = Path(__file__).parent / "img" / "test_img.png"
    bgr = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    H, W = rgb.shape[:2]
    original_ratio = W / H

    print("=" * 70)
    print("最终测试：宽高比保持功能")
    print("=" * 70)
    print(f"\n原始图片: {W} × {H}")
    print(f"原始宽高比: {original_ratio:.4f}")

    # 测试两种模式
    results = []
    for mode_name, normalize in [("启用归一化 (True)", True), ("禁用归一化/保持原始比例 (False)", False)]:
        print(f"\n{'-' * 70}")
        print(f"测试: {mode_name}")
        print(f"{'-' * 70}")

        w, h, img = get_perfect_pixel(
            rgb,
            sample_method="center",
            min_size=4.0,
            peak_width=6,
            refine_intensity=0.25,
            fix_square=False,  # 禁用fix_square以便准确测试
            normalize_ratio=normalize
        )

        if w and h:
            actual_ratio = w / h
            diff = abs(actual_ratio - original_ratio) / original_ratio * 100

            print(f"\n输出尺寸: {w} × {h}")
            print(f"实际宽高比: {actual_ratio:.4f}")
            print(f"目标宽高比: {original_ratio:.4f}")
            print(f"差异: {diff:.2f}%")

            if diff < 1.0:
                print("✅ 成功保持原始宽高比！")
                status = "✅ 通过"
            elif diff < 5.0:
                print("⚠️  宽高比有一定偏差")
                status = "⚠️  偏差"
            else:
                print("❌ 宽高比偏差较大")
                status = "❌ 失败"

            results.append({
                'mode': mode_name,
                'normalize': normalize,
                'output_size': (w, h),
                'actual_ratio': actual_ratio,
                'target_ratio': original_ratio,
                'diff': diff,
                'status': status
            })

    # 总结
    print(f"\n{'=' * 70}")
    print("测试结果总结")
    print(f"{'=' * 70}")

    for r in results:
        print(f"\n{r['mode']}:")
        print(f"  输出尺寸: {r['output_size'][0]} × {r['output_size'][1]}")
        print(f"  实际比例: {r['actual_ratio']:.4f}")
        print(f"  目标比例: {r['target_ratio']:.4f}")
        print(f"  偏差: {r['diff']:.2f}%")
        print(f"  结果: {r['status']}")

    print(f"\n{'=' * 70}")

    # 判断总体结果
    false_result = [r for r in results if not r['normalize']]
    if false_result and false_result[0]['diff'] < 1.0:
        print("✅ 测试通过！normalize_ratio=False 成功保持原始宽高比。")
        return True
    else:
        print("❌ 测试未通过。normalize_ratio=False 未能保持原始宽高比。")
        return False

if __name__ == "__main__":
    success = final_test()
    sys.exit(0 if success else 1)
