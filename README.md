# 📡 Rik's Blog Monitor (博客更新哨兵)

![GitHub Actions Status](https://github.com/zhuyikai2002/MyPythonMoniter/actions/workflows/daily_check.yml/badge.svg)

> 💡 从 Linux/嵌入式 C 转战 Python 自动化的里程碑之作

一个受"青龙面板+钉钉推送"启发，在 Mac Mini 上孕育的 Python 自动化项目。通过 GitHub Actions 实现免服务器的博客更新监控，结合 Server酱 实现微信实时推送。

## ✨ 核心特性

- 🎯 **智能监控**：自动检测 [qzkj.ltd](https://qzkj.ltd/blog) 博客更新
- 🛡️ **防火墙绕过**：使用 `cloudscraper` 突破 Cloudflare 防护（解决 403 问题）
- ⏰ **定时任务**：GitHub Actions 每小时自动执行，无需维护服务器
- 📲 **微信推送**：集成 Server酱，博客更新即时推送到微信
- 🔒 **防崩逻辑**：内置异常处理，防止 Git 提交报错

## 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.9+ | 核心运行环境 |
| **cloudscraper** | Latest | 绕过 Cloudflare 防护 |
| **BeautifulSoup4** | Latest | HTML 解析与数据提取 |
| **GitHub Actions** | - | 自动化任务调度 |
| **Server酱** | API v3 | 微信消息推送 |

## 📦 项目结构

```
MyPythonMoniter/
├── monitor.py         # 主监控程序（生产环境）
├── spider.py          # 爬虫测试脚本
├── notify.py          # Server酱推送测试脚本
├── last_title.txt     # 存储上次检测的标题
└── README.md          # 项目说明文档
```

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.9 或更高版本：

```bash
python --version
```

### 2. 安装依赖

```bash
pip install cloudscraper beautifulsoup4 requests
```

### 3. 本地测试

```bash
# 运行主监控程序
python monitor.py

# 测试爬虫功能
python spider.py

# 测试微信推送
python notify.py
```

### 4. GitHub Actions 部署

#### 4.1 配置 Secret

在 GitHub 仓库中添加 Secret：

- 进入 `Settings` → `Secrets and variables` → `Actions`
- 添加 `SERVER_KEY`，值为你的 Server酱 SCKEY

#### 4.2 创建 Workflow

在项目根目录创建 `.github/workflows/daily_check.yml`：

```yaml
name: Blog Monitor

on:
  schedule:
    - cron: '0 * * * *'  # 每小时执行一次
  workflow_dispatch:      # 支持手动触发

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install Dependencies
        run: |
          pip install cloudscraper beautifulsoup4 requests
      
      - name: Run Monitor
        env:
          SERVER_KEY: ${{ secrets.SERVER_KEY }}
        run: |
          python monitor.py
      
      - name: Commit Changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add last_title.txt
          git diff --quiet && git diff --staged --quiet || git commit -m "Update last_title.txt"
          git push || true
```

## 🎨 核心逻辑

### 防火墙绕过机制

```python
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)
```

通过伪装成 Chrome 浏览器，成功绕过 Cloudflare 的 JavaScript 挑战验证。

### 更新检测流程

1. 使用 `cloudscraper` 获取博客首页
2. 通过 BeautifulSoup 解析最新文章标题
3. 与 `last_title.txt` 中的记录对比
4. 检测到更新时，通过 Server酱 推送微信通知
5. 更新本地记录文件

## 📝 配置说明

编辑 `monitor.py` 中的配置区域：

```python
BLOG_URL = "https://qzkj.ltd/blog"        # 监控的博客地址
SERVER_KEY = os.getenv("SERVER_KEY")      # Server酱 SCKEY
RECORD_FILE = "last_title.txt"            # 记录文件路径
```

## 🔧 常见问题

### Q: 遇到 403 错误？
**A**: 这正是 `cloudscraper` 要解决的问题，确保已正确安装该库。

### Q: 没有收到微信推送？
**A**: 检查 `SERVER_KEY` 环境变量是否正确配置。

### Q: GitHub Actions 不执行？
**A**: 检查 cron 表达式是否正确，或手动触发 workflow_dispatch。

## 📊 运行状态

查看最新的监控结果：
- ✅ 当前监控的文章：`我原本只是想写个简历，结果顺手重构了整个网站`

## 🎯 未来规划

- [ ] 支持多个博客源监控
- [ ] 添加钉钉、企业微信等推送渠道
- [ ] 实现 Web 控制面板
- [ ] 支持自定义监控频率

## 📄 许可证

本项目仅供个人学习和研究使用。

---

<div align="center">
  <strong>Created by Rik in 2026</strong>
  <br>
  <sub>🚀 从嵌入式工程师到 Python 自动化之路</sub>
</div>
