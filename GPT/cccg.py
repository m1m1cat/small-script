import os
import threading
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from requests.exceptions import RequestException, SSLError

# 错误日志控制
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# 设置自定义User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# 设置默认代理
default_proxies = {'http': 'http://127.0.0.1:7890', 'https': 'https://127.0.0.1:7890'}

# 用户输入Google语法和需要爬取的页面数和线程数
google_syntax = input("请输入Google语法：")
num_pages = int(input("请输入需要爬取的页面数："))
num_threads = int(input("请输入线程数（最高500）："))

# 获取代理地址
proxies_str = input("请输入代理地址（格式如http/s://127.0.0.1:7890），按回车键跳过：")
if proxies_str:
    proxies_list = proxies_str.split(",")
    proxies_dict = {}
    for p in proxies_list:
        p_type, p_addr = p.split("://")
        proxies_dict[p_type] = p
else:
    proxies_dict = default_proxies

# 对输入内容进行URL编码
google_syntax = quote_plus(google_syntax)

# 获取当前文件位置，创建结果文件夹
current_path = os.path.dirname(os.path.abspath(__file__))
result_dir = os.path.join(current_path, "result")
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# 定义爬取每个页面的函数
def crawl_url(urls, lock):
    with lock:
        with open(os.path.join(result_dir, "jieguo.txt"), "a", encoding="utf-8") as f:
            for url in urls:
                try:
                    res = requests.get(url, headers=headers, verify=True, proxies=proxies_dict)
                    res.raise_for_status()
                    soup = BeautifulSoup(res.content, "html.parser")
                    results = soup.select(".r a")
                    for result in results:
                        f.write(result["href"] + "\n")
                except SSLError as e:
                    logging.error("SSL错误: {}".format(e))
                    continue
                except RequestException as e:
                    logging.error("请求错误: {}".format(e))
                    continue


# 构造Google搜索URL列表
url_list = []
for i in range(num_pages):
    url = "https://www.google.com/search?q={}&start={}".format(google_syntax, i * 10)
    url_list.append(url)

# 分割URL列表并启动线程
threads = []
urls_per_thread = (len(url_list) + num_threads - 1) // num_threads  # 每个线程要爬取的URL数量
lock = threading.Lock()
for i in range(num_threads):
    start = i * urls_per_thread
    end = (i + 1) * urls_per_thread
    thread_urls = url_list[start:end]
    thread = threading.Thread(target=crawl_url, args=(thread_urls, lock))
    threads.append(thread)
    thread.start()

# 等待所有线程结束
for thread in threads:
    thread.join()

if os.stat(os.path.join(result_dir, "jieguo.txt")).st_size == 0:
    print("未抓取到任何网站URI！")
else:
    print("爬取完成！")
    with open(os.path.join(result_dir, "jieguo.txt"), "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip())
