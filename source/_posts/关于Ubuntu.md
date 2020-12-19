---
title: 关于Ubuntu
date: 2020-08-11 09:56:05
tags: ubuntu
---
关于Ubuntu使用的一些备忘。

<!-- More -->

## VM虚拟机与win10主机互相复制粘贴文件
```
sudo apt install open-vm-tools
sudo apt install open-vm-tools-desktop
```

## SSR

linux [ssr](https://github.com/qingshuisiyuan/electron-ssr-backup)

## 文件压缩

压缩
```
zip -r graphs.zip graphs
zip -r 123.zip abc.cpp def.txt
```

解压
```
unzip graphs.zip
```

tar命令

压缩
```
tar -cvf 123.tar file1 file2 dir1
```
解压

```
tar -xvf file.tar
tar -zxvf apache-tomcat-7.0.75.tar.gz 
```

## WSL 报错cannot execute binary file: Exec format

Bash On Windows(WSL)无法运行32Bit程序，报错cannot execute binary file: Exec format

```
sudo apt install qemu-user-static
sudo update-binfmts --install i386 /usr/bin/qemu-i386-static --magic '\x7fELF\x01\x01\x01\x03\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x03\x00\x01\x00\x00\x00' --mask '\xff\xff\xff\xff\xff\xff\xff\xfc\xff\xff\xff\xff\xff\xff\xff\xff\xf8\xff\xff\xff\xff\xff\xff\xff'
```

# WSL

子系统可以直接访问windows下的任何文件，这也是比虚拟机好用的关键点之一。在 /mnt 目录下就可以访问c、d、e、f等盘符，并且可以直接访问任何一个文件位置。

因为windows的盘符挂载到linux中的时候全部都用了 777 的权限，在一些软件开发上可能会出现一些问题。

* 使用wsl的自动挂载功能，修改 /etc/wsl.conf 文件
```C
[automount]
enabled = true
root = /mnt/
options = "metadata,dmask=022,fmask=133"
mountFsTab = false
```
就可以将/mnt下的所有盘都挂载为linux下默认的权限。
* windows wsl创建文件权限

挂载问题是解决了,但是使用wsl命令打开的终端创建新的文件还是 777。

在/etc/profile或~/.profile或~/.bashrc最后添加一些逻辑。
```C
if [[ "$(umask)" == '000' ]]; then
    umask 022
fi
```
这样在每次启动终端的时候就会重新设置umask, 之后创建文件就正常了。