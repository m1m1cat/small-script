#!/usr/bin/env python3
# _*_encoding: utf-8_*_
# @Author:Cra5h Blog has Down
# 简易POC生成工具

import requests
import os

def main():
    #获取url
    url = input("Please enter the URL: ").strip()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    #检查协议头，没有则默认添加https://
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    #展示对应的请求方法选项
    method = input("Please enter the request method (1 for GET, 2 for POST, 3 for custom): ")
    while method not in ['1', '2', '3']:
        method = input("Invalid method. Please enter the request method (1 for GET, 2 for POST, 3 for custom): ")

    #根据选择进行操作
    if method == '1':
        path = input("Please enter the path: ").lstrip()
        response = requests.get(url + path, headers=headers)
    elif method == '2':
        path = input("Please enter the path: ").lstrip()
        data = input("Please enter the POST data: ").lstrip()
        response = requests.post(url + path, headers=headers, data=data)
    else:
        custom_method = input("Please enter the custom method: ")
        path = input("Please enter the path: ").lstrip()
        data = input("Please enter the POST data: ").lstrip()
        response = requests.request(custom_method, url + path, headers=headers, data=data)

    #打印响应结果
    print(response.content.decode())

    #增加选项 0. 退出
    choice = input("Please choose an option (0. Exit, 1. Modify URL, 2. Modify request method, 3. Generate POC.py): ")
    while choice not in ['0', '1', '2', '3']:
        choice = input("Invalid option. Please choose an option (0. Exit, 1. Modify URL, 2. Modify request method, 3. Generate POC.py): ")

    if choice == '0':
        return #退出程序
    elif choice == '1':
        main()
    elif choice == '2':
        main()
    else:
        #生成对应内容并写入poc.py
        file_name = "poc.py"
        script_dir = os.path.dirname(os.path.realpath(__file__)) #获取文件路径
        file_path = os.path.join(script_dir, file_name)  #生成poc.py保存到文件路径
        with open(file_name, "w") as f:
            f.write("import requests\n\n")
            f.write("url = '" + url + "'\n")
            if method == '1':
                f.write("path = '" + path + "'\n")
                f.write("headers = " + str(headers) + "\n")
                f.write("response = requests.get(url + path, headers=headers)\n")
            elif method == '2':
                f.write("path = '" + path + "'\n")
                f.write("headers = " + str(headers) + "\n")
                f.write("data = '" + data + "'\n")
                f.write("response = requests.post(url + path, headers=headers, data=data)\n")
            else:
                f.write("custom_method = '" + custom_method + "'\n")
                f.write("path = '" + path + "'\n")
                f.write("headers = " + str(headers) + "\n")
                f.write("data = '" + data + "'\n")
                f.write("response = requests.request(custom_method, url + path, headers=headers, data=data)\n")
            f.write("print(response.content.decode())\n")

if __name__ == '__main__':
    main()
