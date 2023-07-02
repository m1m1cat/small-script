# 描述
该脚本是一个用于验证给定链接是否存活的Python脚本，使用了asyncio来实现异步请求。该脚本可以从一个文本文件中读取链接列表，验证每个链接的可用性，然后将验证结果写入另一个文本文件中。

# 用法

```
usage: http_alive.py [-h] [-t TIMEOUT] input_file output_file

Validate URLs in a text file

positional arguments:
  input_file            input file with URLs
  output_file           output file with results

optional arguments:
  -h, --help            show this help message and exit
  -t TIMEOUT, --timeout TIMEOUT
                        timeout in seconds for each URL
```
