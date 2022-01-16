---
title: linux
date: 2021-10-04 14:04:05
tags:
---

Linux 系统目录

* bin 二进制可执行文件
* boot 开机启动程序
* dev 设备文件
* home 普通用户
* etc:用户信息和系统配置文件 password group
* lib 库文件
* root 管理员宿主目录
* usr用户资源目录

文件类型：

* 普通文件 -
* 目录文件 d
* 字符设备文件 c
* 块设备文件 b
* 软连接 l
* 管道文件 p
* 套接字 s
* 未知文件

### 常用命令



* which:查看指定命令所在路径
* pwd： 查看当前所在路径
* rmdir:删除空目录
* rm : rm file `rm dir -rf` f强制删除
* cp 
* mv
* cat
* tac

软连接：快捷方式

`ln -s file file.s`创建软连接

为保证软连接可以随意移动，需保证用绝对路径创建

硬链接：

`ln file file.h`增加硬链接文件计数，共享Inode

* whoami

  `sudo su`切换root用户

* chmod 

  `chmod u+x a.c`给所有者添加可执行权限

  ```
  u表示用户
  g表示同组用户
  o表示其他用户
  a表示所有用户
  ```

  rwx r:4 w:2 x:1

  `chmod 471 a.c`

* chown

  `sudo chown new_user a.c`更改文件所有者

* adduser

  sudo adduser 新用户名

* addgroup 创建用户组

  `sudo addgroup g88`

* chgrp

  `sudo chgrp g88 a.c`

  `sudo chown nobody:nogroup a.c`同时修改用户和用户组

* deluser

  `sudo deluser wangwu`

* find

`find ./ -type 'l'`查找当前目录下软连接

`find ./ -name '*.jpg'`按文件名搜索

`find ./ -maxdepth 1 - name '*.jpg'`指定搜索层级

`find ./ -size +20M -size -50M`文件大小

`-atime -mtime -ctime`

`find ./ -ctime 1` 当天内修改过

`find /usr/ -name "*tmp*" -exec ls -l {} \;`

`find /usr/ -name "*tmp*" -ok rm -r {} \;`

* grep 找文件内容

  `grep -r 'copy' ./ -n` -n显示行号

* ps

  `ps aux` 

  `ps aux |grep 'kernel'`

find ./ -type f | xargs ls -l 

-xargs :将find搜索的结果集执行某一命令，当结果集数量过大时，可以分片映射

-print0:

`find /usr/ -name "*tmp*" -print0 | xargs print0 ls -l`

awk 按列拆分，sed按行拆分

* 软件安装：

`sudo apt-get update`更新软件源列表

卸载`sudo apt-get remove`

安装deb文件

sudo dpkg -i xx.deb

源码安装：

   1.解压缩代码包

2. cd dir

3. ./configure

   检测文件是否缺失，创建makefile，检测编译环境

4. make

   编译源码，生成库和可执行文件

5. sudo make install

   把库和可执行程序安装到系统路径下

6. sudo make distclean

   删除和卸载软件

压缩

* tar

  `tar zcvf 要生成的压缩包名 压缩材料` z: 调用gzip, c： creat, v：显示压缩过程，可以没有，f生成文件名

  先调用gzip 然后调用tar打包

* gzip

  `gzip 文件名`压缩一个文件

  `gzip a.c` 得到a.c.gz

* bzip2

  `tar jcvf test.tar.gz file1 dir2`

* 解压，将压缩命令中的c替换为x

* rar 

  `rar a -r newdir dir`

  解压

  `unrar x rartest.rar`

`sudo aptitude show tree`显示软件是否安装

* zip 

  `zip -r dir.zip dir`

  解压

  unzip dir.zip

* who 
* jobs当前后台运行的作业
* fg 前台
* bg后台
* kill
* env 环境变量
* top 任务管理器

设置密码

sudo passwd 用户名

切换用户

su 用户名

* ifconfig 查看ip地址
* man 查看手册

```
1.可执行程序或shell命令
2.系统调用
3.库调用
5.文件格式、规范
9.内核例程
```

* alias 起别名
* unmask 指定用户创建文件时的掩码
* 创建终端Ctrl+Shift +t
* 切换标签Alt+n
* 新开终端Ctrl+Shift + n

光标移动到第一个字符contrl+a

移动到最后一个字符contrl+e

清空输入control+u

空目录大小4096



### vim

* 命令模式i a o,I A O,s S切换到文本模式,:切换到末行模式，zz保存退出

  ```
  i:插入光标前一个字符
  I:插入行首
  a:插入光标后一个字符
  A:插入行末
  o:向下新开一行，插入行首
  O:向上新开一行，插入行首
  s:删除当前字符，插入
  S:删除当前行，插入
  ```

  

* 文本模式ESC切换到文本模式

* 末行模式w:保存 q:退出，两次ESC回到命令模式

```
h：左移
j:下移
k:上移
l:右移

跳转到指定行
1.88G(命令模式)
2.:88(末行模式)

跳转文件首：
gg(命令模式)

跳转文件尾
G(命令模式)

自动格式化程序：
gg=G(命令模式)

括号对应：
%(命令模式)

删除单个字符
x(命令模式)

删除单词
dw(光标置于首字母)

删除光标至行尾
D或d$

删除光标到行首
d0

光标移至行首
0

光标移至行尾
$

替换单个字符
r

删除指定区域：
按v切换为可视模式，使用hjkl来选中待删除区域，按d删除该区域数据

删除指定行
dd

删除指定N行
ndd

粘贴:
p粘至光标所在下一行
P粘在光标所在上一行

复制一行：
yy

复制多行：
nyy

查找
1.找设想内容
命令模式下，按“/”输入欲搜索关键字，回车，使用n检索下一个

2.找 看到的内容
将光标置于任意一个字符上，按“*、#”查找

单行替换
末行模式
:s /源字符串/替换字符串

通篇替换
末行模式
:%s /源字符串/替换字符串 只替换每一行首个
:%s /源字符串/替换字符串/g 替换所有

指定行替换
末行模式
:起始行号，终止行号s /源字符串/替换字符串/g 

撤销：
u

反撤销：
Ctrl + r

分屏
:sp 横屏分 Ctrl + ww切换
:vsp 竖屏分


跳转至man手册
将光标置于待查看函数单词，使用K跳转，(指定卷：nK

查看宏定义
将光标置于待查看宏定义单词，[ d

末行模式:! 执行shell 命令
```

