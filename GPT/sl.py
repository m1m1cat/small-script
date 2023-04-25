
import os
import time
import random
import requests
import logging
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from requests.exceptions import RequestException

# 配置文件
CONFIG = {
    'THREAD_NUM': 10,
    'RETRY_TIMES': 3, 
    'LOG_LEVEL': logging.INFO,
    'LOG_FILE': 'google.log'
}

# 日志配置
logging.basicConfig(level=CONFIG['LOG_LEVEL'], 
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
fh = logging.FileHandler(CONFIG['LOG_FILE'], mode='a', encoding='utf-8')
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)

# 随机User-Agent 
ua = UserAgent()
headers = {"User-Agent": ua.random}

# 定义代理类
class ProxyPool:
    def __init__(self):
        self.proxies = []
        self.proxy_file = 'proxies.txt'
        self.load_proxies(self.proxy_file)
        
    def load_proxies(self, path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.proxies.append(line)
                    
    def get_proxy(self):
        proxy = random.choice(self.proxies)
        proxies = {
            "http": "http://" + proxy,
            "https": "https://" + proxy
        }
        return proxies
    
# 自定义异常        
class SogouSpiderError(Exception):
    pass   

# 搜索引擎爬虫类    
class SogouSpider:
    def __init__(self, keyword, pages):
        self.keyword = keyword
        self.pages = pages
        self.init_proxies()
        self.urls = []
        
    def init_proxies(self):
        self.proxy_pool = ProxyPool()
        
    def get_search_url(self, page):
        start = page * 10
        return f'https://www.sogou.com/web?query={quote_plus(self.keyword)}&page={page+1}&ie=utf8&s_from=input&_ast=1111111111111&_asf=www.sogou.com&w=01019900&p={start}'
    
    def parse_result(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select('h3.tit a')
        for result in results:
            url = result['href']
            self.urls.append(url)  
                        
    def run(self):    
        for page in range(self.pages):
            retry_time = 0
            while retry_time < CONFIG['RETRY_TIMES']:
                try:
                    proxy = self.proxy_pool.get_proxy()
                    response = requests.get(self.get_search_url(page), headers=headers, proxies=proxy, timeout=5)
                    response.raise_for_status()
                    self.parse_result(response)
                    break
                except RequestException as e:
                    logger.error(f'代理失效,切换新代理, {e}')
                    retry_time += 1
                    if retry_time == CONFIG['RETRY_TIMES']:
                        logger.error(f'所有代理失效,放弃访问页面:{page}!')
                        raise SogouSpiderError('所有代理失效!')
                    continue
                except SogouSpiderError:
                    logger.error(f'访问页面{page}失败!')
                    break
            # 搜索结果页面之间随机延时3-8秒          
            time.sleep(random.randint(3,8))  
          
if __name__ == '__main__':
    keyword = input('输入搜索关键词:')
    pages = int(input('输入需要搜索的页面数:'))
    spider = SogouSpider(keyword, pages)
    try:
        spider.run()
        with open(f'{keyword}.txt', 'w') as f:
            for url in spider.urls:
                f.write(url+'\n')
        logger.info(f'搜索结果已保存至{keyword}.txt')
    except SogouSpiderError as e:
        logger.error(e)
