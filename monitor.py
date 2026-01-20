import requests
from bs4 import BeautifulSoup
import time
import os

# ================= 配置区域 =================
BLOG_URL = "https://qzkj.ltd"
SERVER_KEY = "SCT310360TXJBC3KjVRxheEqzbSO9r6Vhm"  # <--- 记得替换！
CHECK_INTERVAL = 3600  # 检测间隔，单位是秒。3600秒 = 1小时


# ===========================================

def send_wechat_msg(title, content):
    """ 发送微信通知的函数 """
    url = f"https://sctapi.ftqq.com/{SERVER_KEY}.send"
    data = {'title': title, 'desp': content}
    try:
        requests.post(url, data=data)
        print("✅ 微信通知已发送")
    except Exception as e:
        print(f"❌ 发送失败: {e}")


def get_latest_post_title():
    """ 去博客抓取最新的一篇文章标题 """
    try:
        # 伪装成浏览器（有些网站反爬虫）
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(BLOG_URL, headers=headers)
        resp.encoding = 'utf-8'  # 防止乱码

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # 这里的 .post-title-link 是Hexo常用的类名，如果抓不到需要根据实际网页修改
            # find 只会找第一个，也就是最新的那个
            latest_post = soup.find('a', class_='post-title-link')
            if latest_post:
                return latest_post.text.strip()
    except Exception as e:
        print(f"⚠️ 抓取网页出错: {e}")
    return None


def main():
    print("🚀 博客监控服务已启动...")

    # 记录文件的名字
    record_file = "last_title.txt"

    while True:
        # 1. 获取当前线上的最新标题
        current_title = get_latest_post_title()

        if current_title:
            print(f"🔍 当前最新文章: {current_title}")

            # 2. 读取我们本地记录的“旧标题”
            last_title = ""
            if os.path.exists(record_file):
                with open(record_file, "r", encoding="utf-8") as f:
                    last_title = f.read().strip()

            # 3. 核心判断逻辑
            if current_title != last_title:
                # 标题不一样！说明有更新！
                print("🎉 发现新文章！正在推送...")

                # 发送通知
                msg = f"检测到博客更新啦！\n新文章标题：{current_title}\n快去看看吧：{BLOG_URL}"
                send_wechat_msg("博客更新提醒", msg)

                # 4. 把新标题记入小本本
                with open(record_file, "w", encoding="utf-8") as f:
                    f.write(current_title)
            else:
                print("💤 暂无更新")

        else:
            print("❌ 没抓到标题，可能是网站挂了或者改版了")

        # 5. 休息等待下一轮
        print(f"⏳ 等待 {CHECK_INTERVAL} 秒后进行下一次检查...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()