配置vim

```
1. /etc/vim/vimrc
2. ~/.vimrc
~./vimrc优先级高
```



### gcc编译

预处理 gcc -E 展开宏、头文件，替换条件编译，删除注释、空白，空行

编译 gcc -S 检查语法规范 编译消耗时间最多

汇编：gcc -c将汇编指令翻译成机器指令

链接：无参数 数据段合并，地址回填

```
-I 指定头文件
头文件与.c文件不在同一目录
gcc -I ./inc hello.c -o hello

-c 只做预处理、编译、汇编

-g: 编译时添加调试信息

-On （n = 0-3） 编译优化

-Wall 提示更多警告信息

-D<DEF> 编译时定义宏
gcc hello.c -D HELLO
```

### 动态库、静态库

提高编译效率

静态库：对空间要求较低，对时间要求较高的核心程序

动态库：对时间要求较低，对空间要求较高

只做静态库的方法：静态库lib开头 .a结尾

```
ar rcs libmylib.a file1.o（得先编译成.o文件)
```

1.将.c生成.o文件

gcc -c add.c -o add.o

2.使用ar工具制做静态库

ar rcs libmymath.a add.o sub.o

编译错误会有行号信息，链接错误没有行号，显示ld returned 1 exit status

3.使用静态库：

`gcc test.c libmathlib.a -o test`

`gcc test.c ./lib/libmath.a -o a.out -I ./inc`

lib 存放.a文件

inc 存放相应头文件,必须有相应头文件，记录函数声明信息

```c
//防卫式声明
#ifndef _MYMATH_H_
#define _MYMATH_H_
int add(int,int);
int sub(int,int);
int div1(int,int);
#endif
```

动态库制作

1、将.c生成.o文件（生成与位置无关的代码 -fPIC）

```
gcc -c add.c -o add.o -fPIC
```

2.使用gcc -shared 制作动态库

gcc -shared -o lib库名.so add.o sub.o div.o

3.编译可执行程序时，指定所使用的动态库，-l指定库名，-L指定库路径

```
gcc test.c -o a.out -lmymath -L ./lib -I ./inc
```

4.运行可执行程序出错

原因：

链接器：工作于链接阶段，工作时需要-l,和-L

动态链接器：工作于程序运行阶段，工作时需提供动态库所在的目录地址

1.通过环境变量设置` export LD_LIBRARY_PATH = 动态库路径` 临时生效，重启终端环境变量失效 环境变量只与进程有关

2.

```bash
永久生效
1）
vi ~/.bashrc//改变bash环境变量
2）写入 export LD_LIBRARY_PATH= 动态库路径 保存
3）使环境变量生效
. .bashrc 或者 source .bashrc 或者 重启终端
```

`ldd a.out` 查看a.out 加载哪些动态库，及动态库路径

3.直接把动态库放到与标准c库一起，

 `cp libmymath.so /lib`

4. 配置文件法

   1）sudo vi /etc/ld.so.conf

   2）写入动态库绝对路径 保存

   3） sudo ldconfig -v 使配置文件生效

   ldd a.out 查看，失败not found

数据段合并

![image-20211004203908020](C:\Users\liule\AppData\Roaming\Typora\typora-user-images\image-20211004203908020.png)

连接时会把.text段和.rodata段合并,.data段和.bss段合并，节省空间

### gdb

-g 使用该参数编译可执行程序

gdb a.out

基础指令

```c
list: list 1 //列出源码。根据源码指定行号设置断点
b 52 //break 在52行设置断点
run/r //run
n/next //next,下一条指令，如果当前断点是函数则不进入函数
s/step //step，下一条指令，进入函数
p/print :p i//print i
continue: 继续执行断点后续指令
quit: 退出gdb当前调试
```

其他指令：

```c
使用run查找段错误位置
finish 结束当前函数调用，回到调用点
start 启动调试
    
set args 设置命令行参数
run 后面也能加命令行参数
run argv[1] argv[2]
       
info b 断点信息表
    
b 41 if i = 4 //条件断点
    
ptype j //查看变量类型
    
bt/backtrace 查看栈帧信息

frame 1 切换栈帧
    
display i //设置追踪i

undisplay 编号//取消跟踪变量
    
delete 删除断点
```

栈帧：随着函数调用而在stack上开辟的一片内存空间，用于存放函数调用而产生的局部变量和临时值

### Makefile

* 1个规则

 ```makefile
 目标：依赖条件
 	（一个tab缩进）命令
 test: test.c
 	gcc -o test test.c
 
 hello: hello.o
 	gcc hello.o -o hello
 	 
 hello.o:hello.c
 	gcc -c hello.c -o hello.o 
 ```

all:指定makefile的终极目标

1、目标的时间必须晚于依赖条件的时间，否则，更新目录

2、依赖条件不存在，找寻新的规则去产生依赖



* 2个函数

  wildcard 

  patsubst

  ```makefile
  src = $(wildcard ./*.c)
  #找到当前目录所有后缀为.c的文件赋值给src,将文件名组成列表赋值给变量src
  
  obj = $(patsubst %.c %.o $(src))
  #将参数3中，包含参数1的部分，替换为参数2
  #把src变量里所有后缀为.c的文件替换为.o
  
  clean:#(没有依赖)
  	-rm -rf $(obj) a.out #-rm 出错依然执行
  ```

  make clean -n//尝试执行，但不真正执行

  

  

* 3个自动变量

```makefile
$@:在规则的命令中表示规则中的目标
$<：在规则的命令中，表示第一个依赖条件,如果将该变量应用在模式规则中，它可将依赖列表中的依赖依次取出，套用规则
$^：在规则的命令中，表示所有依赖条件

src = $(wildcard *.c)# add.c sub.c hello.c
obj = $(subsubst %.c %.o $(src))# add.o sub.o hello.o

All:a.out

a.out:$(obj)
	gcc $^ -o $@

add.o:add.c
	gcc -c $< -o $@

sub.o: sub.c
	gcc -c $< -o $@

hello.o: hello.c
	gcc -c $< -o $@

clean:
	-rm -rf $(obj) a.out
```

