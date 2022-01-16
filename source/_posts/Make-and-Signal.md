---
title: Make and Signal
date: 2021-02-02 20:31:28
tags: os
---

## Make

hello world in make

```makefile
hello:
	echo "hello world"
```

Save this in a file named ‘makefile’. Then navigate to the directory and run the command:

```bash
$ make hello
```

<!-- More -->

* Makefile syntax

```makefile
target: prerequisites
<TAB> recipe
```

* Make command in shell:

```bash
$ make target
```

* Other targets can be used as prerequisites of a target

```makefile
target: other_target target.c
 Recipe_to_create_target
other_target: other_target.c
 Recipe_to_create_other_target
```

example:

```makefile
code_file1.o: code_file1.c
	gcc -c code_file1.c -o code_file1.o
code_file2.o: code_file2.c
	gcc -c code_file2.c -o code_file2.o
my_app: code_file1.o code_file2.o
	gcc -o my_app code_file1.o code_file2.o
clean:
	rm *.o my_app
```

* When make is ran, it looks for the **target** file in the directory. If the target is not found, 

  recipe to generate target is ran with all the prerequisites.

* If **target** is found, it checks whether the dependencies have changed since last time. If 

  so, changed dependencies are run according to the configuration and the target is 

  generated.

* **target** can be different from output filename. In this case, make won't be able to find the 

file and the file will be regenerated regardless of no changes. (Don’t do this when

compiling)

* By default the first target of the makefile is considered as the default target. If you run 

  make with no arguments, the first target is run.

* By convention, the first target is set as **all**. It should have the recipe for the default 

  behaviour you expect from make.

* Using **.DEFAULT_GOAL** can override the default behaviour of make

```makefile
#same behaviour if we use .DEFAULT_GOAL=my_app
all:my_app 
code_file1.o: code_file1.c
	gcc -c code_file1.c -o code_file1.o
code_file2.o: code_file2.c
	gcc -c code_file2.c -o code_file2.o
my_app: code_file1.o code_file2.o
	gcc -o my_app code_file1.o code_file2.o
clean:
	rm *.o my_app
```



**Phony target** is a target which is not the name of a file. Say we have a target named ‘clean’. If we also have a file named clean, make will not run the recipe for this target.

We can indicate such targets with **.PHONY** and make will run it regardless of a file.

```makefile
.PHONY: clean
clean:
	rm *.o my_app
```

You can define variables in makefile:

```makefile
OBJECTS=code_file1.o code_file2.o
my_app: $(OBJECTS)
	gcc -o my_app $(OBJECTS)
```

You can use wildcards as well.

### implicit variables

There are a set of implicit variables defined in make:

```makefile
CFLAGS
CC
CXX
and etc..
```

These variables can be referred without declaring them and the default value will be passed. If needed they can be overridden by declaring them as a regular variable.

```makefile
code_file1.o: code_file1.c
	$(CC) $(CFLAGS) -c code_file1.c -o code_file1.o
```

[List of implicit variables](https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html)

### pass command line arguments

We can pass command line arguments when using make to alter the compilation.

```c
//main.c
#include <stdio.h>
int main()
{
	printf("MY_VAL = %d\n", MY_VAL);
}
```

```makefile
main:main.c
	gcc $(CFLAGS) main.c -o main
clean:
	rm main
```

```bash
$ make CFLAGS=-DMY_VAL=3
```

```bash
output:
MY_VAL = 3
```

如何在程序中确定make指令有没有指定MY_VAL

```c
#ifdef MY_VAL
...
#else
...
#endif
```



* It won’t compile without the argument.

## Signals

Signals are events created by UNIX and Linux systems and are a method for the OS to communicate with a process. They can be acted upon or ignored.

* A method of interprocess communication
* Are the result of some condition
* Allow the process receiving the signal to take an action through a signal handler

Provide a process a notification of an event.

* Event gains attention of the OS.

* OS stops the application process immediately, sending it a signal.

* Signal handler is executed.

* Application process resumes where it left of.

**Raise**

The generation of a signal upon a process.

**Catch**

The reception of a signal by that process.

**Handle**

How the program reacts to the signal.

#### Conditions for signals

* Error conditions such as：

  Memory segment violations

  Floating-point processor errors

  Illegal instructions

* Explicitly sent from one process to another as a method of Inter-process communication

  example:

