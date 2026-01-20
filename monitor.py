import requests
from bs4 import BeautifulSoup
import os

# ================= 配置区域 =================
BLOG_URL = "https://qzkj.ltd"
# GitHub Actions 会自动把 Secrets 注入到环境变量中，不需要 load_dotenv
SERVER_KEY = os.getenv("SERVER_KEY")
RECORD_FILE = "last_title.txt"


# ===========================================

def send_wechat_msg(title, content):
    if not SERVER_KEY:
        print("❌ 没有找到 SERVER_KEY，跳过发送")
        return
    url = f"https://sctapi.ftqq.com/{SERVER_KEY}.send"
    data = {'title': title, 'desp': content}
    try:
        requests.post(url, data=data)
        print("✅ 微信通知已发送")
    except Exception as e:
        print(f"❌ 发送失败: {e}")


def get_latest_post_title():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        resp = requests.get(BLOG_URL, headers=headers, timeout=15)
        resp.encoding = 'utf-8'

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # 使用我们之前 debug 确认过的正确类名
            latest_post = soup.find('a', class_='article-title')
            if latest_post:
                return latest_post.text.strip()
            else:
                print("❌ 未找到 article-title 标签，请检查网页结构")
        else:
            print(f"⚠️ 网页访问失败: {resp.status_code}")
    except Exception as e:
        print(f"⚠️ 抓取报错: {e}")
    return None


def main():
    print("🚀 开始执行一次性检查...")

    # 1. 抓取线上最新标题
    current_title = get_latest_post_title()
    if not current_title:
        print("❌ 抓取失败，任务结束")
        return

    print(f"🔍 线上最新文章: {current_title}")

    # 2. 读取仓库里的旧标题
    last_title = ""
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r", encoding="utf-8") as f:
            last_title = f.read().strip()

    # 3. 对比
    if current_title != last_title:
        print("🎉 发现新文章！准备推送...")
        msg = f"文章更新啦：{current_title}\n{BLOG_URL}"
        send_wechat_msg("博客更新提醒", msg)

        # 4. 把新标题写入文件
        # 注意：这里我们只管写，GitHub Actions 会负责把这个文件提交回仓库！
        with open(RECORD_FILE, "w", encoding="utf-8") as f:
            f.write(current_title)
    else:
        print("💤 标题未变，暂无更新")


if __name__ == "__main__":
    main()