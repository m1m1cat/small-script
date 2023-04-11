#!/usr/bin/env python3
# -- coding utf-8 --
# @AuthorCra5h
# 地址存活验证

import aiohttp
import asyncio
import argparse
import re
import requests
from urllib.parse import urlparse


async def is_alive(session, uri, timeout):
    '''
    验证链接是否存活的函数，使用asyncio实现异步请求
    :param session: aiohttp的客户端会话对象
    :param uri: 验证链接
    :param timeout: 超时时间
    :return: 返回一个元组，包含链接、状态码和重定向链接（如果有）
    '''
    try:
        async with session.get(uri, allow_redirects=False, timeout=timeout) as resp:
            status = resp.status
            if status in [301, 302]:
                location = resp.headers.get('Location')
                return uri, status, location
            return uri, status, uri
    except:
        return uri, 0, uri


async def main(uris, timeout):
    '''
    用协程验证所有链接是否存活
    :param uris: 待验证的链接列表
    :param timeout: 超时时间
    :return: 返回一个元组列表，包含链接、状态码和重定向链接（如果有）
    '''
    async with aiohttp.ClientSession() as session:
        tasks = []
        for uri in uris:
            tasks.append(asyncio.ensure_future(is_alive(session, uri.strip(), timeout)))
        return await asyncio.gather(*tasks)


async def write_result(result, output_file):
    '''
    将验证结果写入文件
    :param result: 验证结果元组列表
    :param output_file: 输出文件名
    '''
    with open(output_file, 'w') as f:
        for uri, status, location in result:
            if location != uri:
                f.write(f'{uri} -> {location} - {status}\n')
            else:
                f.write(f'{uri} - {status}\n')


async def run(uris, timeout, output_file):
    '''
    主程序，运行协程，验证链接是否存活，并将结果写入文件
    :param uris: 待验证的链接列表
    :param timeout: 超时时间
    :param output_file: 输出文件名
    '''
    result = await main(uris, timeout)
    await write_result(result, output_file)


def main_cli():
    '''
    命令行接口函数，解析参数并执行主程序
    '''
    parser = argparse.ArgumentParser(description='Validate URLs in a text file')
    parser.add_argument('input_file', type=str, help='input file with URLs')
    parser.add_argument('output_file', type=str, help='output file with results')
    parser.add_argument('-t', '--timeout', type=float, default=5.0, help='timeout in seconds for each URL')
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        uris = f.readlines()

    for i in range(len(uris)):
        if not re.match(r'http[s]?://', uris[i]):
            uris[i] = 'https://' + uris[i]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(uris, args.timeout, args.output_file))


if __name__ == '__main__':
    main_cli()