* Process makes illegal memory reference

  Event gains attention of the OS.

  OS stops application process immediately, sending it a SIGSEGV signal.

  Signal handler for SIGSEGV signal executes to completion.

  Default signal handler for SIGSEGV signal prints “Segmentation Fault” and exits process.

  ```
  SIGINT Terminal interrupt
  SIGKILL Kill process
  SIGSEGV Invalid memory segment access
  ```

* Signals can be raised using a few different methods

  ```
  Keystrokes
  Commands
  System calls
  ```

* Keystrokes

​     **CTRL + C** -> SIGINT

​     Default handler exits process.

​     **CTRL + Z** -> SIGTSTP

​     Default handler suspends process.(进程暂停)

​     **CTRL + \\** -> SIGQUIT

​     Default handler exits process

* Sending signals via command

  ```
   kill -signal pid
  ```

  Send a signal of type signal to the process with id pid.

  The kill command can send all signals

  e.g.

  ```bash
  $ kill -2 1234
  $ kill -INT 1234
  ```

* System calls

  **kill()**

  Commands the OS to send a signal to the process, must have permission.

  Both processes must have the same user ID.(具有相同的用户id)

  Superuser can send signal to any process(超级用户可以向任何进程发送信号)

  ==Return value==:

  Success: 0

  Error: -1 (errno is set appropriately)

  EINVAL if invalid

  EPERM if no permission

  ESRCH if specified process does not exist

  **raise()**

  Commands the OS to send a signal to current process

  **alarm()**

  Schedule a SIGALRM at some time in future.

  Processing delays and scheduling uncertainties.

  Value of 0 cancels any outstanding alarm request.

  Each process can have only one outstanding alarm.

  Calling alarm before signal is received will cause alarm to be rescheduled.

  

  ### how to handle signal

  **signal()**

  

  ```c
  #include <signal.h>
  Void (*signal(int sig, void (*func)(int)))(int);
  ```

  signal() returns a function which is the previous value of the function set up to handle the signal.

  OR one of these two special values:

  SIG_IGN – Ignore the signal

  SIG_DFL – Restore default behavior

  ```c
  #include <signal.h>
  #include <stdio.h>
  #include <unistd.h>
  void ouch(int sig) 
  {
   printf(“OUCH – I got signal %d\n”, sig);
   (void) signal(SIGINT, SIG_DFL);
  }
  int main()
  {
   (void) signal(SIGINT, ouch);
   while(1)
   {
   printf(“Hello World!\n”);
   sleep(1);
   }
  }
  ```

  **Waiting for signal**

  **pause()**

  ```c
  #include <unistd.h>
  int pause(void);
  ```

  * Causes program to suspend execution until a signal occurs.

  * When it receives a signal, any established handler is run and execution 

    continues as normal.

**Re-entrant Functions**

* That can be interrupted in the middle of execution and then safely called again (“re-entered”) before its previous invocations complete execution.

* Never call a non-reentrant function inside a signal handler, if the function was being ran the behaviour will be changed.

* Example if a global was used as a temporary value, and gets overwritten in 

  the signal handler

**Race conditions**

* A flaw in a program whereby the correctness of the program is critically 

  dependent on the sequence or timing of other events

* Example: a signal handler and function modifying the same value

* Race conditions Example

  ```c
  //deposit is running and is interrupted by a signal after copying savings to temp.
  savings = 5000, value = 2000
  int savings; // 5000
  
  void deposit(int val) // 2000
  {
  int temp = savings;
  ---- Signal
  temp += val;
  savings = temp;
  }
  void salary(int sig)
  {
  savings += 5000; // 10000
  }
  ```

**POSIX Signal Handling**

**C90 standard**

signal() and raise() functions

Works across all systems (UNIX, Linux, Windows)

But differently across some systems

Blocked signals during handler execution

Reinstall handler after every signal invocation

Does not provide mechanism to block signals

**POSIX standard**

sigaction() and sigprocmask() functions:

Works the same across all POSIX-compliant UNIX systems (Linux, Solaris etc) but…

Do not work on non-UNIX systems (e.g. Windows)

Provides mechanism to block signals in general

sigprocmask() is not required to use sigaction()

**sigaction()**

```c
#include <signal.h>

int sigaction(int sig, const struct sigaction *act, struct sigaction *oact);
```

struct sigaction has at least

```c
void (*) (int) sa_handler // function, SIG_DFL, SIG_IGN
sigset_t sa_mask // signals to block in sa_handler
int sa_flags // signal action modifiers
```



