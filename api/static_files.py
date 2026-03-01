"""
静态文件处理模块
支持从 PyInstaller 嵌入的资源中加载前端文件
"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_resource_path(relative_path: str) -> Path:
    """
    获取资源文件的绝对路径
    支持 PyInstaller 打包后的路径解析

    Args:
        relative_path: 相对于项目根目录的路径

    Returns:
        资源文件的绝对路径
    """
    # 检查是否在 PyInstaller 打包环境中
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 创建的临时目录
        base_path = Path(sys._MEIPASS)
    else:
        # 正常开发环境
        # 获取当前文件所在目录 (api/)
        current_dir = Path(__file__).parent
        # 项目根目录
        base_path = current_dir.parent

    return base_path / relative_path


def get_frontend_path() -> Optional[Path]:
    """
    获取前端文件目录

    Returns:
        前端目录路径，如果不存在则返回 None
    """
    # 首先尝试 PyInstaller 嵌入的路径
    frontend_path = get_resource_path("frontend")

    if frontend_path.exists():
        return frontend_path

    # 回退到开发环境路径
    current_dir = Path(__file__).parent
    dev_frontend = current_dir.parent / "frontend"

    if dev_frontend.exists():
        return dev_frontend

    return None


def get_index_html() -> Optional[Path]:
    """
    获取 index.html 文件路径

    Returns:
        index.html 文件路径，如果不存在则返回 None
    """
    frontend_path = get_frontend_path()

    if frontend_path:
        index_path = frontend_path / "index.html"
        if index_path.exists():
            return index_path

    # 直接尝试 PyInstaller 路径
    direct_path = get_resource_path("frontend/index.html")
    if direct_path.exists():
        return direct_path

    return None


def read_file_content(file_path: Path) -> str:
    """
    读取文件内容

    Args:
        file_path: 文件路径

    Returns:
        文件内容字符串
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


# 测试代码
if __name__ == "__main__":
    print("测试静态文件处理模块...")
    print()

    print(f"是否在 PyInstaller 环境: {hasattr(sys, '_MEIPASS')}")
    print(f"资源根路径: {get_resource_path('.')}")
    print()

    frontend = get_frontend_path()
    print(f"前端目录: {frontend}")

    index = get_index_html()
    print(f"index.html: {index}")

    if index:
        print(f"\nindex.html 存在: {index.exists()}")
        if index.exists():
            content = read_file_content(index)
            print(f"文件大小: {len(content)} 字符")
