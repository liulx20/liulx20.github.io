---
title: linux内核
date: 2021-07-04 15:48:43
tags:
---

### 系统调用

系统调用通过返回一个long类型来表示成功与否，（通常0成功、负值失败

系统调用出错时，将错误码写入全局`errno`中，通过调用`perror()`可翻译成字符串

```c
SYSCALL_DEFINE0(getpid)
{ 
         return task_tgid_vnr(current);
}
```

`SYSCALL_DEFINE0`是一个宏，定义一个无参数(0个)的系统调用

`asmlinkage long sys_getpid(void)`

`asmlinkage`限定词。是一个编译指令，通知编译器仅从栈中提取该函数的参数，所有的系统调用需要这一限定词

函数返回值为long,系统调用在内核空间、用户空间的返回值分别为long,int

系统调用在内核中定义都加`sys_`前缀

* 系统调用号

  每个系统调用赋予了一个系统调用号，通过系统调用号关联系统调用

  当用户进程执行一个系统调用时，这个系统调用号就用来指明到底是要执行哪个系统调用。

  系统调用号一经分配不能变更，linux中有一个未实现的sys_ni_syscall() 只返回-ENOSYS，这个错误号是为无效系统调用设置的

* 用户空间程序无法执行内核代码，应该通过一定方式通知系统，告诉内核自己需要执行一个系统调用

  通知内核的机制是通过软中断实现的：通过引发一个异常来促使系统切换到内核态去执行异常处理程序

  此时的异常处理程序就是系统调用处理程序，在x86系统上预定义的软中断是中断号128，通过`int$0x80`触发中断

* 指定恰当系统调用

  系统调用号通过`eax`寄存器传递给内核

  sys_call()函数通过给定的NR_syscalls作比较来检查其有效性，如果大于等于NR_syscalls,则返回-ENOSYS,否则执行相应系统调用

  `call *sys_call_table(,%rax,8)`

  系统调用表表项是以64位（8字节）类型存放的

* 参数传递

  通过`ebx ecx edx esi edi`按照顺序存放前五个参数

  需要六个及六个以上参数的情况，需要一个单独的寄存器存放指向所有这些参数在用户空间地址的指针

* 参数验证

  系统调用需要检查所有参数是否合法有效

  在接受一个用户空间的指针之前，内核需要保证：

  * 指针指向的内存区域属于用户空间，进程不能哄骗内核去读内核空间的数据
  * 指针指向的内存区域在进程的地址空间，进程绝不能哄骗内核去读其他进程的数据
  * 如果是读，该内存应被标记位可读，如果是写，该内存应被标记为可写，如果是可执行，该内存被标记为可执行

  为了向用户空间写入数据，内核提供了`copy_to_user()`,他需要三个参数，第一个是进程空间的目的内存地址，一个是内核空间的源地址，最后一个是数据长度

  为了向内核空间写入数据，`copy_from_user()`

  如果执行失败，这两个函数返回的都是没能完成拷贝的数据字节数，如果成功返回0，当出现错误时，返回标准-EFAULT

  `copy_to_user`,`copy_from_user`都可能引起阻塞，当包含用户数据的页被换出时，这种情况就会发生，此时进程就会休眠，直到却也处理程序将该页重新换入物理内存

  最后一项检查针对是否有合法权限

  * 老版Linux内核需要超级用户权限的系统调用才可以调用`suser()`函数完成检查
  * 新的系统允许检查针对特定资源的特殊权限，调用者可以使用`capable()`来检查是否有劝能对指定的资源进行操作

* 系统调用上下文

  内核在执行系统调用时处于进程上下文

  current指针指向当前任务，即引发系统调用的进程

  在进程上下文中，内核可以休眠（比如在系统调用阻塞或者显示调用schedule()的时候）并且可以抢占

  首先，能够休眠说明系统调用可以使用内核提供的绝大部分功能

  在进程上下文中能够被抢占表明，像用户空间中的进程一样，当前的进程可以被其他进程抢占

  因为新的进程可以使用相同的系统调用，所以需要保证系统调用是可重入的

  当系统调用返回后，控制权仍在system_call()中，它最终会负责切换到用户空间

* 绑定一个系统调用

  首先，在系统调用表中最后加入一个表项，从0开始计算，系统调用在该表中的位置就是它的系统调用号

  对于所支持的各种体系结构，系统调用号都必须定义于`<asm/unistd.h>`

  系统调用必须被编译进内核映像（不能编译成模块），这只要把它放进kernel/下的一个相关文件中就可以了