模式规则：

```makefile
src = $(wildcard *.c)# add.c sub.c hello.c
obj = $(subsubst %.c %.o $(src))# add.o sub.o hello.o

All:a.out

a.out:$(obj)
	gcc $^ -o $@

%.o:%.c
	gcc -c $< -o $@
	
clean:
	-rm -rf $(obj) a.out
```

静态模式规则

```makefile
$(obj):%.o:%.c
	gcc -c $< -o $@
```

生成伪目标

```makefile
.PHONY:clean ALL
```

调加参数

```makefile
myArgs = -Wall -g
a.out:$(obj)
	gcc $^ -o $@ $(myArgs)

%.o:%.c
	gcc -c $< -o $@ $(myArgs)
```

makefile 名字为m1

```bash
make -f m1
```

参数：

-n模拟执行make,make clean 命令

-f：指定文件执行make命令

### 文件IO

系统调用

* open 函数

```c
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
char *strerror(int num);//根据error num 返回错误信息
int open(const char *pathname,int flags);//O_RDONLY O_WRONLY ORDWR O_CREAT O_APPEND O_EXCL（检查文件是否存在） O_TRUNC（把文件清零） O_NONBLOCK
int open(const char *pathname,int flags,mode_t mode);//不是C语言支持重载，而是open支持可变参数
//返回新的文件描述符，错误返回-1，并设置errno
//mode_t 8进制整数 读写执行权限，需要创建时指定，同时权限受unmask限制 mode&~unmask

int close(int fd);
```



```c
ssize_t read(int fd,void *buf,size_t count);//count缓冲区大小
//成功返回读取得到的字节数,失败返回-1
//-1 并且errno = EAGIN 或EWOULDBLOCK说明不是read失败，而是read在以非阻塞方式读一个设备文件(网络文件），并且文件无数据
ssize_t write(int fd,const void * buf,size_t count);//count实际写出内容的大小
```

```c
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char *argv[]){
    char buf[1024];
    int n = 0;
    int fd1 = open(argv[1],O_RDONLY);
    if(fd1 == -1){
        perror("open argv1 error");
        exit(1);
    }
    int fd2 = open(argv[2],O_RDWR|O_CREAT|O_TRUNC,0664);
    if(fd1 == -1){
        perror("open argv2 error");
        exit(1);
    }
    while((n = read(fd1,buf,1024))!= 0){
        write(fd2,buf,n);
    }
    close(fd1);
    close(fd2);
    return 0;
}
#include<stdio.h>
void perror(const char *s);
```

strace 跟踪程序运行时所进行的系统调用

系统缓冲区

read write无缓冲IO

预读入缓输出

* 文件描述符

  ```c
  stdin 0 STDIN_FILENO
  stdout 1 STDOUT_FILENO
  stderr 2 STDERR_FILENO
  ```

  最多1024个，新建文件描述符是目前进程最小可用的描述符

* 阻塞、非阻塞:

  阻塞是设备文件、网络文件的属性

  读常规文件是不会阻塞的

  产生阻塞的场景：读设备文件，读网络文件

  /dev/tty --终端文件

```c
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
int main(){
        char buf[10];
        int fd,n;
        fd = open("/dev/tty",O_RDONLY|O_NONBLOCK);
        if(fd < 0){
            perror("open /dev/tty");
            exit(1);
        }
    tryagain:
        n = read(STDIN_FILENO,buf,10);
        if(n < 0){
            if(errno != EAGAIN){
                perror("read STDIN_FILENO");
                exit(1);
            }else{
                write(STDOUT_FILENO,"try again\n",strlen("try again\n"));
                sleep(2);
                goto tryagain;
            }
        }
        write(STDOUT_FILENO,buf,n);
        return 0;
}
```

* fcntl函数

```c
int fcntl(int fd,int cmd,.../*arg*/);

int main(void){
    char buf[10];
    int flags,n;
    flags = fcntl(STDIN_FILE,F_GETFL);//获取stdin属性信息
    if(flags == -1){
        perror("fcntl error");
        exit(1);
    }
    flags |= O_NONBLOCK;
    int ret = fcntl(STDIN_FILENO,FSETFL,flags);
    if(ret == -1){
        perror("fcntl error");
        exit(1);
    }
}
```

获取文件状态 F_GETFL

设置文件状态 F_SETFL

* lseek

  ```c
  off_t lseek(int fd,off_t offset,int whence);
  whence //SEEK_SET SEEK_SET SEEK_END
  ```

  1. 文件读写使用同一偏移位置

  2. 使用lseek获取、
  3. 拓展文件大小，要使文件大小真正发生变化，需要发生IO操作 

  ```c
  int trunate(const char *path, off_t length);//拓展一个现有文件大小
  ```

  

od -tcx filename 查看文件的16进制表示

od -tcd filename 查看文件的10进制表示

* 传入参数

  1.指针作为函数参数

  2.const 修饰

  3.指针指向有效区域，在函数内部做读入操作

* 传出参数

  1.指针作为函数参数

  2.指针指向的空间可以无意义，但有效

  3.函数对其进行写操作

  4.函数调用后，充当返回值

* 传入传出参数

  1.指针作为函数参数

  2.在函数调用前，指针指向的空间有意义

  3.在函数内部，先读后写

  4.函数调用结束后，充当函数返回值

  

* inode 本质为结构体，存储文件属性信息

* dentry 目录项： 文件名、inode号 硬链接，相同inode,不同dentry

* stat 获取文件属性 (从inode中获取)

  ```c
  #include<sys/stat.h>
  int stat(const char *path,struct stat * buf);
  参数：
      path:文件路径
       buf:传出参数，存放文件属性
  获取文件大小： buf.st_size
  获取文件类型： buf.st_mode
  获取文件权限： buf.st_mode
  ```

  stat符号穿透，stat检查符号链接时，直接获取符号链接引用的真正文件信息

  lstat不会进行符号穿透

  vim,cat会穿透符号链接，ls -l 不会

