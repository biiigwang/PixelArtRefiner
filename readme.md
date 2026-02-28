# Pixel Art Refiner

将 AI 生成的伪像素画转换为像素完美的艺术作品。

## 简介

Pixel Art Refiner 是一个基于 Perfect Pixel 算法的 Web 服务，旨在解决 AI 生成的像素艺术作品中常见的网格对齐问题。无论是游戏开发者需要高质量像素资源，还是设计师需要像素风格图标，只需上传图片，即可自动获得网格对齐精确的像素完美作品。

## 功能特性

- **图片处理**：自动检测并优化像素网格，将不规则的伪像素画转换为完美像素艺术
- **Web UI**：简单易用的网页界面，支持手动上传和参数调整
- **RESTful API**：功能完整的 API 接口，便于开发者集成到其他系统
- **参数配置**：支持多种算法参数调整，满足不同场景需求

## 技术栈

- **后端**：Python 3.10+ / FastAPI / Uvicorn
- **算法**：Perfect Pixel (基于 FFT 频谱分析的像素网格检测)
- **前端**：HTML5 + Vanilla JavaScript + Bootstrap 5

## 致谢

本项目使用了开源库 [perfectPixel](https://github.com/theamusing/perfectPixel) 作为核心算法（Git 子模块），感谢原作者的贡献。
## 快速开始

### 本地运行

```bash
# 克隆项目后，安装依赖
pip install -r requirements.txt

# 启动服务
cd api
python main.py
```

或者使用 conda 创建环境：

```bash
# 创建并激活环境
conda create -n pixel-refiner python=3.10
conda activate pixel-refiner

# 安装依赖
pip install -r requirements.txt

# 启动服务
cd api
python main.py
```

服务启动后访问：

- Web UI: http://localhost:8000/app
- API 文档: http://localhost:8000/docs

### Docker 运行

```bash
docker-compose up -d
```

## API 使用

### 基本调用

```python
import requests

url = "http://localhost:8000/api/v1/process"
files = {"image": open("your_image.png", "rb")}
data = {
    "sample_method": "center",
    "min_size": 4.0,
    "peak_width": 6,
    "refine_intensity": 0.25,
    "fix_square": True
}

response = requests.post(url, files=files, data=data)
result = response.json()
print(result["download_url"])
```

### 参数说明

| 参数                 | 类型   | 默认值 | 说明                             |
| -------------------- | ------ | ------ | -------------------------------- |
| `sample_method`    | string | center | 采样方法：center/median/majority |
| `min_size`         | float  | 4.0    | 最小像素尺寸 (1.0-20.0)          |
| `peak_width`       | int    | 6      | 峰宽，用于 FFT 峰值检测 (1-20)   |
| `refine_intensity` | float  | 0.25   | 网格细化强度 (0.0-1.0)           |
| `fix_square`       | bool   | true   | 是否修正为正方形                 |

详细参数说明请参考 [参数指南](docs/parameters-guide.md)

## 典型场景配置

### 标准像素游戏素材

```yaml
采样方法: center
最小像素尺寸: 4.0
峰宽: 6
细化强度: 0.25
修正正方形: true
```

### AI 生成的伪像素图（有抗锯齿）

```yaml
采样方法: majority
最小像素尺寸: 4.0
峰宽: 6
细化强度: 0.3
修正正方形: true
```

### 高清像素艺术（64x64+）

```yaml
采样方法: median
最小像素尺寸: 8.0
峰宽: 8
细化强度: 0.2
修正正方形: true
```

## 项目结构

```
.
├── api/                    # 后端 API
│   └── main.py            # 主应用
├── frontend/               # 前端页面
├── perfect-pixel/          # 算法子模块
├── docs/                   # 项目文档
├── tests/                  # 测试代码
├── Dockerfile             # Docker 配置
├── docker-compose.yml     # Docker Compose 配置
└── requirements.txt       # Python 依赖
```

## 文档

- [产品简介](docs/product-brief-pixel-art-refiner-20260226.md)
- [技术规格](docs/tech-spec-pixel-art-refiner-20260226.md)
- [参数指南](docs/parameters-guide.md)

## 许可证

MIT License