* 从用户空间访问系统调用

  open()系统调用的定义：

  `long open(const char *filename,int flags,int mode)`

  不靠库支持，直接调用此系统调用的宏形式

  ```c
  #define NR_open 5
  _syscall3(long,open,const char *,filename,int,flags,int,mode)
  ```

  

  

### 内核数据结构

#### 链表

`<linux/list.h>`

```c
struct list_head{
    struct list_head *prev;
    struct list_head *next;
}
```

* 令人迷惑的宏

```C
#define LIST_HEAD_INIT(name) { &(name), &(name) }

#define LIST_HEAD(name) \
	struct list_head name = LIST_HEAD_INIT(name)

//展开一下就能看懂了==
//struct list_head list = {&list,&list}
```

遍历list

```C
#define list_for_each(pos, head) \
	for (pos = (head)->next; pos != (head); pos = pos->next)
```



```c
#define offsetof(TYPE,MEMBER) ((size_t)&((TYPE*)0)->MEMBER)
```

对地址0强转？



```C
#include <stdio.h>
struct Node{
	struct Node * next;//0
	char c;//8
	int a;//12，这里发生了内存对齐，64位机器
};

void test(struct Node * node){
	//这里只计算相对首地址偏移量，不会发生段错误
    printf("%u\n%u\n%u\n%u\n",node,&node->next,&node->c,&node->a);
	//printf("%d",node->a);只有去访问一个成员才会出现段错误
	printf("%u",sizeof(*node));
}
int main(){
	test(NULL);
	return 0;
}

```

* 64位系统`long`竟然是和`long long`数据范围一致，8位

```c
#define container_of(ptr,type,member) ({\
    const typeof(((type*)0)->member)*__mptr = (ptr);\
    (type*)((char*)__mptr -offsetof(type,member));})
```

 其中`typeof`是GNU中获取变量类型的关键字

为啥要有第一句？

因为宏没有参数检查的功能，增加这个`const typeof( ((type *)0)->member ) *__mptr = (ptr)`赋值语句之后，如果类型不匹配，会有警告

`ptr`，是指向`member`的指针，`type`，是容器结构体的类型，`member`就是结构体中的成员

```c
#define list_for_each_entry(pos, head, member)				\
	for (pos = list_first_entry(head, typeof(*pos), member);	\
	     !list_entry_is_head(pos, head, member);			\
	     pos = list_next_entry(pos, member))
```

安全遍历list,用n缓存下一个节点，可以在遍历时删除

```c
#define list_for_each_entry_safe(pos, n, head, member)			\
	for (pos = list_first_entry(head, typeof(*pos), member),	\
		n = list_next_entry(pos, member);			\
	     !list_entry_is_head(pos, head, member); 			\
	     pos = n, n = list_next_entry(n, member))
```

#### 队列

`<linux/kfifo>`

```c
struct __kfifo {
	unsigned int	in;//入口偏移
	unsigned int	out;//出口偏移
	unsigned int	mask;
	unsigned int	esize;
	void		*data;
};

```

`__attribute__((aligned(n)))`：此属性指定了指定类型的变量的最小对齐(以字节为单位),如果结构中有成员的长度大于n，则按照最大成员的长度来对齐.

注意：对齐属性的有效性会受到链接器(linker)固有限制的限制，即如果你的链接器仅仅支持8字节对齐，即使你指定16字节对齐，那么它也仅仅提供8字节对齐。

`__attribute__((packed))`此属性取消在编译过程中的优化对齐

#### 映射

Linux内核提供唯一标志数（UID)到一个指针的映射

`idr`数据结构用于映射用户空间的UID,比如将`inodify watch`的描述符或者POSIX的定时器ID映射到内核中相关联的数据结构上

* 初始化一个idr

静态或动态分配一个idr数据结构

然后调用`idr_init()`

`void idr_init(struct idr *idp)`

比如：

```c
struct idr id_huh;/*静态定义idr结构*/
idr_init(&id_huh);
```

* 分配一个新的UID

一旦建立了idr，就可以分配新的UID

1. 告诉idr你需要分配新的UID，允许其在必要时调整后备树的大小

`int idr_pre_get(struct idr *idp,gfp_t gfp_mask);`

该函数在需要时进行`UID`分配工作，调整由`idp`指向的`idr`大小，如果真的需要调整大小，则内存分配例程使用`gfp`标志：`gfp_mask`

