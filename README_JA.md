# 📡 Rik's Blog Monitor（ブログ更新監視）

[![GitHub Actions Status](https://github.com/zhuyikai2002/MyPythonMoniter/actions/workflows/daily_check.yml/badge.svg)](https://github.com/zhuyikai2002/MyPythonMoniter/actions)

---

**🌍 Languages / 语言 / 言語 / اللغات:**

[English](./README_EN.md) | [简体中文](./README.md) | [日本語](./README_JA.md) | [العربية](./README_AR.md)

---

> 💡 Linux/組み込みCからPython自動化への転身を示すマイルストーン作品

「青龍パネル+DingTalkプッシュ」に触発され、Mac Mini上で開発されたPython自動化プロジェクト。GitHub Actionsを通じてサーバーレスのブログ更新監視を実現し、ServerChanと組み合わせてWeChatリアルタイム通知を実装。

## ✨ コア機能

- 🎯 **スマート監視**：[qzkj.ltd](https://qzkj.ltd/blog) ブログの更新を自動検出
- 🛡️ **ファイアウォール回避**：`cloudscraper`を使用してCloudflare保護を突破（403問題を解決）
- ⏰ **定時タスク**：GitHub Actionsが毎時自動実行、サーバーメンテナンス不要
- 📲 **WeChat通知**：ServerChan統合により、ブログ更新を即座にWeChatへプッシュ
- 🔒 **クラッシュ防止**：例外処理を内蔵し、Gitコミットエラーを防止

## 🛠️ 技術スタック

| 技術 | バージョン | 用途 |
|------|-----------|------|
| **Python** | 3.9+ | コアランタイム環境 |
| **cloudscraper** | Latest | Cloudflare保護の回避 |
| **BeautifulSoup4** | Latest | HTML解析とデータ抽出 |
| **GitHub Actions** | - | 自動化タスクスケジューリング |
| **ServerChan** | API v3 | WeChatメッセージプッシュ |

## 📦 プロジェクト構造

```
MyPythonMoniter/
├── monitor.py         # メイン監視プログラム（本番環境）
├── spider.py          # Webスクレイパーテストスクリプト
├── notify.py          # ServerChanプッシュテストスクリプト
├── last_title.txt     # 前回検出したタイトルを保存
└── README.md          # プロジェクトドキュメント
```

## 🚀 クイックスタート

### 1. 環境準備

Python 3.9以上がインストールされていることを確認：

```bash
python --version
```

### 2. 依存関係のインストール

```bash
pip install cloudscraper beautifulsoup4 requests
```

### 3. ローカルテスト

```bash
# メイン監視プログラムを実行
python monitor.py

# Webスクレイパー機能をテスト
python spider.py

# WeChat通知をテスト
python notify.py
```

### 4. GitHub Actions デプロイ

#### 4.1 シークレット設定

GitHubリポジトリにシークレットを追加：

- `Settings` → `Secrets and variables` → `Actions`へ移動
- `SERVER_KEY`を追加し、ServerChanのSCKEY値を設定

#### 4.2 ワークフロー作成

プロジェクトルートに`.github/workflows/daily_check.yml`を作成：

```yaml
name: Blog Monitor

on:
  schedule:
    - cron: '0 * * * *'  # 毎時実行
  workflow_dispatch:      # 手動トリガーサポート

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

## 🎨 コアロジック

### ファイアウォール回避メカニズム

```python
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)
```

Chromeブラウザに偽装することで、CloudflareのJavaScriptチャレンジ検証を突破。

### 更新検出フロー

1. `cloudscraper`を使用してブログのホームページを取得
2. BeautifulSoupで最新記事タイトルを解析
3. `last_title.txt`の記録と比較
4. 更新検出時、ServerChan経由でWeChat通知をプッシュ
5. ローカル記録ファイルを更新

## 📝 設定説明

`monitor.py`の設定セクションを編集：

```python
BLOG_URL = "https://qzkj.ltd/blog"        # 監視するブログURL
SERVER_KEY = os.getenv("SERVER_KEY")      # ServerChan SCKEY
RECORD_FILE = "last_title.txt"            # 記録ファイルパス
```

## 🔧 よくある質問

### Q: 403エラーが発生する？
**A**: これはまさに`cloudscraper`が解決する問題です。ライブラリが正しくインストールされているか確認してください。

### Q: WeChat通知が届かない？
**A**: `SERVER_KEY`環境変数が正しく設定されているか確認してください。

### Q: GitHub Actionsが実行されない？
**A**: cron式が正しいか確認するか、workflow_dispatchを手動でトリガーしてください。

## 📊 実行状態

最新の監視結果を表示：
- ✅ 現在監視中の記事：`履歴書を書くつもりだったのに、気がついたらWebサイト全体をリファクタリングしていた`

## 🎯 今後の計画

- [ ] 複数のブログソース監視をサポート
- [ ] DingTalk、WeCom等のプッシュチャネルを追加
- [ ] Webコントロールパネルを実装
- [ ] カスタム監視頻度をサポート

## 📄 ライセンス

このプロジェクトは個人学習・研究目的でのみ使用されます。

---

<div align="center">
  <strong>Created by Rik in 2026</strong>
  <br>
  <sub>🚀 組み込みエンジニアからPython自動化への道</sub>
</div>
