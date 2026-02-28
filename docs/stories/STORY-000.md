# STORY-000：开发环境搭建

**Epic：** 基础设施建设
**Priority：** P0（Must Have）
**Story Points：** 2
**Status：** Not Started
**Assigned To：** Unassigned
**Created：** 2026-02-26
**Sprint：** 1

---

## User Story

作为开发者，我希望搭建完整的开发环境，以便能够开始开发 Pixel Art Refiner 项目。

---

## Description

### Background

在开始 Pixel Art Refiner 项目开发之前，需要建立一个完整、可复现的开发环境。这包括项目结构创建、依赖库安装、开发服务器配置以及基础的项目管理设置。

### Scope

**In scope：**
- 按照技术规格说明创建项目结构
- 安装所需的依赖库（FastAPI、Perfect Pixel、OpenCV、numpy）
- 配置开发服务器（Uvicorn）
- 测试 Perfect Pixel 算法的功能
- 配置 git 版本控制

**Out of scope：**
- 生产环境部署配置
- 高级功能的实现（如并发处理、监控）
- 文档编写

### User Flow

1. 开发者克隆项目或创建新项目结构
2. 安装并配置 Python 虚拟环境
3. 安装项目依赖库
4. 创建基础的项目文件和配置
5. 测试 Perfect Pixel 算法的基本功能
6. 初始化 git 仓库并进行第一次提交

---

## Acceptance Criteria

- [ ] 项目结构按照技术规格说明创建，包括 api、frontend、tests 等目录
- [ ] 成功创建 requirements.txt 文件，包含所有必要的依赖
- [ ] Python 虚拟环境成功创建并激活
- [ ] 所有依赖库成功安装，包括 FastAPI、Uvicorn、Perfect Pixel、OpenCV、numpy
- [ ] 开发服务器成功启动并运行在默认端口（通常是 8000）
- [ ] 可以成功运行 Perfect Pixel 算法的示例代码
- [ ] 项目成功使用 git 进行版本控制
- [ ] 项目目录结构在文件系统中正确显示

---

## Technical Notes

### 项目结构

```
pixel-art-refiner/
├── api/              # 后端 API
│   ├── main.py       # 主应用文件
│   ├── endpoints/    # API 端点
│   ├── dependencies/ # 依赖注入
│   ├── schemas/      # 请求/响应模型
│   ├── services/     # 业务逻辑
│   └── utils/        # 工具函数
├── frontend/         # 前端代码
│   ├── index.html    # 主页面
│   ├── styles.css    # 样式
│   ├── script.js     # 前端逻辑
│   └── assets/       # 静态资源
├── tests/            # 测试代码
│   ├── test_api.py   # API 测试
│   └── test_processing.py # 处理逻辑测试
├── .dockerignore     # Docker 忽略文件
├── Dockerfile        # Docker 镜像
├── docker-compose.yml# Docker 编排
├── requirements.txt  # Python 依赖
└── README.md         # 项目说明
```

### 依赖库安装

```bash
# 使用 pip 安装基本依赖
pip install fastapi uvicorn numpy opencv-python python-multipart python-magic

# 安装 perfect-pixel 库
pip install perfect-pixel[opencv]
```

### 虚拟环境创建

```bash
# 创建虚拟环境（Windows）
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 创建虚拟环境（Mac/Linux）
python3 -m venv venv

# 激活虚拟环境（Mac/Linux）
source venv/bin/activate
```

### 验证 Perfect Pixel 算法

创建简单的测试脚本 `test_algorithm.py`：

```python
import cv2
from perfect_pixel import get_perfect_pixel

# 读取示例图片
bgr = cv2.imread("images/girl.jpg", cv2.IMREAD_COLOR)
if bgr is None:
    raise FileNotFoundError("无法读取图片")

rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

# 测试 Perfect Pixel 算法
w, h, out = get_perfect_pixel(rgb, sample_method="center", refine_intensity=0.3)

# 显示结果
print(f"输入图片尺寸: {rgb.shape[1]}x{rgb.shape[0]}")
print(f"输出图片尺寸: {w}x{h}")

# 保存结果
out_bgr = cv2.cvtColor(out, cv2.COLOR_RGB2BGR)
cv2.imwrite("output_test.png", out_bgr)

print("处理完成！结果已保存到 output_test.png")
```

### 开发服务器配置

创建最小化的 main.py 文件：

```python
from fastapi import FastAPI

app = FastAPI(title="Pixel Art Refiner", version="0.1.0")

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/")
async def root():
    return {"message": "Pixel Art Refiner API"}
```

### Git 初始化

```bash
# 初始化 git 仓库
git init

# 第一次提交
git add .
git commit -m "Initial commit: Project structure and basic configuration"
```

### 安全注意事项

- 确保忽略敏感文件（如 venv、*.pyc、__pycache__）
- 使用 .gitignore 文件配置忽略规则
- 不提交密码、API 密钥等敏感信息

### 边界情况

- 如果 OpenCV 安装失败，尝试使用 conda 安装或下载预编译版本
- 确保系统有足够的资源（建议内存 ≥ 4GB）
- 如果网络问题导致依赖库无法下载，考虑使用本地镜像源

---

## Dependencies

### 技术依赖

- **Python 3.10+**：项目使用 Python 3.10 或更高版本
- **pip 包管理器**：用于安装项目依赖
- **操作系统支持**：项目应该能在 Windows、Mac 和 Linux 上运行，但需要适当调整

### 外部依赖

- **pip 镜像源**：如果使用默认源下载速度慢，可能需要配置镜像源
- **文件系统权限**：项目需要有足够的权限来读取和写入文件

### 人员依赖

- **开发者**：需要具备 Python 开发经验和基本的命令行操作知识

---

## Definition of Done

- [ ] 项目结构按照技术规格说明创建
- [ ] 依赖库成功安装（FastAPI、Perfect Pixel、OpenCV、numpy）
- [ ] 开发服务器成功启动（Uvicorn）
- [ ] 可以成功运行 Perfect Pixel 算法的示例代码
- [ ] 项目使用 git 进行版本控制
- [ ] 所有验收标准都已满足
- [ ] 代码通过基本的格式检查
- [ ] 项目可以在另一台机器上成功重建

---

## Story Points Breakdown

- **项目结构创建**：0.5 个故事点
- **依赖库安装和配置**：0.5 个故事点
- **虚拟环境创建**：0.5 个故事点
- **Perfect Pixel 算法测试**：0.3 个故事点
- **开发服务器配置**：0.2 个故事点
- **git 初始化和提交**：0.5 个故事点
- **总：2 个故事点**

---

## Additional Notes

### 常见问题解决

1. **OpenCV 安装失败**：
   - 使用 conda 安装：`conda install -c conda-forge opencv`
   - 下载预编译版本并手动配置

2. **依赖库版本冲突**：
   - 使用 virtualenv 或 conda 虚拟环境
   - 尝试安装特定版本的库

3. **网络问题**：
   - 使用国内镜像源：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package_name`
   - 配置 pip 全局镜像源

---

## Progress Tracking

**Status History：**
- 2026-02-26：创建故事文档

**Actual Effort：** TBD（将在实施过程中记录）

---

**This story was created using BMAD Method v6 - Phase 4 (Implementation Planning)**