==该函数成功时返回1，失败时返回0==

2. 请求新的UID

实际执行获取新的UID，并将其加到idr中

`int idr_get_new(struct idr *idp,void *ptr,int *id);`

该方法使用`idp`所指向的idr去分配一个新的UID,并且将其关联到指针ptr上，成功时该方法返回0，并将新的UID存于id。

错误时，返回非0错误码，错误码是`-EAGAIN`说明需要再次调用`idr_pre_get()`,如果idr已满，错误码为`-ENOSPC`

```C
int id;
do{
if(!idr_pre_get(&id_huh,GFP_KERNEL)){
 return -ENOSPC;
}
ret = idr_get_ner(&idr_huh,ptr,&id);
}while(ret == -EAGAIN);
```



* 查找UID

  `void *idr_find(struct idr*idp,int id);`

  如果调用成功，则返回id关联的指针，如果错误，则返回空指针

  ```c
  struct my_struct *ptr = idr_find(&id_huh,id);
  if(!ptr){
   return -EINVAL;/*错误*/
  }
  ```

* 删除UID

  `void idr_remove(struct idr*idp,int id)`

  删除id及id关联的指针，不提供错误信息

* 撤销idr

  `void idr_destory(struct idr *idp)`

  释放idr中未使用的内存，不释放已经分配给UID使用的任何内存

`void idr_remove_all(struct idr*idp)`

强制删除所有UID



#### rb tree

```c
struct rb_node {
	unsigned long  __rb_parent_color;//parent and current color
	struct rb_node *rb_right;
	struct rb_node *rb_left;
} __attribute__((aligned(sizeof(long))));

struct rb_root {
	struct rb_node *rb_node;
};

#define rb_parent(r)   ((struct rb_node *)((r)->__rb_parent_color & ~3))  //获得父结点的地址  
#define rb_color(r)   ((r)->rb_parent_color & 1) //获得颜色属性

```

奇奇怪怪的结构体初始化

```c
#define RB_ROOT	(struct rb_root) { NULL, }
```

##### 强制内联 `__always_inline`

```c
static __always_inline struct rb_node *
rb_find_add(struct rb_node *node, struct rb_root *tree,
	    int (*cmp)(struct rb_node *, const struct rb_node *));
```

带缓存的根节点

```C

struct rb_root_cached {
	struct rb_root rb_root;
	struct rb_node *rb_leftmost;
};

```

O(1)获取最小节点

```c
#define rb_first_cached(root) (root)->rb_leftmost
```

```
# define likely(x)  __builtin_expect(!!(x), 1)
# define unlikely(x)    __builtin_expect(!!(x), 0)
```

述源码中采用了内建函数__builtin_expect来进行定义，即 built in function。
　　`__builtin_expect`的函数原型为`long __builtin_expect (long exp, long c)`，返回值为完整表达式`exp`的值，它的作用是期望表达式`exp`的值等于`c`（如果`exp == c`条件成立的机会占绝大多数，那么性能将会得到提升，否则性能反而会下降）。注意， `__builtin_expect (exp, c)`的返回值仍是`exp`值本身，并不会改变`exp`的值。
　　`__builtin_expect`函数用来引导`gcc`进行条件分支预测。在一条指令执行时，由于流水线的作用，CPU可以同时完成下一条指令的取指，这样可以提高CPU的利用率。在执行条件分支指令时，CPU也会预取下一条执行，但是如果条件分支的结果为跳转到了其他指令，那CPU预取的下一条指令就没用了，这样就降低了流水线的效率。
　　另外，跳转指令相对于顺序执行的指令会多消耗CPU时间，如果可以尽可能不执行跳转，也可以提高CPU性能。
　　简单从表面上看if(likely(value)) == if(value)，if(unlikely(value)) == if(value)。
也就是likely和unlikely是一样的，但是实际上执行是不同的，加likely的意思是value的值为真的可能性更大一些，那么执行if的机会大，而unlikely表示value的值为假的可能性大一些，执行else机会大一些。
　　加上这种修饰，编译成二进制代码时likely使得if后面的执行语句紧跟着前面的程序，unlikely使得else后面的语句紧跟着前面的程序，这样就会被cache预读取，增加程序的执行速度。



#### radix_tree

linux的基数树结构是将指针与long类型的整数键值相映射的机制，可以提到查找的效率，是典型的以空间换取时间的做法.