* link 函数：创建硬链接

  ```c
  int link(const char *oldpath,const char *newpath);
  ```

* unlink 函数:删除一个文件的目录项

  ```c
  int unlink(const char * pathname);
  ```

  unlink :如果文件硬链接数到0了，但该文件仍不会马上释放，需等到所有打开该文件的进程关闭

* symlink创建符号链接

  ```c
  int symlink(const char *oldpath,const char * newpath);
  ```

  readlink读软连接本身

  ```c
  readlink t.soft
  ```

* readlink

  ```c
  ssize_t readlink(const char * path,char * buf,size_t bufsize);
  ```

* rename

  ```c
  int rename(const char *oldpath,const char * newpath);
  ```

* getcwd:获取工作目录

  ```c
  char *getcwd(char * buf,size_t size);
  ```

* chdir：改变工作目录

  ```c
  int chdir(const char * path);
  ```

* 文件权限

  r:目录可以被浏览

  w:创建删除修改文件

  x:可以被进入

* opendir函数 库函数

  ```c
  #include<dirent.h>
  DIR*opendir(const char *name);
  ```

* closedir

  ```c
  int closedir(DIR *dirp);
  ```

* readdir

  ```c
  struct dirent *readdir(DIR*dirp);
  ```

  ```c
  #include <stdio.h>
  #include <stdlib.h>
  #include <string.h>
  #include <unistd.h>
  #include <dirent.h>
  
  int main(int argc,char * argv[]){
      DIR *dp;
      struct dirent *sdp;
      dp = opendir(argv[1]);
      if(dp == NULL){
          perror("opendir error");
          exit(1);
      }
      while((sdp = readdir(dp)) != NULL){
          printf("%s\t",sdp->d_name);
      }
      printf("\n");
      close(dp);
      return 0;
  }
  ```

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
void isFile(char * name);
void readdir(char *dir){
    DIR *dp = opendir(dir);
    if(dp == NULL){
        perror("opendir");
        exit(-1);
    }
    struct dirent *sdp;
    char name[256];
    while((sdp = readdir(dp))!= NULL){
        if(sdp->d_name[0] == '.'){
            continue;
        }
        sprintf(name,"%s/%s",dir,sdp->d_name);
        isFile(name);
    }
}
void isFile(char * name){
    int ret = 0;
    struct stat sb;
    ret = stat(name, &sb);
    if(ret == -1){
        perror("stat");
        exit(-1);
    }
    if(S_ISDIR(sb.st_mode)){
        readdir(name);
    }
    printf("%s\t%ld\n",name,sb.st_size);
    return;
}
int main(int argc,char * argv[]){
    if(argc == 1){
        isFile(".");
    }else isFile(argv[1]);
    return 0;
}


```

* dup

```c
int dup(int oldfd);
oldfd:已有文件描述符
newfd:新文件描述符
    
