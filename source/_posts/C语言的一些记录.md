---
title: C语言的一些记录
date: 2020-08-21 23:00:15
tags: C语言
---

* 指针类型大小都为8
* 文件指针不关闭会导致内存泄漏
<!--More-->
```cpp
//test.cpp
#include<stdio.h>
int main()
{
  FILE *f = fopen("a.txt","r");
  return 0;
}
```

```
valgrind --leak-check=full --show-reachable=yes --trace-children=yes   ./test
```
```cpp
==333== Memcheck, a memory error detector
==333== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==333== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==333== Command: ./test
==333==
==333== error calling PR_SET_PTRACER, vgdb might block
==333==
==333== HEAP SUMMARY:
==333==     in use at exit: 472 bytes in 1 blocks
==333==   total heap usage: 1 allocs, 0 frees, 472 bytes allocated
==333==
==333== 472 bytes in 1 blocks are still reachable in loss record 1 of 1
==333==    at 0x483B7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==333==    by 0x48E0AAD: __fopen_internal (iofopen.c:65)
==333==    by 0x48E0AAD: fopen@@GLIBC_2.2.5 (iofopen.c:86)
==333==
==333== LEAK SUMMARY:
==333==    definitely lost: 0 bytes in 0 blocks
==333==    indirectly lost: 0 bytes in 0 blocks
==333==      possibly lost: 0 bytes in 0 blocks
==333==    still reachable: 472 bytes in 1 blocks
==333==         suppressed: 0 bytes in 0 blocks
==333==
==333== For lists of detected and suppressed errors, rerun with: -s
==333== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
### C语言判断文件是否存在
access函数判断文件夹或者文件是否存在
```C
int access(const char *filename, int mode);

filename：可以填写文件夹路径或者文件路径

mode：0 （F_OK） 只判断是否存在
      2 （R_OK） 判断写入权限
      4 （W_OK） 判断读取权限
      6 （X_OK） 判断执行权限
```
用于判断文件夹是否存在的时候，mode取0，判断文件是否存在的时候，mode可以取0、2、4、6。 若存在或者具有权限，返回值为0；
不存在或者无权限，返回值为-1。
fopen函数判断文件是否存在

函数原型：FILE *fopen (char *filename, char *type);

filename：文件路径

type：打开文件的方式（有r、w、r+、w+、a、rb、wb等等）

用于判断文件是否存在可以使用 r 或者 rb ，因为使用其它方式的话，可能会自动建立文件。 返回值为NULL（打不开）和正数（能打开）。

### unlink函数
```C
#include<unistd.h>
int unlink(const char *pathname);

if(unlink("test.txt") < 0)
{
        printf("unlink errpr!\n");
}
```


* 结构体定义在`xx.c`文件，其他文件通过`#include "xx.h"`使用该结构体会报错：不允许使用不完整类型
只能把结构体定义在.h文件里面

* 把数据内容type a存入char数组s
memcpy(s,&a,sizeof(type))

* 不能对宏定义的常量进行取地址操作

### 编译相关
* gcc 生成文件跟在-o后面就行
* 编译含math库函数时，要加-lm

### 多进程相关
* 创建n个进程
```C
int i;
for(i = 0; i < n; i++){
   pid = fork();
   if(pid == 0)break;
}
```
* 子进程会拷贝fork语句之前的内容
* 共享内存
```C
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>  // for using shared memory

int size_bytes = length * sizeof(int);
int shmid = shmget(IPC_PRIVATE, size_bytes, 0666 | IPC_CREAT);
int * arr = shmat(shmid, 0, 0);
```
* 信号
```C
#include <sys/wait.h>
#include <unistd.h>

//向进程pid发送信号
kill(pid,SIGCONT);

//接收信号并处理,handler 为处理函数，只带一个int参数，返回值为void
signal(SIGCONT,handler);
```

* 访问临界数据必须加互斥锁
* 指针 + 1产生的偏移量取决于指针类型
* sizeof(size_t) == 8