```c
#include <signal.h>
#include <unistd.h>
#include <stdio.h>
int stop = 0;
void handler(int sig) {
 stop = 1;
}
int main() {
 struct sigaction sa;
 sa.sa_flags = 0; // no flags
 sigemptyset(&sa.sa_mask); // clear the mask so no signals are blocked
 sa.sa_handler = handler; // set function pointer for handler
 sigaction(SIGINT, &sa, NULL); // set the handler
 while(!stop) {
 ;
 }
}
```

**setjmp & longjmp**

* setjmp and longjmp are two flow control subroutines.

* When setjmp is called, it saves the program state at that point and returns 0.

* When longjmp is called, it returns from the place where the jump is set with the given value.

* If you are jumping from a signal handler, you might need to used **sigsetjmp** and **siglongjmp** instead setjmp and longjmp due to signal mask issues. 

```c
#include <setjmp.h>
#include <stdlib.h>
#include <stdio.h>
int main()
{
 jmp_buf env;
 int i;
 i = setjmp(env);
 printf("i = %d\n", i);
 if (i != 0)
 {
 exit(0);
 }
 longjmp(env, 1);
 printf("I will never be printed!!\n");
}
```

`setjmp` 與 `longjmp` 函數可以讓程式往回跳到函數呼叫堆疊中的某個函數中，就像是一種跨函數的 `goto`。

首先使用 `setjmp` 在程式中標示一個目標位置（跳躍的目的地），然後在程式要進行跳躍的地方呼叫 `longjmp` 即可。

```c
#include <stdio.h>
#include <setjmp.h>

// 儲存程式跳躍時所需之資訊
jmp_buf jmpbuffer;

int fun_a(int v) {
  int r = v * 2 - 1;
  if (r < 0) {
    // 跳躍至 main 函數
    longjmp(jmpbuffer, 1);
  }
  return r;
}
int fun_b(int v) {
  int r = fun_a(v) + 6;
  if (r > 10) {
    // 跳躍至 main 函數
    longjmp(jmpbuffer, 2);
  }
  return r;
}
int fun_c(int v) {
  int r = fun_b(v) * 5 - 21;
  return r;
}
int main() {
  // 設定跳躍目標位置
  int jmpVal = setjmp(jmpbuffer);
  if ( jmpVal == 1 ) {
    printf("fun_a errorn");
  } else if ( jmpVal == 2 ) {
    printf("fun_b errorn");
  } else {  // jmpVal == 0
    int x = -5;
    int result = fun_c(x);
    printf("Result = %dn", result);
  }
  return 0;
}

```

在 `setjmp` 設定跳躍目標位置時，會需要指定一個特殊的 `jmp_buf` 變數，用來儲存程式跳躍時所需之資訊，而在直接呼叫 `setjmp` 函數時其傳回值為 `0`，若是透過 `longjmp` 跳回這裡時，其傳回值就會是呼叫 `longjmp` 時所指定的值.



* What if you want to handle a signal multiple times in your program?

* Do not use setjmp() and longjmp().

* setjmp() does not save the signal mask.

* The first SIGSEGV is added to the process' signal mask to prevent subsequent signals interrupting the handler

* When setjmp() pseudo returns, that mask is still there.

*  use sigsetjmp() and siglongjmp()

  ````c
  int sigsetjmp(sigjmp_buf env, int savemask)
  void siglongjmp(sigjmp_buf env, int val)
  ````

  If savemask is set to 1, it saves the signal mask and siglongjmp restores the saved signal mask.

* What is saved in sigjmp_buf?

  **Program Counter**

  Location in the code

  **Stack pointer**

  Locations of local variables

  Return address of called functions

  **Signal Mask** 

   If specified

  **Rest of environment (CPU state)**

  Calculations can continue from where they stopped

* What is NOT saved in sigjmp_buf?

  Global variables

  Variables allocated dynamically

  Values of local variables

  Any other global resources

* What does it mean by scanning the memory?

  Simply, you can try to access memory locations in a loop, using pointer dereferencing

  ```c
  char *p = (char *)0xff13abc1;
  char a = *p;
  ```

* How do we know where the process’ address space starts and ends?

  0x0 to 0xffffffff (2^32-1)

  This is organized into pages of 4096 bytes (or other defined size in the assignment)

* How do we check a page’s permissions?

  Try reading/writing to it and see what’s the response from OS.

  If two consecutive pages have the same permissions, they are part of the same “mem_region"

  When you try to write to memory, write the same content to avoid modifying it

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  