int dup2(int oldfd,int newfd);
把旧的复制给新的，返回newfd
newfd指向和oldfd一致
```

```c
int newfd = fcntl(fd1,F_DUPFD,0);//0被占用，fcnt使用文件描述符表最小可用文件描述符返回
int newfd = fcntl(fd1,F_DUPFD,7);//7未被占用，可以被使用
```

### 进程

* 进程：占用内存、cpu等系统资源

* PCB

  进程id

  进程状态：就绪，运行，挂起，停止

  进程切换时需要保存和恢复的一些寄存器值

  描述虚拟地址空间信息

  描述控制终端的信息

  当前工作位置

  文件描述符表

  和信号相关信息

  用户id和组id

  会话和进程组

  进程可以使用的资源上限

  

* 环境变量

PATH SHELL TERM LANG HOME `echo $PATH`

* 进程控制

  ```c
  pid_t fork(void);
  ```

  ```c
  pid_t getpid(void);
  pid_t getppid(void);
  uid_t getuid(void);
  gid_t getgid(void);
  ```

* 进程共享

  刚发生父子进程fork之后

  全局变量，.data,.text,栈，堆，环境变量，用户ID，宿主目录，进程工作目录，信号处理方式相同

  不同：

  进程id,fork返回值，父进程id，进程运行时间，闹钟（定时器），未决信号集

  读时共享，写时复制

  父子进程共享 文件描述符，mmap映射区

* gdb调试

  ```c
  set follow-fork-mode child 跟踪子进程
  set follow-fork-mode parent
  ```

* exec函数族

  将当前进程的.text、.data替换为所要加载的程序的.text、.data，然后让进程从新的.text第一条指令开始执行，但进程id不变

  ```c
  int execl(const char *path,const char * arg,...);
  int execlp(const char *file, const char *arg,...);
  int execvp(const char *file, char const * argv[]);
  
  ```

  execlp，加载一个进程，借助PATH环境变量

  ```c
  execlp("ls","ls"/*相当于argv[0],没啥用*/,"-l","-h",NULL);//只有execlp出错时才返回-1，否则之后代码不再执行
  perror("exec error");
  exit(-1);
  ```

  

  ```c
  execl("./a.out","./a.out");
  ```

  只有execve是系统调用

* 孤儿进程

  父进程先于子进程结束，子进程的父进程将成为init进程

* 僵尸进程

  进程终止，父进程尚未收回，子进程残留资源（PCB)存放于内核中，变为僵尸进程

* wait函数（waitpid(-1,&status,0);)

  阻塞等待子进程退出

  回收子进程残留资源

  获取子进程结束状态

  ```c
  pid_t wait(int *status);
  WIFEXITED(status)
      return true if the child terminated normally
  WEXITSTATUS(status)
      return the exit status of the child
  WIFSIGNALED(status)
      return true if the child process was terminated by a signal
  WTERMSIG(status)
         return the number of the signal that caused the child process to terminate
          
  ```

* waitpid

  ```c
  pid_t waitpid(pid_t pid,int * status,int options);//一次wait/waitpid函数调用，只能回收一个子进程
  正常回收返回pid
  如果设置WNOHANG，子进程未结束，返回0
  -1：失败返回-1
  ```
  
  

### IPC

文件，管道，共享内存，消息队列，套接字，命名管道

管道（使用最简单，匿名管道只能用于有血缘关系的进程之间，要共享文件描述符）

信号（开销小，表示信息有限）

共享映射区（无血缘关系）

本地套接字（最稳定，实现复杂度最高）

* 管道

  pipe函数创建 mkfifo 创建有名管道（伪文件不占用磁盘空间）

  1. 其本质上是一个伪文件
  2. 由两个文件描述符引用，一个表示读端，一个表示写端
  3. 规定数据从管道写段流入，从读端写出

  管道的原理，管道是为内核使用环形队列机制，借助内核缓冲区（4k)实现

  局限性：自己写，不能自己读

  ​              数据不可反复读

  ​              半双工通信

  ​              只能在有血缘关系的进程之间使用

  pipe函数：创建并打开管道

  ```c
  int pipe(int fd[2]);
  参数:fd[0]读端
      fd[1]写端
  返回：0 成功 -1失败
  ```

* 管道的读写行为

  1. 读管道 

     * 管道有数据，read返回实际读到的字节数

     * 管道中无数据

       管道写端全部关闭，read返回0(读到文件结尾)

       写端没有全部关闭，read阻塞等待

  2. 写管道：

     * 管道写端全部关闭，进程异常终止，SIGPIPE

     * 管道写端没有全部关闭

       管道已满，write阻塞

       管道未满，write将数据写入，并返回实际写入字节数

  可以有一个写端，多个读端，或者一个读端，多个写端

* ulimit -a 查看打开文件个数，pipe缓存区大小

  ```c
  #include <unistd.h>
  long fpathconf(int fd,int name);
  ```

* FIFO命名管道

  解决没有关系进程之间的通信

  ```bash
  mkfifo myfifo
  ```

  ```c
  int mkfifo(const char *pathname,mode_t mode);
  ```

* 文件进程通信

* 存储映射IO

  ```c
  void *mmap(void *addr,size_t length,int prot,int flags,int fd,off_t offset);//创建共享内存
  参数：
      addr：指定映射区的首地址，通常传NULL,表示让系统自动分配
      length:共享内存大小（<=文件实际大小）
      prot:共享内存映射区的读写权限 PROT_READ PROT_WRITE PROT_NONE PROT_EXEC
      flags:标志共享内存共享属性：MAP_SHARED MAP_PRIVATE（对内存的修改不会反应到磁盘上）
      fd:用于创建共享内存映射区的文件描述符
      offset：默认0，表示映射文件全部，偏移位置，必须是4k的整数倍
          
  返回值：
          成功：映射区首地址
          失败： MAP_FAILED,(void*)-1
  
  int munmap(void *addr,size_t length);释放映射区
  addr:mmap返回值
  length:大小
  
  #include <stdio.h>
  #include <stdlib.h>
  #include <unistd.h>
  #include <string.h>
  #include <sys/mann.h>
  #include <fcntl.h>
  void sys_err(const char * s){
      perror(s);
      exit(1);
  }
  int main(int argc,char * argv[]){
      char *p = NULL;
      int fd;
      fd = open("testmp",O_RDWR|O_CREAT|O_TRUNC,0644);
      if(fd == -1){
          sys_err("open error");
      }
      /*
      lseek(fd,10,SEEK_END);
      write(fd,'\0',1); //相当于ftruncate()
      */
      ftruncate(fd,20);//需要写权限
      int len = lseek(fd,0,SEEK_END);
      p = mmap(NULL,len,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);
      if(p == MAP_FAILED){
          sys_err("mmap error");
      }
      strcpy(p,"hello mmap");
      printf("---%s\n",p);
      int ret = munmap(p,len);
      if(ret == -1){
          sys_err("munmap error");
      }
      return 0;
  }
  ```

* 注意事项

  1.用于创建映射区文件大小为0，实际指定非零大小创建映射区，会造成SIGBUS

  2.用于创建映射区文件大小为0，实际指定0大小创建映射区，invalid argument

  3.用于创建映射区的文件读写属性为只读，实际mmap指定写，会造成invalid argument

  4.创建映射区隐含一次read操作，需要read权限，mmap读写权限，映射区访问权限为SHARED时，应该不超过文件的open权限，文件只读open没发建立映射区

  5.文件描述符fd在mmap创建后即可关闭，后续文件可以通过地址访问

  6.offset必须是4k整数倍（MMU映射的最小单位为4k)

  7.对申请的内存越界访问未定义

  8.munmap释放的地址，必须是mmap申请的地址

  9.映射区访问权限为私有，对内存的修改只跟内存有关，跟磁盘无关

  10.映射区访问权限为私有，只需要open文件时有读权限，用于创建映射区即可

* mmap

  1.open("文件名",O_RDWR)

  2.mmap(NULL,有效文件大小，PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);

* 父子间mmap通信，需设置flag为MAP_SHARED，否则父子进程各有一份映射区

  父进程先创建映射区open（O_RDWR) mmap(MAP_SHARED)

  指定MAP_SHARED权限

  fork()创建子进程

  一个进程读，一个进程写

* 无血缘关系进程之间mmap通信

  两个进程打开同一个文件，创建映射区

  指定flags为MAP_SHARED

  一个进程写入，另一个进程读出，同一个文件mmap映射区是同一个位置

  无血缘关系进程间通信 mmap：数据可以重复读取

  ​                                       fifo:数据只能一次读取

* 匿名映射：只能用于有血缘关系进程之间通信

  使用MAP_ANONYMOUS（或者MAP_ANON)

  ```c
  int *p = mmap(NULL,4,PROT_READ|PROT_WRITE,MAP_SHARED|MAP_ANONYMOUS,-1,0);
  //fd -1
  ```

  不支持ANONYMOUS的操作系统，可以打开/dev/zero，大小想要多大有多大

  /dev/null

### 信号

简单，不能携带大量信息，满足某个特设条件才发送

信号的特质：

信号时软件层面的中断，一旦信号产生，无论程序执行到什么位置，必须立即停止运行，处理信号，处理结束，再继续执行后续指令

所有信号的产生和处理都是内核完成的

产生信号：

1. 按键产生，Ctrl+C Ctrl + Z Ctrl + \
2. 系统调用产生 kill raise abort
3. 软件条件产生，定时器alarm sleep借助alarm实现
4. 硬件异常产生，非法访问内存（段错误）、除零，内存对齐出错（总线错误）
5. 命令产生kill命令

递达：递送并到达进程,直接被处理掉

未决：产生和抵达之间的状态，主要由于阻塞（屏蔽）导致该状态

信号处理方式：

1。执行默认动作

2.忽略（丢弃）

3.捕获（调用户处理函数）

* 阻塞信号集（信号屏蔽字）：本质：位图，用来记录信号的屏蔽状态，将某些信号加入集合，对他们设置屏蔽，当屏蔽信号x后，再收到该信号，该信号的处理将推后（解除屏蔽后）

* 未决信号集,本质：位图，用来记录信号的处理状态

  信号产生，未决信号集中描述该信号的位立即翻转为1，表信号处于未决状态，当信号被处理对应位翻转回0

  信号产生后由于某些原因不能抵达（主要是阻塞），这类信号的集合称之为未决信号集，在屏蔽解除时，信号一直处于未决状态

kill -l 列出所有信号

0-31常规信号：都有默认的处理事件和处理动作

34-64实时信号 ：没有默认事件

* 信号4要素

  1.编号，2.名称 3.信号对应的事件 4.默认处理动作

  man 7 signal

  SIGHUB 用户退出shell

  SIGQUIT <ctrl+\>

  SIGINT <ctrl+c>终止进程

  SIGKILL 无条件终止进程，不能被忽略，处理，阻塞

  SIGSTOP停止进程的执行，不能忽略，处理，阻塞

  SIGUSR1，SIGUSR2没有默认处理事件，处理动作是终止进程

  SIGTERM, kill命令发送的信号，终止进程（不带信号编号）

  SIGCHLD:子进程状态发生变化时，父进程接收这个信号，默认动作为忽略这个信号

  SIGTSTP：停止中断交互进程的运行<ctrl+z>

* 默认动作

  Term：终止进程

  Ign忽略信号

  Core:终止进程，生成Core文件

  Stop:停止（暂停）进程

  Cont:继续运行进程

  

  ```c
  #include <signal.h>
  int kill(pid_t pid,int sid);
  pid > 0 杀死指定进程
     = 0 杀跟调用kill函数的进程处于同一进程组的所有组员
      <-1 取绝对值，发送信号给该绝对值所对应的进程组的所有组员
      =-1 发送信号给有权限的所有进程
  ```

  ps ajx查看进程组信息

  kill -SIGKILL -1杀死所有有权限的进程

  发送者实际有效ID == 接收者实际有效ID

* 其他几个发信号函数

  ```c
  int raise(int sig);//发送信号给调用者
  void abort(void);
  ```

  alarm函数

  设置定时器，（闹钟）指定seconds后，发送SIGALRM信号，进程接收到该信号，默认动作终止

  每个进程有且只有唯一定时器

  ```c
  unsigned int alarm(unsigned int seconds);
  返回值：无错误
  ```

  取消定时器alarm(0)返回旧闹钟剩余秒数

  定时，与进程状态无关

  time指令 查看程序执行的时间`time ./alarm`

  实际执行时间=系统时间+用户时间+等待时间

  setitimer函数，可以实现周期定时

  ```c
  int setitimer(int which,const struct itimerval *new_value,struct itimerval *old_value);
  new_value 定时秒数
  old_value 传出参数，上次定时剩余时间
  struct itimerval{
      struct timeval it_interval;/*next value*/
      struct timeval it_value;/*current value*/
  };
  struct timeval{
      time_t tv_sec;/*seconds*/
      suseconds_t tv_usec;/*microseconds*/
  }
  struct itimerval new_t;
  new_t.it_interval.tv_sec = 1;
  new_t.it_interval.tv_usec = 0;
  it_interval 用来设定两次定时任务之间的间隔时间
  it_value 定时的时长
  /*
  which
  自然计时：ITIMER_REAL ->14)SIGLARM
  虚拟空间计时（用户空间）ITIMER_VIRTUAL—>26)SIGVTALRM 计算占用cpu时间
  运行时计时（用户+内核）ITIMER_PROF->27)SIGPROF 计算占用cpu及执行系统调用的时间
  */
  成功0，失败-1
  ```

* 信号集操作函数

  只可以操作阻塞信号集

  ```c
  sigset_t set;//typedef unsigned long sigset_t;
  int sigemptyset(sigset_t*set);//将某个信号集清零
  int sigfillset(sigset_t*set);//将某个信号集置为1
  int sigaddset(sigset_t*set,int signum);//将某个信号加入信号集
  int sigdelset(sigset_t*set,int signum);//删除某个信号
  int sigismember(const sigset_t*set,int signum);//判断信号是否在信号集，在返回1，不在返回0
  ```

  sigprocmask函数

  可以用来屏蔽信号，解除屏蔽

  ```c
  int sigprocmask(int how,const sigset*set,sigset*oldset);//成功0，失败-1
  set传入参数，是一个位图
  oldset传出参数，保存旧的信号屏蔽集
  how参数取值：假设当前信号的屏蔽字为mask
     SIG_BLOCK:set表示需要屏蔽的信号，mask = mask|set
     SIG_UNBLOCK:set表示需要解除的信号，相当于mask = mask&~set
     SIG_SETMASK,替换原来的mask mask = set
  ```

  sigpending函数

  读取当前进程未决信号集

  ```c
  int sigpending(sigset_t *set);//set传出参数
  ```

* 信号捕捉

  signal函数

  注册一个信号捕捉函数

  ```c
  #include <signal.h>
  typedef void (*sighandler_t)(int);
  sighandler_t signal(int signum,sighandler_t handler);
  
  ```

  sigaction函数

  ```c
  int sigaction(int signum,const struct sigaction*act,struct sigaction *oldact);
  struct sigaction{
      void (*sa_handler)(int);
      void (*sg_sigaction)(int,siginfo_t*,void *);//发送信号携带复杂信息
      sigset_t sa_mask;//只工作于信号捕捉工作时间之中，绝大时候传0
      int sa_flags;//设置参数，绝大时候传0
      void (*sa_restorer)(void);//废弃
  };
  ```

* 信号捕捉特性

  1.进程正常运行时，默认PCB有一个信号屏蔽字，假定为mask，它决定了进程自动屏蔽哪些信号，当注册了某个信号捕捉函数，捕捉到该信号之后，要调用该函数，而该函数有可能执行很长时间，这期间所屏蔽的信号不由mask指定，而由sa_mask指定，调用完信号处理函数，再恢复为mask

  2.xxx信号捕捉函数执行期间，相同信号自动被屏蔽

  3.阻塞的常规信号不支持排队，产生多次只记录一次

* 内核实现信号捕捉

  1.在执行主控制流程的某条指令时因为中断、异常或系统调用进入内核（用户态）

  2.内核处理完异常准备回用户模式之前先处理当前进程中可以递送的信号

  3.do_signal()如果信号的处理动作有自定义的信号处理函数则回到用户模式执行信号处理函数

  4.信号处理函数返回时执行特殊的系统调用sigreturn再次进入内核（用户态）函数调用之后需要返回调用者

  5.sys_sigreturn()返回用户模式，从主控制流程中上次被中断的地方继续向下执行

* SIGCHID产生条件

  子进程终止时

  子进程接收到SIGSTOP信号停止时

  子进程处于停止态，接收到SIGCONT后唤醒

  ```c
  void catch_child(int signo){
      pid_t wpid;
      int status;
      while((wpid = waitpid(0,&status,WNOHANG))> 0){//防止因为处理SIGCHID期间屏蔽SIGCHID，造成一些子进程的SIGCHID丢失导致未回收
         if(WIFEXITED(status))//正常退出
  			printf("child %d exit %d\n", pid, WEXITSTATUS(status));
  		else if(WIFSIGNALED(status))//被信号退出
  			printf("child %d cancel signal %d\n", pid, WTERMSIG(status));
      }
      return;
  }
  ```

* 中断系统调用

  1.慢速系统调用：可能会使进程永远阻塞的系统调用，如果阻塞期间收到一个信号，该系统调用就被中断，不再执行，也可设定系统调用是否重启

  2.其他系统调用：getpid getppid fork

  慢速系统调用被中断的相关行为，实际上就是pause行为

  

  可修改sa_flags来设置被信号中断后系统调用是否重启SA_INTERRURT不重启，SA_RESTART重启
  
* 会话

  多个进程组的集合

  setid函数

  创建一个会话，并以自己的ID设置进程组ID，同时也是会话的ID

  ```c
  pid_t setsid(void);//成功返回0，失败-1并设置errno
  调用setid函数的进程，既是新会长，也是新组长
  ```

### 守护进程

daemon 进程，Linux后台服务进程，通常独立于控制终端，并且周期性执行某种任务，或等待某些发生的事件。通常采用以d结尾的名字

通常运行于操作系统后台，脱离控制终端，一般不与用户进行交互，周期性等待某个事件发生或者周期性执行某一动作

不受用户登录注销影响，通常采用以d结尾的命名方式

创建守护进程：

* 创建子进程，父进程退出

  所有工作在子进程中进行，形式上脱离了控制终端

* 在子进程中创建会话

  setsid()函数

  使子进程完全独立出来，脱离控制

* 改变当前目录为根目录

  chdir()函数

  防止占用可卸载文件系统

  也可换成其他路径

* 重设文件权限掩码

  umask()函数

  防止继承的文件创建屏蔽字拒绝某些权限

  增加守护进程灵活性

* 关闭/重定向文件描述符

  0，1，2，继承打开文件不会用到，浪费系统资源，无法卸载

* 开始执行守护进程核心工作，守护进程退出处理程序模型

### 线程

进程:独立地址空间，拥有PCB，最小资源分配单位

线程：有独立PCB，但没有独立地址空间，最小执行单位

ps -Lf pid -->线程号

页目录（首地址在PCB中），页表，页面

* 轻量级进程，也有PCB，创建线程使用的底层函数和进程一样，都是clone
* 从内核看线程和进程一样的，但PCB所指的三级页表相同
* 进程可以蜕变成线程
* 线程可以看成是寄存器和栈的集合
* 在linux下，线程是最小的执行单位，晋城市最先的资源分配单位

线程共享资源

* 文件描述符表
* 每个信号处理方式
* 当前工作目录
* 用户id,组id
* 内存地址空间

线程非共享资源

* 线程id
* 处理器现场和栈指针（内核栈）
* 独立的栈空间
* errno变量
* 信号屏蔽字
* 调度优先级

线程优缺点：

* 提高程序并发性
* 开销小
* 数据通信，共享数据方便

缺点：

* 库函数，不稳定
* 调试，编写困难，gdb不支持
* 对信号支持不好

#### 线程控制原语

* pthread_self函数

获取线程id,其作用对应进程的getpid()函数

```c
pthread_t pthread_self(void);
线程ID：pthread_t类型，本质在linux下为无符号整型，其它系统有可能是结构体
线程ID是进程内部识别标志，(两个进程间可以有线程ID相同)
线程号：标识线程身份，交给CPU选择调度时间
```

* pthread_create

```c
int pthread_create(pthread_t *thread,const pthread_attr_t *attr,void*(*start_routine)(void*),void *arg);//成功返回0，失败返回错误号
thread 传出参数，新创建线程的子线程id
attr 线程属性,NULL表示默认参数
start_routine 回调函数
arg 回调函数所需要的参数
传参采用值传递，借助强转
(void*)i//不可是(void*)&i
```

* pthread_exit

```c
void pthread_exit(void *retval);//将当前线程退出
retval 退出值，无退出值时，NULL
```

* pthread_join函数

  阻塞等待线程退出，获取线程退出状态，对应进程中的waitpid()函数

  ```c
  int pthread_join(pthread_t thread,void ** retval);成功0，失败错误号
  thread 线程ID
  retval记录线程结束状态
  ```

* pthread_cancel函数

  ```c
  int pthread_cancel(pthread_t thread);
  ```

  

  杀死线程,cancel杀死进程需要到达一个取消点(保存点)（系统调用

  子线程没发生系统调用，须要子线程自己添加取消点

  ```c
  pthread_testcancel();
  ```

  如果子线程没有到达取消点，那么pthread_cancel()无效

  被pthread_cancel()杀死的线程返回-1，使用pthread_join回收

* pthread_detach 函数

  线程分离

  ```c
  int pthread_detach(pthread_t thread);//成功0，失败错误号
  ```

  线程分离之后资源由操作系统自动回收

  ```c
  //线程失败打印错误,perror没用
  strerror(ret);
  检查出错返回
      fprintf(stderr,"xxx error %s\n",stderror(ret));
  ```

  线程控制原语：thread_create()  thread_self()   pthread_exit()   pthread_join()  pthread_cacel() pthread_detach()

  进程控制原语：fork()                    gepid()             exit() //return    wait()/waitpid() kill()

* 线程属性初始化

```c
int pthread_attr_init(pthread_attr_t * attr);//成功0，失败：错误号
int pthread_attr_destory(pthread_attr_t * attr);//成功0，失败：错误号
```

线程分离状态的函数

```c
int pthread_attr_setdetachstate(pthread_attr_t*attr,int detachstate);
int pthread_attr_getdetachstate(pthread_attr_t*attr,int* detachstate);
attr:已初始化的线程属性
detachstate： PTHREAD_CREATE_DETACHED（分离线程）
              PTHREAD_CREATE_JOINABLE(非分离线程)
    
