import cloudscraper
from bs4 import BeautifulSoup
import os

# ================= 配置区域 =================
BLOG_URL = "https://qzkj.ltd"
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
        # 这里的 requests 不需要换，因为 Server酱没有防火墙
        import requests
        requests.post(url, data=data)
        print("✅ 微信通知已发送")
    except Exception as e:
        print(f"❌ 发送失败: {e}")


def get_latest_post_title():
    """ 使用 cloudscraper 绕过防火墙抓取 """
    try:
        # 创建一个“通过验证”的浏览器实例
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )

        print(f"🕵️‍♂️ 正在伪装成 Chrome 访问: {BLOG_URL} ...")
        resp = scraper.get(BLOG_URL, timeout=30)
        resp.encoding = 'utf-8'

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')

            # 尝试多种可能的标题选择器（为了保险）
            possible_selectors = [
                ('a', 'article-title'),  # 你博客原本的结构
                ('h1', 'post-title'),  # 常见结构1
                ('h2', 'post-title'),  # 常见结构2
                ('.post-title-link', None)  # 常见结构3
            ]

            latest_post = None
            for tag, cls in possible_selectors:
                if cls:
                    latest_post = soup.find(tag, class_=cls)
                else:
                    latest_post = soup.select_one(tag)

                if latest_post:
                    print(f"✅ 成功通过 {tag}.{cls} 找到标题")
                    break

            if latest_post:
                return latest_post.text.strip()
            else:
                print("❌ 网页访问成功，但没找到标题标签！")
                # 打印出网页前500个字，帮我们看看到底抓到了啥
                print(f"🧐 网页内容摘要: {soup.text[:200]}...")
                return None
        else:
            print(f"⚠️ 访问被拦截，状态码: {resp.status_code}")
            return None

    except Exception as e:
        print(f"💥 抓取严重报错: {e}")
    return None


def main():
    print("🚀 开始执行 CloudScraper 检查...")

    current_title = get_latest_post_title()

    if not current_title:
        print("❌ 抓取失败，任务结束")
        return

    print(f"🔍 线上最新文章: {current_title}")

    last_title = ""
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r", encoding="utf-8") as f:
            last_title = f.read().strip()

    if current_title != last_title:
        print(f"🎉 发现新文章: {current_title}")
        msg = f"文章更新啦：{current_title}\n{BLOG_URL}"
        send_wechat_msg("博客更新提醒", msg)

        with open(RECORD_FILE, "w", encoding="utf-8") as f:
            f.write(current_title)
    else:
        print("💤 标题未变，暂无更新")


if __name__ == "__main__":
    main()