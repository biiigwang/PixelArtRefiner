# Sprint Plan: PixelArtRefiner 打包为可执行程序

## 项目信息
- **项目名称**: PixelArtRefiner
- **项目级别**: Level 2
- **当前阶段**: Sprint Planning
- **目标**: 将 Python 后端 + HTML 前端打包为 Windows 和 macOS 的可执行程序

## 项目现状

### 技术栈
- **后端**: Python 3.10 + FastAPI + Uvicorn
- **前端**: 纯 HTML + JavaScript (Vanilla JS)
- **图像处理**: OpenCV + NumPy
- **依赖管理**: Conda + pip
- **项目结构**:
  ```
  PixelArtRefiner/
  ├── api/              # FastAPI 后端
  ├── frontend/         # HTML 前端
  ├── perfectPixel/     # 图像处理算法 (Git 子模块)
  └── requirements.txt  # Python 依赖
  ```

### 已完成功能
- ✅ 宽高比归一化参数 (`normalize_ratio`)
- ✅ 后端 API (`/api/v1/process`)
- ✅ 前端 HTML 页面
- ✅ 图像处理算法

### 待完成任务
- ⬜ 将 Python 后端打包为可执行文件
- ⬜ 将前端资源嵌入可执行文件
- ⬜ Windows 平台打包
- ⬜ macOS 平台打包
- ⬜ 创建安装程序/便携包

## Sprint 目标

### Sprint 1: 可行性调研与基础打包 (2 周)
**目标**: 调研打包方案，完成基础打包流程验证

### Sprint 2: Windows 平台打包 (2 周)
**目标**: 完成 Windows 可执行程序打包和测试

### Sprint 3: macOS 平台打包 (2 周)
**目标**: 完成 macOS 可执行程序打包和测试

### Sprint 4: 发布与文档 (1 周)
**目标**: 创建发布包和用户使用文档

---

## Story Inventory

### Epic: 可执行程序打包

#### STORY-001: 调研 Python 打包方案
- **Epic**: 可执行程序打包
- **Priority**: Must Have
- **Points**: 3

**User Story:**
作为 开发者
我希望 调研 Python 打包工具
以便 选择最适合的打包方案

**Acceptance Criteria:**
- [ ] 调研 PyInstaller、cx_Freeze、Nuitka 等主流工具
- [ ] 对比各工具的优缺点
- [ ] 列出选择方案的理由
- [ ] 提供 POC 验证结果

**Technical Notes:**
- 评估标准：打包速度、可执行文件大小、跨平台支持、依赖处理、启动速度
- 特别关注点：OpenCV 和 NumPy 的处理

---

#### STORY-002: 创建基础打包脚本
- **Epic**: 可执行程序打包
- **Priority**: Must Have
- **Points**: 5

**User Story:**
作为 开发者
我希望 创建打包脚本
以便 自动化可执行文件的生成

**Acceptance Criteria:**
- [ ] 创建 build.py 打包脚本
- [ ] 处理项目依赖
- [ ] 配置 PyInstaller spec 文件
- [ ] 生成单文件可执行程序
- [ ] 测试生成的可执行文件可以正常运行

**Technical Notes:**
- 使用 PyInstaller 作为基础
- 需要处理 perfectPixel 子模块
- 需要包含前端静态文件
- 考虑使用 --onefile 或 --onedir 模式

**Dependencies:**
- STORY-001 完成

---

#### STORY-003: 嵌入前端静态资源
- **Epic**: 可执行程序打包
- **Priority**: Must Have
- **Points**: 3

**User Story:**
作为 用户
我希望 前端资源被嵌入到可执行文件中
以便 不需要单独部署前端文件

**Acceptance Criteria:**
- [ ] 前端 HTML/CSS/JS 文件被打包进可执行文件
- [ ] FastAPI 能够正确提供嵌入的静态文件
- [ ] 浏览器可以正常访问前端页面
- [ ] 页面功能完整

**Technical Notes:**
- 使用 PyInstaller 的 --add-data 参数
- 在代码中使用 pkgutil 或类似方式读取嵌入的资源
- 需要修改 FastAPI 的静态文件路由

**Dependencies:**
- STORY-002 完成

---

#### STORY-004: Windows 可执行程序打包
- **Epic**: 可执行程序打包
- **Priority**: Must Have
- **Points**: 5

**User Story:**
作为 Windows 用户
我希望 获得 Windows 可执行程序
以便 在 Windows 上运行应用

**Acceptance Criteria:**
- [ ] 在 Windows 环境或 CI 中构建 Windows 可执行文件
- [ ] 可执行文件在 Windows 10/11 上正常运行
- [ ] 处理 Windows 下的路径分隔符问题
- [ ] 提供 .exe 安装程序或便携包

**Technical Notes:**
- 在 Windows 上运行 PyInstaller
- 或使用 GitHub Actions 进行交叉编译
- 需要测试 OpenCV 在 Windows 上的兼容性
- 考虑使用 NSIS 或 Inno Setup 创建安装程序

**Dependencies:**
- STORY-002, STORY-003 完成

---

#### STORY-005: macOS 可执行程序打包
- **Epic**: 可执行程序打包
- **Priority**: Must Have
- **Points**: 5

