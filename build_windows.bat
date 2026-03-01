@echo off
REM PixelArtRefiner Windows 打包脚本
REM 在 Windows 环境中运行此脚本

echo ============================================================
echo PixelArtRefiner Windows 打包脚本
echo ============================================================

REM 激活 conda 环境（如果需要）
REM conda activate perfectpixel

REM 清理旧的构建
echo.
echo [1/3] 清理构建目录...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo    完成清理

echo.
echo [2/3] 开始打包...
echo.

REM 运行 PyInstaller
python -m PyInstaller --name=PixelArtRefiner --onedir --console --clean --noconfirm --add-data="frontend;frontend" --add-data="perfectPixel\src\perfect_pixel;perfect_pixel" --hidden-import=uvicorn --hidden-import=fastapi --hidden-import=cv2 --hidden-import=numpy --hidden-import=python_multipart --collect-all=uvicorn --collect-all=fastapi api\main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================
    echo ❌ 打包失败！
    echo ============================================================
    exit /b 1
)

echo.
echo [3/3] 打包完成！
echo.
echo ============================================================
echo ✅ 构建成功！
echo 📁 输出目录: dist\PixelArtRefiner
echo ============================================================
echo.
echo 📋 下一步:
echo    1. 将 dist\PixelArtRefiner 目录打包为 ZIP
echo    2. 或者使用 Inno Setup 创建安装程序
echo.

pause
