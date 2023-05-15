#!/bin/bash

# 定义测试速度的函数
test_speed() {
  url=$1
  echo "Testing download speed of $url ..."
  speed=$(curl -so /dev/null $url -w '%{speed_download}')
  printf "Download speed: %.2f Mb/s\n" $(echo "$speed / 1048576" | bc -l)
}


# 打印选择菜单
echo "请选择需要测速的Linux版本："
echo "1. CentOS"
echo "2. Ubuntu"
echo "3. Debian"
echo "4. RedHat"
echo "5. Deepin"
read -p "请选择（输入数字即可）: " choice

# 根据选择设置测试源
case $choice in
  1)
    urls=("http://centos.ustc.edu.cn/centos/7.9.2009/os/x86_64/Packages/centos-indexhtml-7-9.2009.0.el7.centos.noarch.rpm"
          "http://mirrors.aliyun.com/centos/7.9.2009/os/x86_64/Packages/centos-indexhtml-7-9.2009.0.el7.centos.noarch.rpm"
          "http://mirrors.163.com/centos/7.9.2009/os/x86_64/Packages/centos-indexhtml-7-9.2009.0.el7.centos.noarch.rpm"
          "http://mirrors.huaweicloud.com/centos/7.9.2009/os/x86_64/Packages/centos-indexhtml-7-9.2009.0.el7.centos.noarch.rpm")
    ;;
   2)
    urls=("http://archive.ubuntu.com/ubuntu/pool/main/b/bash/bash_4.4.18-2ubuntu1_amd64.deb"
          "http://mirrors.aliyun.com/ubuntu/pool/main/b/bash/bash_4.4.18-2ubuntu1_amd64.deb"
          "http://mirror.sjtu.edu.cn/ubuntu/pool/main/b/bash/bash_4.4.18-2ubuntu1_amd64.deb"
          "http://mirror.lzu.edu.cn/ubuntu/pool/main/b/bash/bash_4.4.18-2ubuntu1_amd64.deb"
          "http://mirror.neu.edu.cn/ubuntu/pool/main/b/bash/bash_4.4.18-2ubuntu1_amd64.deb")
    ;;
   3)
    urls=("http://ftp.debian.org/debian/pool/main/b/bash/bash_4.4-5_amd64.deb"
          "http://mirrors.aliyun.com/debian/pool/main/b/bash/bash_4.4-5_amd64.deb"
          "http://mirror.sjtu.edu.cn/debian/pool/main/b/bash/bash_4.4-5_amd64.deb"
          "http://mirror.lzu.edu.cn/debian/pool/main/b/bash/bash_4.4-5_amd64.deb"
          "http://mirror.neu.edu.cn/debian/pool/main/b/bash/bash_4.4-5_amd64.deb")
    ;;
    4)
    urls=("http://mirror.centos.org/centos/7/os/x86_64/Packages/centos-indexhtml-7-9.2009.0.el7.centos.noarch.rpm"
          "http://mirrors.aliyun.com/epel/7/x86_64/Packages/e/epel-indexhtml-7-1.noarch.rpm"
          "http://mirrors.163.com/epel/7/x86_64/Packages/e/epel-indexhtml-7-1.noarch.rpm"
          "http://mirrors.huaweicloud.com/epel/7/x86_64/Packages/e/epel-indexhtml-7-1.noarch.rpm")
    ;;
   5)
    urls=("https://packages.deepin.com/deepin/pool/non-free/d/deepin.com.qq.im.helper/deepin.com.qq.im.helper_1.1.0deepin8_i386.deb"
          "https://cdn-download.deepin.com/applications/deepin.com.qq.im.helper_1.1.0deepin8_i386.deb"
          "https://community-packages.deepin.com/deepin/pool/non-free/d/deepin.com.qq.im.helper/deepin.com.qq.im.helper_1.1.0deepin8_i386.deb"
          "https://community-store-packages.deepin.com/applications/deepin.com.qq.im.helper_1.1.0deepin8_i386.deb")
    ;;
   *)
    echo "无效选择"
    exit 1
esac

# 循环测试速度并输出结果
for url in "${urls[@]}"
do
  test_speed "$url"
done