```

* 线程使用注意事项

  * 主线程退出其他线程不退出，主线程应调用pthread_exit

  * 避免僵尸进程

    pthread_join

    pthread_detach

    pthread_create 指定分离属性

    被join线程可能在join函数返回前就释放完自己的所有内存资源，所以不应当返回被回收栈中的值

  * malloc和mmap申请的内存可以被其他线程释放

  * 应避免在对多线程模型中调用fork，除非马上exec，子进程只有调用fork的线程存在，其他线程在子进程中均pthread_exit

  * 信号的复杂语义很难与多线程并存，应避免使用信号机制

### 同步

线程同步：协同步调，按照预定的先后次序运行

线程同步：指一个线程发出某一个功能调用时，在没有得到结果之前，该调用不返回，同时其他线程为保证数据一致性，不能调用该功能。

锁：建议锁，对公共数据的访问，所有线程应该在访问公共数据前先拿锁再访问，但锁不具有强制性（互斥量）

```c
pthread_mutex_init()
pthread_mutex_mutex_destory()
pthread_mutex_lock()
pthread_mutex_trylock()
pthread_mutex_unlock()
返回值：成功0，失败返回错误号
pthread_mutex_t类型，本质是一个结构体
pthread_mutex_t mutex;变量值只有0，1两种
```

```c
int pthread_mutex_init(pthread_mutex_t *restrict mutex,const pthread_mutexattr_t *restrict attr);//restrict本指针指向的内存写操作只能由mutex完成
int pthread_mutex_destory(pthread_mutex_t * mutex);
int pthread_mutex_lock(pthread_mutex_t * mutex);
int pthread_mutex_trylock(pthread_mutex_t * mutex);
int pthread_mutex_unlock(pthread_mutex_t * mutex);
```

注意事项

尽量保证锁的粒度越小越好。

互斥锁，初值为1

加锁 --操作，阻塞线程

解锁++操作，唤醒阻塞在锁上的线程

try锁，尝试加锁，成功--，失败返回，同时设置错误号EBUSY

* 死锁:使用锁不恰当导致的现象：

  1.对一个锁反复lock

  2.两个线程各持有一把锁，请求对方持有的锁

* 读写锁

  * 锁只有一把，以读方式加锁，读锁，以写方式加锁，写锁

  * 读共享，写独占
  * 写锁优先级高

  读写锁是写模式加锁时，解锁前，所有对该锁的加锁线程都会被阻塞

  读写锁是读模式加锁时，如果线程以读模式对其加锁会成功，如果以写模式加锁会阻塞

  读写锁是读模式加锁时，同时有以读、写模式加锁的线程请求，会先满足写请求，致使所有线程阻塞

  ```c
  pthread_rwlock_init
  pthread_rwlock_destory
  pthread_rwlock_rdlock
  pthread_rwlock_wrlock
  pthread_rwlock_tryrdlock
  pthread_rwlock_trywrlock
  pthread_rwlock_unlock
  ```

  ```c
  pthread_rwlock_t 类型，用于定义一个读写锁变量
  ```

  相较于互斥量而言，当读线程多时，提高访问效率

* 条件变量

  条件变量本身不是锁，但它也可以造成线程阻塞，通常与互斥锁配合使用，给多线程提供一个会和的场所

  ```c
  pthread_cond_init函数
  pthread_cond_destory
  pthread_cond_wait
  pthread_cond_timewait
  pthread_cond_signal
  pthread_cond_broadcast
      
  pthread_cont_t类型，用于定义条件变量
  pthread_cont_t cond = PTHREAD_COND_INITIALIZER;//静态初始化
  ```

  * pthread_cond_wait函数

    ```c
    int pthread_cond_wait(pthread_cond_t *restrict cond,pthread_mutex_t*restrict mutex);
    ```

    函数作用：

    * 阻塞等待条件变量cond满足
    * 释放已掌握的互斥锁，解除互斥量（1，2两步为一个原子操作）`pthread_mutex_unlock(&mutex)`
    * 当被唤醒，pthread_cond_wait返回时，解除阻塞并重新申请获得互斥锁`pthread_mutex_lock(&mutex)`

* 生产者消费者模型

  ```c
  while(cond不满足){
     pthread_cond_wait(&cond,&mutex);
  }
  ```

* 信号量

  相当于初始化值为N的互斥量

  可应用于进程、线程之间同步

  ```c
  #include <semaphore.h>
  sem_init
  sem_destory
  sem_wait//加锁
  sem_trywait
  sem_timewait
  sem_post//解锁
  
  sem_t 本质上是结构体
  sem_t sem;//规定信号量sem不能小于0
  int sem_init(sem_t*sem,int pshared,unsigned int value);
  //pshared 0 线程间同步
            1 进程间同步
  //value N值（指定同时访问的线程数）
  ```

  

  

  

* "cd" does not work in shell script

```bash
tr -d "\r" < oldname.sh > newname.sh
```

