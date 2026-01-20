import requests
from bs4 import BeautifulSoup

# 1. 确定目标：你自己的博客
url = 'https://qzkj.ltd/blog'

# 2. 伪装自己：告诉服务器“我是浏览器”，不是可疑的脚本
# (虽然你爬自己不需要这步，但养成好习惯很重要)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"🕷️ 正在悄悄靠近目标: {url} ...")

# 3. 发起攻击：发送 GET 请求
try:
    response = requests.get(url, headers=headers)

    # 【重点】强制告诉 Python：这个网页是 UTF-8 编码的！
    response.encoding = 'utf-8'

    # 检查是不是成功了 (200 代表成功，404 代表找不到)
    if response.status_code == 200:
        print("✅ 成功潜入！服务器返回 200 OK")

        # 4. 解析战利品：把网页源代码交给 BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # 5. 提取数据：找到 <title> 标签里的文字
        # 你的博客标题应该藏在这里
        blog_title = soup.title.string
        print(f"\n🏆 抓取到的博客标题是：\n👉 {blog_title}")

        # 进阶：试着抓取所有文章的标题（Hexo 默认通常用 .post-title 类名）
        # 这里只是演示，如果没抓到说明你的主题类名不一样，那是正常的
        print("\n🔍 正在搜索首页的文章列表...")
        articles = soup.find_all('a', class_='post-title-link')
        for i, article in enumerate(articles):
            print(f"{i + 1}. {article.text.strip()}")

    else:
        print(f"❌ 哎呀，被发现了？状态码: {response.status_code}")

except Exception as e:
    print(f"💥 发生错误: {e}")