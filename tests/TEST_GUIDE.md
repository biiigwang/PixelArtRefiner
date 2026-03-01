# Pixel Art Refiner 测试指南

本文档提供 Pixel Art Refiner 项目的测试操作步骤和测试报告模板，用于回归测试。

## 目录结构

```
tests/
├── algorithm/              # 算法单元测试
│   ├── debug_aspect.py    # 宽高比调试脚本
│   ├── test_aspect_ratio.py  # 宽高比归一化测试
│   ├── test_grid_scale.py    # 网格比例测试
│   └── final_test.py      # 最终功能测试
├── integration/            # 集成测试
│   ├── test_api.py        # API 端点测试
│   └── test_api_complete.py  # 完整 API 测试
├── unit/                  # 单元测试（预留）
└── reports/               # 测试报告输出目录
```

---

## 快速开始

### 1. 环境准备

```bash
# 激活 conda 环境
conda activate perfectpixel

# 进入项目目录
cd /Users/biiigwang/Dev/gitCode/PixelArtRefiner

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行所有测试

```bash
# 方式一：使用测试脚本
python tests/integration/test_api.py

# 方式二：使用 pytest
pytest tests/ -v
```

---

## 测试操作步骤

### 步骤 1：启动服务

**方式 A：开发模式（使用源代码）**
```bash
cd /Users/biiigwang/Dev/gitCode/PixelArtRefiner
python api/main.py
```

**方式 B：生产模式（使用打包的应用）**
```bash
cd /Users/biiigwang/Dev/gitCode/PixelArtRefiner/dist/PixelArtRefiner
nohup ./PixelArtRefiner > /tmp/pixel_app.log 2>&1 &
sleep 3
```

### 步骤 2：健康检查

```bash
curl http://localhost:8000/api/v1/health
```

预期输出：
```json
{"status":"healthy","version":"0.1.0","service":"Pixel Art Refiner API"}
```

### 步骤 3：图像处理测试

```bash
curl -X POST http://localhost:8000/api/v1/process \
  -F "image=@perfectPixel/images/skull.png" \
  -F "sample_method=center" \
  -F "min_size=4.0" \
  -F "peak_width=6" \
  -F "refine_intensity=0.25" \
  -F "fix_square=true" \
  -F "normalize_ratio=true"
```

预期输出：
```json
{
  "status": "success",
  "original_size": [1024, 1024],
  "refined_size": [127, 123],
  "pixel_size": 8.19,
  "download_url": "/api/v1/download/xxx_result.png"
}
```

---

## 回归测试检查清单

### 功能测试

| 编号 | 测试项 | 预期结果 | 实际结果 | 状态 |
|------|--------|----------|----------|------|
| 1 | 服务启动 | 无报错，正常启动 | | |
| 2 | 健康检查 | 返回 healthy 状态 | | |
| 3 | 根端点 | 返回服务信息 | | |
| 4 | Web UI | 返回 HTML 页面 | | |
| 5 | 图像处理 | 返回处理结果 | | |
| 6 | 图像下载 | 返回 PNG 文件 | | |

### 参数组合测试

| 编号 | 参数 | 测试值 | 预期 | 实际 | 状态 |
|------|------|--------|------|------|------|
| 1 | sample_method | center | 成功处理 | | |
| 2 | sample_method | median | 成功处理 | | |
| 3 | sample_method | majority | 成功处理 | | |
| 4 | min_size | 2.0 | 成功处理 | | |
| 5 | min_size | 4.0 | 成功处理 | | |
| 6 | min_size | 8.0 | 成功处理 | | |
| 7 | fix_square | true | 输出正方形 | | |
| 8 | fix_square | false | 保持原比例 | | |
| 9 | normalize_ratio | true | 归一化比例 | | |
| 10 | normalize_ratio | false | 保持原比例 | | |

### 算法测试

| 编号 | 测试项 | 命令 | 预期 | 状态 |
|------|--------|------|------|------|
| 1 | 宽高比测试 | `python tests/algorithm/test_aspect_ratio.py` | 输出两张对比图 | |
| 2 | 网格比例测试 | `python tests/algorithm/test_grid_scale.py` | 显示比例差异 | |
| 3 | 最终测试 | `python tests/algorithm/final_test.py` | 测试通过 | |

---

## 测试图像资源

项目提供的测试图像：

| 路径 | 尺寸 | 说明 |
|------|------|------|
| `perfectPixel/images/skull.png` | 1024×1024 | 骷髅像素画 |
| `perfectPixel/images/pig.png` | - | 小猪像素画 |
| `img/test_img.png` | - | 测试用图 |

---

## 常见问题排查

### 端口占用

```bash
# 查看端口占用
lsof -i :8000

# 杀掉占用进程
kill <PID>
```

### 服务无响应

```bash
# 查看日志
tail -f /tmp/pixel_app.log

# 重启服务
pkill -f PixelArtRefiner
nohup ./PixelArtRefiner > /tmp/pixel_app.log 2>&1 &
```

### 图像处理失败

- 检查图像格式是否支持（PNG, JPG 等）
- 尝试调整 `min_size` 参数（推荐 4.0-8.0）
- 使用更清晰的像素艺术图像

---

## 输出报告

测试完成后，将结果记录到 `tests/reports/` 目录：

```bash
# 复制输出文件到报告目录
cp output_*.png tests/reports/

# 生成测试报告
date > tests/reports/test_report_$(date +%Y%m%d).txt
```

---