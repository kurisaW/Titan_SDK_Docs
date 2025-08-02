# Titan SDK 文档

这是一个基于 Sphinx 的 Titan SDK 文档项目，支持自动从 project 目录下的 README 文件生成在线文档。

## 功能特性

- **自动文档生成**: 从 `project/` 目录下的 README.md 文件自动生成 RST 文档
- **GitHub Pages 部署**: 自动构建并部署到 GitHub Pages
- **版本切换**: 支持类似 Read the Docs 的版本切换功能
- **多语言支持**: 支持中英文文档

## 目录结构

```
├── project/                    # 项目示例目录
│   ├── Titan_basic_*/         # 基础功能示例
│   ├── Titan_driver_*/        # 驱动示例
│   └── Titan_component_*/     # 组件示例
├── source/                    # Sphinx 文档源文件
├── scripts/                   # 自动生成脚本
│   └── generate_docs.py      # 文档生成脚本
└── .github/workflows/        # GitHub Actions 配置
```

## 使用方法

### 本地开发

1. 安装依赖:
   ```bash
   pip install -r source/requirements.txt
   ```

2. 生成文档:
   ```bash
   python scripts/generate_docs.py
   ```

3. 构建文档:
   ```bash
   sphinx-build -b html source source/_build/html
   ```

### 自动部署

推送代码到 main 分支后，GitHub Actions 会自动:

1. 扫描 `project/` 目录下的所有项目
2. 读取 README.md 和 README_EN.md 文件
3. 自动生成 RST 文档
4. 构建并部署到 GitHub Pages

## 维护文档

只需要维护 `project/` 目录下的 README.md 文件，系统会自动:

- 按项目名称前缀分类（basic/driver/component）
- 转换 Markdown 格式为 RST 格式
- 复制图片文件到静态资源目录
- 生成完整的文档结构

## 访问地址

文档部署在: https://kurisaw.github.io/Titan_SDK_Docs/