# 📡 Rik's Blog Monitor

[![GitHub Actions Status](https://github.com/zhuyikai2002/MyPythonMoniter/actions/workflows/daily_check.yml/badge.svg)](https://github.com/zhuyikai2002/MyPythonMoniter/actions)

---

**🌍 Languages / 语言 / 言語 / اللغات:**

[English](./README_EN.md) | [简体中文](./README.md) | [日本語](./README_JA.md) | [العربية](./README_AR.md)

---

> 💡 A milestone project transitioning from Linux/Embedded C to Python automation

A Python automation project inspired by "Qinglong Panel + DingTalk Push", developed on Mac Mini. Implements serverless blog update monitoring through GitHub Actions, combined with ServerChan for real-time WeChat notifications.

## ✨ Core Features

- 🎯 **Smart Monitoring**: Automatically detects updates on [qzkj.ltd](https://qzkj.ltd/blog) blog
- 🛡️ **Firewall Bypass**: Uses `cloudscraper` to bypass Cloudflare protection (solves 403 issues)
- ⏰ **Scheduled Tasks**: GitHub Actions runs automatically every hour, no server maintenance required
- 📲 **WeChat Push**: Integrated with ServerChan for instant WeChat notifications on blog updates
- 🔒 **Crash Prevention**: Built-in exception handling to prevent Git commit errors

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Core runtime environment |
| **cloudscraper** | Latest | Bypass Cloudflare protection |
| **BeautifulSoup4** | Latest | HTML parsing and data extraction |
| **GitHub Actions** | - | Automated task scheduling |
| **ServerChan** | API v3 | WeChat message push |

## 📦 Project Structure

```
MyPythonMoniter/
├── monitor.py         # Main monitoring program (production)
├── spider.py          # Web scraper test script
├── notify.py          # ServerChan push test script
├── last_title.txt     # Stores last detected title
└── README.md          # Project documentation
```

## 🚀 Quick Start

### 1. Environment Setup

Ensure Python 3.9 or higher is installed:

```bash
python --version
```

### 2. Install Dependencies

```bash
pip install cloudscraper beautifulsoup4 requests
```

### 3. Local Testing

```bash
# Run main monitoring program
python monitor.py

# Test web scraper functionality
python spider.py

# Test WeChat push
python notify.py
```

### 4. GitHub Actions Deployment

#### 4.1 Configure Secret

Add Secret in GitHub repository:

- Go to `Settings` → `Secrets and variables` → `Actions`
- Add `SERVER_KEY` with your ServerChan SCKEY value

#### 4.2 Create Workflow

Create `.github/workflows/daily_check.yml` in project root:

```yaml
name: Blog Monitor

on:
  schedule:
    - cron: '0 * * * *'  # Run every hour
  workflow_dispatch:      # Support manual trigger

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

## 🎨 Core Logic

### Firewall Bypass Mechanism

```python
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)
```

Successfully bypasses Cloudflare's JavaScript challenge verification by masquerading as Chrome browser.

### Update Detection Flow

1. Fetch blog homepage using `cloudscraper`
2. Parse latest article title with BeautifulSoup
3. Compare with record in `last_title.txt`
4. Push WeChat notification via ServerChan when update detected
5. Update local record file

## 📝 Configuration

Edit the configuration section in `monitor.py`:

```python
BLOG_URL = "https://qzkj.ltd/blog"        # Blog URL to monitor
SERVER_KEY = os.getenv("SERVER_KEY")      # ServerChan SCKEY
RECORD_FILE = "last_title.txt"            # Record file path
```

## 🔧 FAQ

### Q: Encountering 403 errors?
**A**: This is exactly what `cloudscraper` solves. Ensure the library is correctly installed.

### Q: Not receiving WeChat notifications?
**A**: Check if the `SERVER_KEY` environment variable is correctly configured.

### Q: GitHub Actions not running?
**A**: Verify the cron expression is correct, or manually trigger workflow_dispatch.

## 📊 Running Status

View latest monitoring results:
- ✅ Currently monitoring article: `I originally just wanted to write a resume, but ended up refactoring the entire website`

## 🎯 Future Plans

- [ ] Support monitoring multiple blog sources
- [ ] Add DingTalk, WeCom and other push channels
- [ ] Implement web control panel
- [ ] Support custom monitoring frequency

## 📄 License

This project is for personal learning and research use only.

---

<div align="center">
  <strong>Created by Rik in 2026</strong>
  <br>
  <sub>🚀 From Embedded Engineer to Python Automation Journey</sub>
</div>