```c
struct  radix_tree_root {
    unsigned int height;
    gfp_t gfp_mask;
    struct radix_tree_node *rnode;  /*间接指针，指向节点而非数据条目，通过设置root->rnode的低位表示是否是间接指针*/
};

struct radix_tree_node {
    unsigned int  height;  /*从叶子节点向上计算的树高度*/
    unsigned int count;    /*非叶子节点包含一个count域，表示出现在该节点的孩子节点的数量*/
    struct rcu_head rcu_head;
    void*  slot[RADIX_TREE_MAP_SIZE];  //64个指针，指示该几点的子节点最多有64个，该值是可以进行设置的，参考下面的全局变量的设置*/
    unsigned long tags[RADIX_TREE_MAX_TAGS][RADIX_TREE_TAG_LONGS];
};

```

以index=0x5BFB68为例，化为二进制，每6位为一组：10110(22,第一层编号),111111(63,第2层编号),101101(45,第三层编号),101000(40,第四层编号)

dix_tree_node.tags:  标识该节点的每个子节点中的标志位，是通过位图的方式进行表示的。该域是一个2X2的数组，其中每个成员都是32位。在该节点结构中每个slot都用2位标识，用于记录该节点下面的子节点的响应标识位有没有被置位。行数对应于有多少个标识，比如，如果有两个标识，PAGE_DIRTY和PAGE_WRITEBACK，那么就需要使用两行；如果有三个标识，就使用三行。列数对应于有多少个子节点，例如，如果有64个子节点，那么每一列代表其中的一个子节点。因此，该2x2数组中的每个值代表了每个slot中的每个标识是否被设置（当然需要将long类型的整数对应成二进制位才行，那么64个子节点恰好是需要64位，恰好是两个long  int 类型，每位代表一个子节点；每行代表一个标识）。该标识对于基数树的查找非常有帮助。如果tag[0]=0（PAGE_DIRTY为全为0），那么标识该节点对应的子节点中没有相应的节点有存在脏页，则在寻找脏页的过程中可以绕过该节点所对应的所有子节点，而不用遍历整棵树，提高了查找的效率；tag[1]=0（PAGE_WRITEBACK标志全为0)。

### 中断和中断处理

中断使得硬件得以发出通知给处理器。中断本质上是一种特殊的电信号，由硬件设备发向处理器，处理器接收到中断后，会马上向操作系统反映此信号到来，然后就由操作系统负责处理这些新到来的数据。

中断本质上是一种电信号，由硬件设备生成，并直接送入中断控制器的输入引脚中。

当接收到一个中断后，中断控制器会给处理器发送一个电信号。

不同设备对应的中断不同，而每个中断都通过一个唯一的数字标识。

这些中断值通常被称为中断请求（IRQ）线。每个IRQ线都会被关联一个数值量。

* 异常：

异常与中断不同，它在产生时必须考虑与处理器时钟同步。

异常常被称为同步中断

中断与异常工作方式类似，差异在于中断是由硬件而不是由软件引起。

#### 中断处理程序（interrupt handler)

在响应一个特定的中断时，内核会执行一个函数，该函数叫做中断处理函数。

一个设备的中断处理程序是它设备驱动程序的一部分。设备驱动程序是用于对设备进行管理的内核代码。

中断处理程序是被内核调用来响应中断的，他们运行在我们称之为中断上下文的特殊上下文中。该上下文中的执行代码不可阻塞。

#### 上半部下半部

要求：

中断处理程序运行快，完成工作量多

处理：

把中断处理程序分为两个部分：

* 上半部，接受一个中断，马上执行，只做有严格时限的工作。
* 能够被允许稍后完成的工作推迟到下半部。

#### 注册中断处理程序

`<linux/interrupt.h>`

`int request_irq(unsigned int irq,irq_handler_t handler,unsigned long flags,const char *name,void *dev);`

第一个参数表示要分配的中断号，对某些设备，这个值是预先确定的，对大多数设备，可以通过探测获取或者编程动态确定。

第二个参数handler是一个指针，指向中断处理函数。

`typedef irqreturn_t (*irq_handler_t)(int, void *)`

接收两个参数，返回一个`irqreturn_t`

第三个参数flags可以为0，也可以是下列一个或多个标志的位掩码。

`IRQF_DISABLED`: 内核在处理中断处理程序时，禁止所有其他的中断。

`IRQF_SAMPLE_RANDOM`:表明这个设备产生的中断对内核熵池有贡献。内核熵池负责从各种随机事件中导出真正的随机数。

