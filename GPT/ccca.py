import os
import threading
import requests
from bs4 import BeautifulSoup

# 设置自定义User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# 用户输入Google语法和需要爬取的页面数
google_syntax = input("请输入Google语法：")
num_pages = int(input("请输入需要爬取的页面数："))

# 获取当前文件位置，创建结果文件夹
current_path = os.path.dirname(os.path.abspath(__file__))
result_dir = os.path.join(current_path, "result")
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# 定义爬取每个页面的函数
def crawl_url(url, thread_id):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    results = soup.select(".r a")
    with open(os.path.join(result_dir, "jieguo_{}.txt".format(thread_id)), "w", encoding="utf-8") as f:
        for result in results:
            f.write(result["href"] + "\n")

# 构造Google搜索URL列表
url_list = []
for i in range(num_pages):
    url = "https://www.google.com/search?q={}&start={}".format(google_syntax, i * 10)
    url_list.append(url)

# 定义线程数，最多500
num_threads = min(len(url_list), 500)

# 创建线程并启动
threads = []
for i in range(num_threads):
    thread_url_list = url_list[i::num_threads]  # 将URL列表按线程数分割
    thread = threading.Thread(target=crawl_url, args=(thread_url_list, i))
    threads.append(thread)
    thread.start()

# 等待所有线程结束
for thread in threads:
    thread.join()

print("爬取完成！")