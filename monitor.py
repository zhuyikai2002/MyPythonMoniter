import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

# 1. 加载本地的 .env 文件
load_dotenv()

# ================= 配置区域 =================
BLOG_URL = "https://qzkj.ltd"
SERVER_KEY = os.getenv("SERVER_KEY")
CHECK_INTERVAL = 3600

if not SERVER_KEY:
    print("❌ 警告：未找到 SERVER_KEY！")


# ===========================================

def send_wechat_msg(title, content):
    """ 发送微信通知 """
    url = f"https://sctapi.ftqq.com/{SERVER_KEY}.send"
    data = {'title': title, 'desp': content}
    try:
        requests.post(url, data=data)
        print("✅ 微信通知已发送")
    except Exception as e:
        print(f"❌ 发送失败: {e}")


def get_latest_post_title():
    """ 抓取最新文章标题 """
    try:
        # 【核心修改】这里换成了和你 debug.py 一模一样的完整身份证
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        resp = requests.get(BLOG_URL, headers=headers, timeout=15)
        resp.encoding = 'utf-8'

        # 【新增诊断】如果状态码不是200（成功），就打印出来到底是几
        if resp.status_code != 200:
            print(f"⚠️ 访问被拒绝，状态码: {resp.status_code}")
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')
        latest_post = soup.find('a', class_='article-title')

        if latest_post:
            return latest_post.text.strip()

    except Exception as e:
        print(f"⚠️ 抓取报错: {e}")
    return None


def main():
    print("🚀 博客监控服务已启动...")
    record_file = "last_title.txt"

    while True:
        current_title = get_latest_post_title()

        if current_title:
            print(f"🔍 当前最新文章: {current_title}")

            last_title = ""
            if os.path.exists(record_file):
                with open(record_file, "r", encoding="utf-8") as f:
                    last_title = f.read().strip()

            if current_title != last_title:
                print("🎉 发现新文章！正在推送...")
                msg = f"文章更新啦：{current_title}\n{BLOG_URL}"
                send_wechat_msg("博客更新提醒", msg)

                with open(record_file, "w", encoding="utf-8") as f:
                    f.write(current_title)
            else:
                print("💤 暂无更新")

        else:
            print("❌ 本次未抓取到标题（可能是网络波动或被拦截）")

        print(f"⏳ 等待 {CHECK_INTERVAL} 秒...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()