**User Story:**
作为 macOS 用户
我希望 获得 macOS 可执行程序
以便 在 Mac 上运行应用

**Acceptance Criteria:**
- [ ] 在 macOS 环境或 CI 中构建 macOS 可执行文件
- [ ] 可执行文件在 macOS Intel 和 Apple Silicon 上正常运行
- [ ] 处理 macOS 下的库依赖问题
- [ ] 提供 .app 或 .dmg 安装包

**Technical Notes:**
- 在 macOS 上运行 PyInstaller
- 使用 GitHub Actions 进行交叉编译
- 需要创建 .app 应用包
- 可能需要处理代码签名问题

**Dependencies:**
- STORY-002, STORY-003 完成

---

#### STORY-006: 创建发布流程
- **Epic**: 可执行程序打包
- **Priority**: Should Have
- **Points**: 3

**User Story:**
作为 开发者
我希望 创建自动化的发布流程
以便 简化版本发布过程

**Acceptance Criteria:**
- [ ] 使用 GitHub Actions 创建 CI/CD 工作流
- [ ] 自动构建 Windows 和 macOS 可执行文件
- [ ] 自动生成发布包
- [ ] 创建 GitHub Release 并上传构建产物

**Technical Notes:**
- 使用 GitHub Actions 的矩阵构建
- 需要配置 secrets 用于代码签名（可选）
- 使用 PyInstaller 在 CI 环境中构建

**Dependencies:**
- STORY-004, STORY-005 完成

---

#### STORY-007: 编写用户文档
- **Epic**: 可执行程序打包
- **Priority**: Should Have
- **Points**: 2

**User Story:**
作为 用户
我希望 有清晰的使用文档
以便 了解如何安装和使用应用

**Acceptance Criteria:**
- [ ] 编写安装指南
- [ ] 编写使用说明
- [ ] 编写常见问题解答
- [ ] 更新 README.md

**Technical Notes:**
- 使用 Markdown 格式
- 包含截图说明
- 针对不同平台分别说明

**Dependencies:**
- STORY-004, STORY-005 完成

---

## Sprint 分配

### Sprint 1 (Week 1-2): 基础调研与工具选择
**目标**: 完成打包方案调研和基础环境搭建

**Stories:**
| Story ID | 标题 | Points | Priority |
|----------|------|--------|----------|
| STORY-001 | 调研 Python 打包方案 | 3 | Must Have |
| STORY-002 | 创建基础打包脚本 | 5 | Must Have |
| STORY-003 | 嵌入前端静态资源 | 3 | Must Have |

**总计**: 11 points

---

### Sprint 2 (Week 3-4): Windows 平台打包
**目标**: 完成 Windows 可执行程序打包

**Stories:**
| Story ID | 标题 | Points | Priority |
|----------|------|--------|----------|
| STORY-004 | Windows 可执行程序打包 | 5 | Must Have |

**总计**: 5 points

---

### Sprint 3 (Week 5-6): macOS 平台打包
**目标**: 完成 macOS 可执行程序打包

**Stories:**
| Story ID | 标题 | Points | Priority |
|----------|------|--------|----------|
| STORY-005 | macOS 可执行程序打包 | 5 | Must Have |

**总计**: 5 points

---

### Sprint 4 (Week 7): 发布流程和文档
**目标**: 完成发布流程和用户文档

**Stories:**
| Story ID | 标题 | Points | Priority |
|----------|------|--------|----------|
| STORY-006 | 创建发布流程 | 3 | Should Have |
| STORY-007 | 编写用户文档 | 2 | Should Have |

**总计**: 5 points

---

## 风险和缓解措施

### 技术风险

**高风险:**
1. **OpenCV/NumPy 打包问题**: 这些库在打包时可能遇到问题
   - 缓解措施: 在 Sprint 1 进行充分的 POC 验证

2. **跨平台兼容性问题**: 不同平台的库依赖可能有差异
   - 缓解措施: 使用 GitHub Actions 进行自动化测试

**中等风险:**
3. **代码签名问题**: macOS 和 Windows 可能需要代码签名
   - 缓解措施: 可以先创建未签名的版本，签名作为后续优化

### 资源风险

- **团队规模**: 如果只有 1 个开发者，需要合理安排时间
- **时间限制**: 如果需要在特定日期前完成，需要调整范围

---

## 定义完成 (Definition of Done)

对于一个 Story 被认为完成，需要满足：

- [ ] 代码实现完成并通过测试
- [ ] 可执行文件可以在目标平台上正常运行
- [ ] 代码审查通过
- [ ] 文档更新完成
- [ ] 验收标准满足

---

## 下一步行动

**立即可做:**
1. 开始 Sprint 1: 调研打包方案
2. 运行 `/create-story STORY-001` 创建详细 Story 文档
3. 或者运行 `/dev-story STORY-001` 直接开始实现

**准备工作:**
- 确保有 Windows 和 macOS 的测试环境
- 准备 GitHub 仓库用于 CI/CD
- 如果使用 BMAD 方法，运行 `/workflow-init` 初始化工作流

---

**本计划使用 BMAD Method v6 - Phase 4 (Implementation Planning) 创建**
