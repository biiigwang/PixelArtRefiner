#!/usr/bin/env python3
"""
PixelArtRefiner 打包脚本
使用 PyInstaller 打包为可执行程序
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# 项目路径
PROJECT_ROOT = Path(__file__).parent
API_DIR = PROJECT_ROOT / "api"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
PERFECT_PIXEL_DIR = PROJECT_ROOT / "perfectPixel"
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"


def clean_build():
    """清理之前的构建文件"""
    print("🧹 清理构建目录...")
    for dir_path in [BUILD_DIR, DIST_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   已删除: {dir_path}")


def run_pyinstaller():
    """直接使用 PyInstaller 命令行"""
    print("📦 开始打包...")

    # macOS 使用冒号分隔
    frontend_data = f"{FRONTEND_DIR}:frontend"
    perfectpixel_data = f"{PERFECT_PIXEL_DIR / 'src' / 'perfect_pixel'}:perfect_pixel"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=PixelArtRefiner",
        "--onedir",  # 创建目录而不是单文件
        "--console",  # 显示控制台窗口
        "--clean",
        "--noconfirm",
        f"--add-data={frontend_data}",
        f"--add-data={perfectpixel_data}",
        "--hidden-import=uvicorn",
        "--hidden-import=fastapi",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--hidden-import=python_multipart",
        "--collect-all=uvicorn",
        "--collect-all=fastapi",
        str(API_DIR / "main.py"),
    ]

    print(f"执行命令: {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=False)

    return result.returncode == 0


def build():
    """执行打包构建"""
    print("=" * 70)
    print("🚀 PixelArtRefiner 打包脚本")
    print("=" * 70)

    # 清理旧构建
    clean_build()

    # 执行打包
    success = run_pyinstaller()

    if not success:
        print("❌ 构建失败！")
        sys.exit(1)

    print()
    print("=" * 70)
    print("✅ 构建成功！")
    print(f"📁 输出目录: {DIST_DIR / 'PixelArtRefiner'}")
    print("=" * 70)


if __name__ == "__main__":
    build()