`IRQF_TIMER`:系统定时器的中断处理准备的

`IRQF_SHARED`:多个中断处理程序之间共享中断线。

第四个参数name是中断相关设备的ASCII文本表示。键盘中断对应`keyboard`,这些名字被`/proc/irq`和`/proc/interrupts`使用

第五个参数dev用于共享中断线，当一个中断处理程序需要释放时，dev将提供唯一的标志信息（cookie)，以便从共享中断线的诸多处理程序中删除指定的哪一个。

`request_irq()`成功执行返回0，返回非零表示有错误发生。

`request_irq()`函数可能睡眠，不能在中断上下文或其他不允许阻塞代码中调用该函数，在注册过程中，内核需要在/proc/irq文件中创建一个与中断对应的项。

函数`proc_mkdir()`用来创建这个`procfs`项，通过调用`proc_create()`对这个新的项进行设置，而`proc_create()`会调用`kmalloc()`,`kmalloc()`是可以睡眠的。

```c
if(request_irq(irqn,my_interrupt,IRQF_SHARED,"my_device",my_dev)){
printk(KERN_ERR "my_device:cannot register IRQ %d\n",irqn);
return -EIO;
}
```



#### 释放中断处理程序

`void free_irq(unsigned int irq,void * dev)`

卸载驱动程序时，需要注销相应的中断处理程序，并释放总线。

总线非共享直接删除，共享仅删除dev对应的处理程序。

#### 编写中断处理程序

`static irqreturn_t intr_handler(int irq,void *dev)`

第一个参数irq是这个处理程序要响应的中断的中断号。

第二个参数dev是一个通用指针，它与在中断处理程序注册时传递给`request_irq()`的参数dev必须一致。

中断处理程序返回值是一个特殊类型`irqreturn_t`

中断处理程序可能返回两个特殊的值：`IRQ_NONE` `IRQ_HANDLED`

当中断处理程序检测到一个中断，但该中断对应的设备并不是在注册处理函数期间产生的指定的产生源时，返回`IRQ_NONE`

当中断处理程序被正确调用，且确是它所对应的设备产生了中断时返回`IRQ_HANDLED`

Linux中的中断处理程序是无需重入的，当一个给定的中断处理程序正在执行，相应的中断线在所有处理器上都会被屏蔽掉，以防止在同一中断线上接受另一个新的中断。但不影响其他中断线。

#### 共享的中断处理程序

* request_irq()的flags必须设为IRQF_SHARED标志
* 对于每个注册的中断处理程序，dev参数必须唯一
* 中断处理程序必须能够区分它的设备是否真的产生了中断

指定IRQF_SHARED标志调用request_irq()时，只有在

* 当前中断线未被注册
* 当前中断线所有已注册处理程序指定了IRQF_SHARED时才能成功

内核在接收到一个中断后，依次调用该中断线上注册的每一个中断处理程序。因此处理程序必须知道他是否对这个中断负责。

#### 中断上下文

进程上下文是一种内核所处的操作模式，此时内核代表进程执行（执行系统调用、运行内核进程）。在进程上下文中，可以通过current宏关联当前线程。

中断上下文和进程无关，没有后备线程，不能睡眠，否则不能对它进行重新调度。

中断上下文有较为严格时间限制，因为打断了其他代码。中断上下文中的代码应该迅速简洁，尽量不使用循环。

中断处理程序栈是一个配置选项，（曾经共享中断进程的内核栈。

#### 中断处理机制的实现

设备产生中断，通过总线将电信号发送个中断控制器，如果中断线是激活的（允许被屏蔽），那么中断控制器将把中断发送给处理器。除非在处理器上禁止该中断，处理器会立刻停止正在做的事情，关闭中断系统，跳到内存中预定义位置开始执行那里的代码，这个位置是内核设置的，是中断处理的入口点。

对于每条中断线，处理器都会跳到对应唯一位置，这样内核就知道所接收中断的IRQ号，初始入口点只是在栈上保存这个号，并存放当前寄存器的值（这些值属于当前被中断任务）。

然后内核调用do_IRQ()

`unsigned int do_IRQ(struct pt_regs regs)`

计算出中断号，do_IRQ()对所接受的中断进行应答，禁止这条线上中断传递

do_IRQ()需要确保这条中断线上有一个有效的处理程序，并且这个程序已经启动，但没执行

调用handle_IRQ_event()来运行这条中断线所安装的中断处理程序。
