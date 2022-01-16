---
title: Effective C++
date: 2021-08-14 12:58:27
tags:
---

### 尽量以const,enum,inline 替换#define

```C++
#define AspectRatio 1.635
const double AspectRatio = 1.635;
```

class 专属常量，为保证常量只有一份实体，必须让它成为一个static变量

```c++
class A{
private:
     static const int Num = 5;
     int score[Num];
};
```

### 尽量使用const

```c++
char greet[] = "Hello";
char *p = greet;//non_const pointer non-const data
const char *p = greet;//const data, non-const pointer
char* const p = greet;//const pointer,non-const data
const char* const p = greet;//const pointer,const data
```

如果const出现在星号左边，被指物是常量，出现在星号右边，指针本身是常量。

STL迭代器：

```c++
std::vector<int> vec;
const std::vector<int>::iterator iter = vec.begin();//相当于T* const
*iter = 10;//没问题，改变iter所指物
++iter;//不行，iter是const
std::vector<int>::const_iterator cIter = vec.begin();//相当于const T*
*cIter = 10;//不行，*cIter是const
++cIter;//没问题
```

const 重载

```c++
#include<iostream>
class Textbook
{
public:
    Textbook(std::string s):text(s){}
    const char& operator[](std::size_t pos) const
    {
        std::cout << "const\n";
        return text[pos];
    }
    char& operator[](std::size_t pos)
    {
        std::cout <<"non const\n";
        return text[pos];
    }
private:
    std::string text;
};
int main()
{
    Textbook tb("hello");
    std::cout << tb[0] << '\n';
    const Textbook ctb("world");
    std::cout << ctb[0] << '\n';

}

```

只是改变参数const属性不可以重载

```c++
class Textbook
{
public:
    void test(int a){
        
    }
    void test(const int a){
       
    }
};
```

### 确定对象在被调用前已经被初始化

```c++
ABEntry::ABEntry(const std::string&name,const std::string&addr,const std::list<PhoneNumber>&phones):theName(name),theAddr(addr),thePhones(phones){}
```

初始化列表省了一次调用默认构造函数的代价

为免除跨编译单元之初始化次序问题，用local static对象替换non_local static 对象

### 构造、析构、赋值操作

在一个内含reference成员的class内支持赋值操作，必须自己定义copy assignment操作符。

面对内含const成员的class,编译器反应一样。

如果某个base class将assignment操作符声明为private,编译器拒绝为其derived class生成assignment操作符.

### 不想使用编译器自动生成的函数

```c++
class Test{
    public:
    ...
    private:
        Test(const Test &);//只有声明
        Test& operator=(const Test&);
}
```

将复制构造函数、copy assignment声明为private,外部不可调用，内部调用会有链接错误

还可以定义一个base类，其复制构造函数、copy assignment为private，子类就不能生成默认构造函数、copy assignment.

### 为多态基类声明virtual函数

一个base类指针指向一个derived对象，base类析构函数non-virtual,调用delete时，derived类成员可能未被delete

要实现virtual函数，对象必须携带一些信息。用于在运行时决定哪一个virtual函数被调用

通常是一个所谓的vptr指针指出。

vptr指向一个由函数指针构成的数组，称为vtbl.

* 只有class内含至少一个virtual函数才为析构函数声明为virtual

STL容器都带有non-virtual析构函数

纯虚函数：

```c++
class AWOV{
public:
 virtual ~AWOV() = 0;
};
```

析构函数的运作方式：

最深层派生（most derived)的那个class其析构函数最先被调用，然后是其每一个base class的析构函数被调用。

### 别让异常逃离析构函数

### 绝不在构造函数和析构函数中调用virtual函数

"在base class构造期间，virtual函数不是virtual函数"（会调用base class版本的virtual函数）

### 令operator=返回一个reference to *this

### 在operator=中处理自我赋值

```c++
Widget&Widget::operator=(const Widget&rhs){
    if(this == &rhs)return *this;//证同测试（identity test)
    delete pb;
    pb = new Bitmap(*rhs.pb);
    return *this;
}
```

```c++
Widget& Widget::operator=(const Widget&rhs){
    Bitmap* POrig = pb;
    pb = new Bitmap(*rhs.pb);
    delete pOrig;
    return *this;
}
```

```c++
Widget& Widget::operator=(const Widget& rhs){
    Widget temp(rhs);
    swap(temp);
    return *this;
}
```

(1)某class的copy assignment操作符可能被声明为’以by value方式接收实参‘

(2)以by value 方式传递东西会造成一份副本

```c++
Widget& Widget::operator=(Widget rhs){
    swap(temp);
    return *this;
}
```

将copy操作从函数本体移至函数参数构造阶段

### 复制对象时勿忘每一成分

令copy构造函数调用copy assignment操作无意义，构造函数用来初始化新对象，而assignment操作符只施于已初始化对象身上。

令copy assignment操作符调用copy构造函数不合理，因为这就像在构造一个已经存在的对象。

copy构造函数和copy assignment操作符有相似代码，消除重复代码的做法是，建立一个新的成员函数给二者调用。

### 以对象资源管理对象

* 获得对象后立刻放进管理对象

* 管理对象运用析构函数确保资源被释放

  share_ptr在其析构函数中调用delete 而不是delete[]

  不能在动态分配的array身上使用share_ptr

### 在资源管理类中小心copying行为

* 禁止复制
* 对底层资源祭出引用计数法

shared_ptr允许指定所谓的删除器，那是一个函数或函数对象，当引用次数为0时便调用

```c++
class Lock{
public:
    explicit Lock(Mutex* pm):mutexPtr(pm,unlock){
            lock(mutexPtr.get());
    }
private:
    std::shared_ptr<Mutex>mutexPtr;
    
};
```

* 复制底部资源

复制资源管理对象时，也应该复制其所包裹的底层资源

* 转移底部资源的所有权

某些场合下希望只有一个RAII指向一个（raw resource),即使RAII对象被复制依然如此，此时资源的所有权会从被复制物转移到目标物.

### 在资源管理类中提供对原始资源的访问

share_ptr 重载了*，->运算符，隐式转换至底层资源

### 成对使用new 和delete时要采取相同的形式

当使用new,有两件事情发生：第一内存被分配出来，第二，针对此内存会有一个或更多构造函数函数被调用，

当使用delete,有两件事发生：会有一个或多个析构函数被调用，然后内存才被释放

delete最大的问题在于，即将被删除的内存究竟存有多少个对象，这个问题决定了有多少个析构函数必须被调用

唯一让delete知道内存是否存在一个数组大小记录的办法就是在使用delete时加上中括号

==重写不能改变返回值类型，参数列表==

==引用也能实现多态==

成为虚函数的条件：
1.要能取地址
2.依赖对象调用

==内联函数不能成为虚函数，没法对一个内联函数取地址==

==构造函数 不可以 系统调用 不依赖对象调用==

static函数 不可以 无this指针 不依赖对象调用





### 引用

引用本质上是一个常量指针，`int * const p`

占用空间情况和指针一致

对引用的修改即是对源数据的修改

引用必须初始化，指针不可以

指针可以赋值为nullptr,没有空引用

没有`int & const a`,只有`const int & a`



强转运算重载：

```C++
class Complex{
public:
    //注意函数声明
    operator double(){
        return real;
    }
private:
    double real,img;
}
```



```c++
class A{
public:
    virtual void print(){
        cout << "A\n";
    }
    A& operator=(const A & a){
        cout << "assignment\n";
    }
    A(const A& a){
        cout << "copy\n";
    }
    A(const A&&a){
        cout << "move\n";
    }
    A(){
        cout << "default\n";
    }
};
class C:public A{
public:
    void print(){
        cout << "C\n";
    }
};
int main(){
    //default
    A a = A();
    //default,move
    //没有move会调用copy
    A c = C();
}
```

私有继承：

```C++
#include<iostream>
using namespace std;

class A{

};
class C:private A{

};



int main(){
    //都不行， 'A' is an inaccessible base of 'C'|
    A&& a = C();
    A * a = new C();
    A a = C();
}

```

const 重载

```c++
class A{
public:
    void print(){
        cout << "print\n";
    }
    void print()const{
        cout << "print const\n";
    }
};
int main(){
    A a;
    a.print(); //print,当没有non-const print()时，也输出print const
    const A b;
    b.print();//print const,当没有const print(),报错passing 'const A' as 'this' argument discards qualifiers
}

```

```C++
class A{
public:
    virtual void print(){
        cout << "print\n";
    }
};
class C:public A{
public:
    void print()const{
        cout << "print const\n";
    }
};



int main(){
    A&& a = C();
    a.print();//输出的是print,类C没有重载A的print()
}

```

子类以私有方式重写父类虚函数，通过父类引用、指针可以调用子类相应私有方法

```C++
class A{
public:
    virtual void print(){
        cout << "A\n";
    }
};
class C:public A{
private://此处print为私有
    void print(){
        cout << "C\n";
    }
};



int main(){
    A&& a = C();
    a.print();//输出C
    C c;
    c.print();//报错'virtual void C::print()' is private within this context
}


```

纯虚函数是可以有实现的

```C++
class A{
public:
    virtual void test() = 0;//纯虚函数
    A(int x){

    }
};

void A::test(){
    cerr << "test A\n";
}

class B:public A{
public:
    void test(){
        A::test();
    }
    B(int x):A(x){//必须写在初始化列表

    }
    int cal(){
        return 2;
    }
};
int main(){
    B b(2);
    b.test();
    //test(1);
}



```

构造函数中==必须写在member initialization list的==

* 初始化一个reference member
* 初始化一个const member
* 当调用一个base类的constructor且它有一组参数
* 当调用一个member类的constructor且它有一组参数

### 段错误的原因

* 访问不存在的内存地址 

  ```C++
  int main(){
  int *p = NULL;
  *p = 0;
  }
  ```

  

* 访问系统保护的内存地址 

  ```c++
  int main(){
  int *ptr = (int *)0; 
  *ptr = 100; 
  }
  ```

* 访问只读的内存地址 

  ```c++
  char *ptr = "test"; 
  strcpy(ptr, "TEST"); 
  ```

* 栈溢出 

  ```C++
  int main(){
  main();
  }
  ```

* double free

  ```c++
  int main(){
      int * p = (int *)malloc(sizeof(int));
      *p = 2;
      free(p);
      cout << (*p) << '\n';
      free(p);
  }
  
  ```

  

Why are only `static const` integral types & enums allowed In-class Initialization?

为什么只有static const integral类型以及enums被允许类内初始化呢？



这个答案就在Bjarne的那段话中。“C++需要每一个对象有特定的定义。如果C++允许存储在内存中的对象进行类内定义，那么这一规则将会被打破。”

注意只有static const integers 会被看作编译时的常量。编译器了解这样的integer变在任何情况下都不会改变，因此编译器才可以对其做出特有的优化与改进，编译器会简单的将其内联化这样的变量，因而不再使其保存在内存中。因为保存在内存中的需求被移除了，使得他们成了Bjane所说规则的例外。

值得注意的是，即使static const integral这样的变量被允许使用类内初始化，但是获取这样的变量的地址是不被允许的。一个变量只有拥有类外定义的情况下，才能被获得地址。



```c++
class A{
public:
    static int x ;
};
//要有這句才能過編譯
int A::x = 0;
int main(){
    cout << &A::x << '\n';
}

```



* 静态成员函数

```c++
class A{
public:
    static int print() const{
        return 1;
    }
};
//static member function 'static int A::print()' cannot have cv-qualifier
```

1.static成员函数不包含`this`指针
2.static成员函数不能为`virtual`
3.不能存在static和non-static成员函数有相同的名字和参数
4.static 成员函数不能被声明成const、volatile或者const volatile。(可以为inline)



析构函数是私有、删除的情况下，不能在栈上定义对象。

```c++
class A{
public:
    ~A() =delete;
};
signed main(){
     //A a;
    //use of deleted function 'A::~A()'
    //因为a离开作用域后会自动调用析构函数
    A *a = new A();//允许，不能delete
}


```





```c++
void test(int && a){
    cerr << "right\n";
}
void test(int &a){
    cerr << "left\n";
}
void test(const int & a){
    cerr << "const left\n";
}
void test(const int && a){
    cerr << "const right\n";
}
signed main(){
   int&& x = 2;
   test(x);
   const int && y = 3;
   test(y);
   test(4);
}
/*输出：
left
const left
right
*/
```

```c++
int a;
int& setVal(){
    return a;
}
setVal() = 3;//允许，返回的是左值

void test(int & a){}
test(2);//不合法，要求传一个左值
```



不能对一个类的构造/析构函数取地址，因为构造函数析构函数没有返回值，不能产生一个有效的函数指针。

成员函数指针占16个字节。为在简单函数指针的后面还需要保存怎样调整 “this" 指针（总是隐式地传递给非静态成员函数）的信息。

```c++
#include <iostream>

struct A {
    void foo() const {
        std::cout << "A's this: " << this << std::endl;
    }
    char pad0[32];
};

struct B {
    void bar() const {
        std::cout << "B's this: " << this << std::endl;
    }
    char pad2[64];
};

struct C : A, B
{ };

int main()
{
    C obj;
    obj.foo();
    obj.bar();
}
/*
A's this: 0x7fff57ddfb48
B's this: 0x7fff57ddfb68
*/
“this” 指针的值传给 B 的方法要比 A 的方法要大 32 字节——一个类 A 对象的实际大小。
```

`g++ -fno-elide-constructors`阻止部分编译优化

```c++
int *(*fun(int*))(int*);
=>fun先与(int*)结合，接收一个参数int*
  int ** fun(int*)(int*)
=>typedef int** (*FP)(int*);
  FP (int *);
```

```c++
int* fun(int* x){
    return NULL;
}
int* (*test(int* ))(int*){
    cout << "test\n";
    return fun1;
}
int main(){

    int*  (*(*f)(int*))(int*) = test;
    //f是一个函数指针，接受一个参数(int*)
    //返回值也是一个函数指针int* (*) (int*)
    f(NULL);
}

```



### 指针和引用

* 没有所谓空引用
* 引用必须有初值
* 使用引用不能测试其有效性
* pointer可以重新赋值，指向另一个对象



### 类型转换

static_cast基本与C旧式转型一致，不能用static_cast将一个struct转为int,或将一个double转为pointer,不能移除const性质

```c++
int main(){
    int *a = new int;
    cerr << (size_t)(a) << '\n';
    //报错了???
    cerr << static_cast<size_t>(a) << '\n';
}
```

能够将任意类型指针转成`void*`，通过`void*` 转成其他类型指针

const_cast 用来改变表达式的常量性、易变性

将一个指针或引用去掉const

```c++
int j = 0;
const int i = j;
int &k = const_cast<int &>(i);
k++;
printf("%d", i);


string a = "123";
char *p = const_cast<char*>(a.c_str());
strcpy(p, "abc");
printf("%s", a.c_str());
```

dynamic_cast 安全的向下转型或跨系转型动作

`dynamic_cast` can only cast to a pointer value or reference, dynamic 转换时的类必须有虚函数

`reinterpret_cast`不具有移植性

### 绝对不要以多态方式处理数组

基类数组元素大小和derived类不一致，数组产生的偏移不一样

### C++的const类型成员函数

* 在C++中只有被声明为const的成员函数才能被一个const类对象调用
* const成员函数可以被对应的具有相同形参列表的非const成员函数重载

```c++
void fun(int a，int b) const{}

void const fun(int a,int b){}
```

这两种写法的本质是：void fun (const 类 *this, int a,int b);

**本质上，const指针修饰的是被隐藏的this指针所指向的内存空间，修饰的是this指针。**

### 重载<运算符

```c++
friend bool operator<(const A&a,const A&b){
        return a.x < b.x;
}
或
bool A::operator<(const A&a){
    return x < a.x;
}
```

==类引用成员、常量指针必须在构造函数初始化列表中完成初始化==

```c++
class A{
public:
    A(int x,int * y):x(x),y(y){}
    int& x;
    int * const y;
};
```

### 类型转换函数

* 两种函数允许编译器执行类型转换

  单自变量constructor

  ```c++
  class Name{
  public:
      Name(const string &s);
  };
  class Rational{
  public:
      Rational(int numerator=0,int denominator=1);
  };
  ```

  

  隐式类型转换操作符

  ```c++
  class Rational{
  public:
      operator double() const;//将Rational转为double
  };
  ```

### 前置后置

```c++
class UPInt{
public:
    UPInt& operator++();前置
    const UPInt operator++(int);//后置，返回const，避免出现i++++
}
UPInt& UPInt::operator++(){
    *this += 1;
    return *this;
}
const UPInt UPInt::operator++(int){
    UPInt oldValue = *this;
    ++(*this);
    return oldValue;
}
```

### 不要重载||，&&，及，运算符

函数调用语义会取代骤死式语义

* 函数调用动作执行时，所有参数都会被求值

* 未规定参数求值顺序

逗号表达式从左至右求值

不能重载的运算符：

```c++
. 
.* 
:: 
?:
new 
delete
sizeof
typeid
static_cast
dynamic_cast
const_cast
reinterpret_cast
```

### 不同意义的new和delete

```c++
string *ps = new string("Memory Management");
//new operator
```

`new operator`由语言内建的，类似sizeof,不能改变意义

`operator new`

```c++
void * operator new(size_t size);
```

可以重载，但需保证第一个参数为size_t

```c++
void *rawMemory = operator new(sizeof(string));
```

operator new 和malloc一样，唯一任务是分配内存

`placement new`

有一些分配好的内存上直接构建对象

```c++
new (buffer) Widget();
```

如果只想处理原始的、未设初值的内存，应该回避new operator 和delete operator,改用operator new 和operator delete

如果使用placement new ，不应该调用delete，调用相应对象析构函数即可



`operator new[]`可以重载

数组版`new operator`先调用`operator new[]`分配内存，后为每个元素调用构造函数

数组版delete operator先为每个元素调用析构函数，后调用`operator delete[]`释放空间

### 在constructor内阻止内存泄漏

析构函数只负责析构构造好的对象，构造过程中发生异常不会引发析构函数调用

### 禁止异常流出destructor

如果基于exception的因素离开destructor,此时正有另一个exception处于作用状态，c++会调用terminate函数，程序立即结束

如果exception从destruction流出而没得到任何处理，会导致析构函数执行不全

### 实现shared_ptr

```c++
template <class T>
class Shared_ptr{
public:
    Shared_ptr(T *p):ptr(p),_use_count(new int(1)){}
    Shared_ptr(Shared_ptr<T>&other):_use_count(&(++(*other._use_count))),ptr(other.ptr){}
    Shared_ptr<T>& operator=(Shared_ptr<T>& sp){
        if(*this == sp){//处理自我赋值
            return *this;
        }
        ++(*sp._use_count);
        --(*this->_use_count);
        if(!(*(this->_use_count))&&this->ptr){
            delete ptr;
            delete _use_count;
        }
        this->_use_count= sp._use_count;
        this->ptr = sp.ptr;
        return *this;
    }
    T& operator*(){//返回值是引用，避免当前指针指向派生类对象造成对象切割问题
        return *ptr;
    }
    T* operator->(){
        return ptr;
    }

    ~Shared_ptr(){
        --(*_use_count);
        if(!*_use_count){
            delete ptr;
            delete _use_count;
        }
    }
    operator void*() //隐式转换，有隐式转换才能写如:if(p) if(!p) if(p == 0)语句 
    {
        if(!ptr)return 0;
        return ptr;
    }
    int use_count(){
        return *_use_count;
    }
private:
    int* _use_count;//动态内存分配，保证所有的Shared_ptr共用一份use_count,节省内存
    T *ptr;
};
int main(){
   Shared_ptr<int> p(new int(2));
   cerr << p.use_count() << '\n';
   Shared_ptr<int> c = p;
   cerr << p.use_count() << '\n';
   cerr << c.use_count() << '\n';
   cerr << (*c);
}
```





### 抛出一个exception与传递一个参数差异

一个对象被抛出无论是以by value和by reference方式传递都会发生复制行为，因为抛出异常时，控制权会离开当前作用域，其他局部变量会被销毁，只能通过复制保存对象状态。

* 即使是静态局部变量，复制行为也会发生

```c++
class A{
public:
    A(){
        cerr << "A constructor\n";
    }
    A(const A& a){
        cerr << "A copy constructor\n";
    }
    virtual ~A(){
        cerr << "A destructor\n";
    }
    virtual void print(){
        cerr << "A\n";
    }
};

class B:public A{
public:

    B(){
        cerr << "B constructor\n";
    }
    B(const B& b){
        cerr << "B copy constructor\n";
    }
    ~B(){
        cerr << "B destructor\n";
    }
    virtual void print(){
        cerr << "B\n";
    }
};


int main(){
   B b;
   A&a = b;
   a.print();//B
   A c = a;//调用A的复制函数，只关注静态类型
   c.print();//A
   
   A* x = new B;
   x->print();//B
   A* y = x;
   y->print();//B
}
```

一个被抛出的临时对象可以被左值引用捕捉，不需要`by reference-to-const`方式，函数调用将一个临时对象传递给一个左值引用是不合法的

by value 方式传递exception,会调用两次复制构造函数，第一次产生一个临时对象，第二次将临时对象复制给参数`w`

by reference只会调用一次复制构造函数，产生一个临时对象

exception和catch子句匹配不会发生隐式类型转换

```c++
void f(int value){
    try{
        if(someFunction()){
        	throw value;
    	}
    }
    catch(double d){//不会捕捉value
        
    }
}
```

有两种转换可以发生：

* 为base class exceptions写的catch子句可以捕捉derived class exceptions

* 有形指针到无形指针

  ```c++
  catch(const void *)...//可以捕捉任意指针类型
  ```

  catch子句以其在源代码中出现的顺序匹配（first fit)。

`mutable`关键字修饰的member成员能在const member functions中改变。实现`lazy fetching`,对象读取可能需要在const member function内进行



### 临时对象

只要你产生了一个non-heap object而没有为它命名，便诞生了一个临时对象。

此等匿名对象通常发生于：

* 当隐式转换被施行起来以求函数能够调用成功
* 当函数返回对象的时候

```c++
size_t countChar(const string &s,char ch);
char buffer[MAX_STRING_LEN];
char c;
cin >> c >> setw(MAX_STRING_LEN) >> buffer;
cout << "These are "<< countChar(buffer,c);
//countChar 接收const string &类型，传入的却是char[]
//会调用string的构造器，以buffer为参数生成临时string对象
//当countChar返回时，临时对象自动销毁
```

只有当对象以by value或reference-to-const参数时转换才会发生

如果对象传给一个reference-to-no-const,并不会发生这种转换

```c++
void uppercasify(string & str);
char sub[] = "Effective C++";
uppercasify(sub);//报错
//期望是修改原对象，如果允许生成临时对象，修改的只是临时对象
```

```c++
const Number operator+(const Number&a,const Number&b);
```

返回值是一个临时对象

### 返回值优化（RVO)

返回所谓`constructor arguments`以取代对象

```c++
const Rational operator*(const Rational &lhs,const Rational &rhs){
    return Rational(lhs.numerator()*rhs.numerator(),lhs.denominator(),rhs.denominator());
}
```

### 利用重载技术避免隐式类型转换

```c++
class A{
public:
    A(int x=0):x(x){}
    int x;
};
A get(){
    return A();
}

int main(){
    //允许
    get() = 2;
    //允许
    A&&a = get();
}

```

```c++
class Rational{
public:
    Rational(int x,int y):x(x),y(y){
    }
    Rational& operator+=(const Rational& rhs){
        this->x = this->x*rhs.y + this->y*rhs.x;
        this->y = this->y*rhs.y;
        int z = __gcd(this->x,this->y);
        this->x/=z;
        this->y/=z;
        return *this;
    }


    int x,y;
};
//返回const,避免写出类似a+b = c;表达式
const Rational operator+(const Rational&lhs,const Rational &rhs){
        //调用的复制构造函数
        return Rational(lhs) += rhs;
    }

int main(){
   Rational a (1,2);
   Rational b(2,3);
   a += b;
   cerr << a.x << ' '<< a.y << '\n';
   a = a + b;
   cerr << a.x << ' ' << a.y << '\n';
}
```



```C++
Derived::Derived()
{
// 如果在堆上创建对象，为其分配堆内存；
// operator new的介绍参见条款 8
if (本对象在堆上)
this = ::operator new(sizeof(Derived));//在构造函数内无法知道对象是不是在堆上,对 this 赋值是非法的。  
Base::Base(); // 初始化 Base 部分,cannot call constructor 'Base::Base' directly, 通过函数调用访问构造函数也是不允许的。
dm1.string(); // 构造 dm1
dm2.string(); // 构造 dm2
dm3.string(); // 通过对象调用访问构造函数也是不允许的。  
}
```



```c++
//operator只能声明成友元
friend ostream & operator<<(ostream & str,A&a);
//第一个参数必须是ostream
//如果反过来就会出现 t << cout;形式调用
```

### 不要产生内含local static对象的inline non-member functions

`inline non-member functions`意味着这个函数有内部连接（`internal linkage`)

函数如果有内部连接，可能在程序中被复制，也就是程序目标代码可能会对带有内部连接的函数复制一份以上代码，而此复制行为包括函数内的staic对象

如果有一个inline non-member function并于其中包含local static对象，程序可能会产生多个static副本



带有private constructors的class不能被继承导致禁止派生

只有const static member能在类定义区内指定初值

```c++
class Printer{
private:
    static size_t numObjects;
    static const size_t maxObjects = 10;//类内指定
};
size_t Printer::numObjects = 0;//类外指定
```

==智能指针没法管理栈上的对象==,事实上也不需要，离开作用域自动析构

### 在成员函数调用delete this

在类的成员函数中能不能调用delete this？答案是肯定的，能调用，而且很多老一点的库都有这种代码。假设这个成员函数名字叫release，而delete this就在这个release方法中被调用，那么这个对象在调用release方法后，还能进行其他操作，如调用该对象的其他方法么？答案仍然是肯定 的，调用release之后还能调用其他的方法，但是有个前提：被调用的方法不涉及这个对象的数据成员和虚函数。说到这里，相信大家都能明白为什么会这样 了。

**根本原因**在于delete操作符的功能和类对象的内存模型。当一个类对象声明时，系统会为其分配内存空间。**在类对象的内存空间中，只有数据成员和虚函数表指针，并不包含代码内容，类的成员函数单独放在代码段中**。在调用成员函数时，隐含传递一个this指针，让成员函数知道当前是哪个对象在调用它。当 调用delete this时，类对象的内存空间被释放。**在delete this之后进行的其他任何函数调用，只要不涉及到this指针的内容，都能够正常运行**。一旦涉及到this指针，如操作数据成员，调用虚函数等，就会出现**不可预期**的问题。

为什么是不可预期的问题？**delete this之后不是释放了类对象的内存空间了么**，那么这段内存应该已经还给系统，不再属于这个进程。照这个逻辑来看，应该发生**指针错误**，**无访问权限之类的令系统崩溃**的问题才对啊？这个问题牵涉到操作系统的内存管理策略。**delete this释放了类对象的内存空间，但是内存空间却并不是马上被回收到系统中，可能是缓冲或者其他什么原因，导致这段内存空间暂时并没有被系统收回**。此时这段内存是可以访问的，你可以加上100，加上200，但是其中的值却是不确定的。当你获取数据成员，可能得到的是一串很长的未初始化的随机数；访问虚函数表，指针无效的可能性非常高，造成系统崩溃。


大致明白在成员函数中调用delete this会发生什么之后，再来看看另一个问题，如果在类的析构函数中调用delete this，会发生什么？实验告诉我们，会导致堆栈溢出。原因很简单，delete的本质是“为将被释放的内存调用一个或多个析构函数，然后，释放内存” (来自effective c++)。显然，**delete this会去调用本对象的析构函数，而析构函数中又调用delete this，形成无限递归，造成堆栈溢出，系统崩溃**。

**1.在普通的非const成员函数中：**this的类型是一个指向类类型的const指针，可以改变this指向的值，但是不能改变this所保存的地址

2.在const成员函数中，this的类型是一个指向const类类型对象的const指针，既不能改变this所指向的对象，也不能改变this所保存的地址。

### 关于成员函数内调用memset(this,0,sizeof(*this))

会将对象内存按位清零，包括成员变量、虚指针、虚基类指针等信息

```c++
class A
{
public:
    virtual void test(){
        cerr << "nothing\n";
    }
    A()
    {
        cerr << "A\n";
    }
    ~A()
    {
        cerr << "~A\n";
    }
};
class B:public A
{
public:

    B()
    {
        x = 2;
        cerr << "B\n";
    }
    ~B()
    {
        cerr << this << '\n';
        cerr << "~B\n";
    }
    void test(){
        cerr << x << '\n';
        cerr << sizeof(*this) << '\n';
        memset(this,0,sizeof(*this));
    }
    int x;
};

int main()
{   A *a = new B();
    a->test();
    a->test();//会发生段错误，虚指针已经被清零
    /**
    B b;
    b.test();
    b.test();//调用没问题，但数据确是清零了，原因在于对象调用虚函数不会通过虚机制，会以B::test()形式调用
    */
}
```

### push_back emplace_back

```c++
class A
{
public:
    A() {}
    A(int x,int y=0):x(x),y(2)
    {
        cerr << "A constructor\n";
    }
    A(const A& a):x(a.x)
    {

        cerr << "A copy constructor\n";
    }
    A(A&& a):x(std::move(x))
    {
        cerr << "move constructor\n";
    }
    ~A()
    {
        cerr << "~A\n";
    }
    int x,y;
};

int main()
{
    vector<A> vec;
    for(int i = 0; i < 10; i++)
    {
        cerr << '\n';
        cerr << "push_back\n";
        //vec.push_back(2,2);不被允许
        vec.push_back(2);//此时会先调用A constructor生成临时对象a,然后再调用move constructor
        cerr << "push end\n";
        cerr << '\n';


        cerr << "emplace back\n";
        vec.emplace_back(2,2);//会直接调用constructor
        
        cerr << "emplace end\n";
        cerr <<'\n';
    }
   //如下情况是没有区别的
    for(int i = 0; i < 10; i++){
        A a(2);
        vec.push_back(a);
        vec.emplace_back(a);//都会调用copy constructor
        
        vec.push_back(A(2));
        vec.emplace_back(A(2));//都会调用constructor and move constructor
    }
}



```



```c++
class A
{
public:
    void test(){
        cerr << "test\n";
    }
    void test()const{
        cerr << "const test\n";
    }
};

int main()
{
    A a;
    a.test();//test
    const A b;
    b.test();//const test
}
```

==可以定义纯虚析构函数，但是纯虚析构函数必须有定义==

```c++
class A{
public:
    virtual ~A() = 0;
}
A::~A(){}
```

```c++
class A
{
public:
    //这是非法的
    int& test()const{
        return x;
    }
    int* test()const{
        return (&x);
    }
    const int& test()const{//合法
        return x;
    }
    
    int x;
};
//More Effective C++  p203疑似有误
template<class T>
T* RCPtr<T>::operator->()const{return pointee;}
template<class T>
T& RCPtr<T>::operator*()const{return *pointee};
```

==传参时隐式类型转换产生临时对象只发生参数以by value或者reference-to-const形式传递时发生，通过reference-to-non-const形式传递不会发生，因为可能改变reference-to-non-const的值，而隐式类型转换会产生临时对象，发生的改变只作用在临时对象上==

```c++
int test(int&x){
    x = 2;
    return x;
}
int main(){
    double x = 2.0;
    test(x);//cannot bind non-const lvalue reference of type 'int&' to an rvalue of type 'int'
}

```



```c++
void print(int func(int)){
    ::std::cout <<func;//cout未对函数指针进行重载，会把函数指针隐式转换为bool
}
void print(short num){
    ::std::cout << num;
}
int main(){
    print(::std::putchar);
   // print(0);0的类型是int,可以转换为short或指针， call of overloaded 'print(int)' is ambiguous
}


```



### 空对象调用成员函数

```c++
class Nod{
public:

    void printD(){
        cerr << "dynamic print\n";
    }
    static void printS(){
        cerr << "static print\n";
    }
    virtual void printV(){
        cerr << "virtual print\n";
    }
};
int main(){
   Nod * a = nullptr;
   a->printS();//静态函数，不涉及this指针，没问题
   a->printD();//不涉及Nod成员变量访问，没问题，涉及成员变量会得到段错误
   a->printV();//段错误
}

```

### 实现final

1）如果类的构造函数或析析构函数声明为私有的，那么该类不能被继承，但同时该类也不能使用；

2）派生类只能访问基类的公有成员和保护成员，如果是私有继承，基类中所有成员到子类中将成为私有的，子类的派生类也即子类的子类只能访问其直接父类的公有成员或保护成员，不能访问最原始基类的任何成员；

3）如果有三个类A、B、C，B虚拟继承A，C继承B，则意味着C将直接继承A和B，也即构造C的对象时，将会直接调用A的构造函数

(下述解决方案g++不报错)

```c++
class FinalBase {
protected:
	~FinalBase() {}
};
 
class Final : virtual private FinalBase {
public:
	void foo() {
		cout << "i'm a final class" << endl;
	}
};
 
void tfinalclass() {
	Final obj;
	obj.foo();
}


template<typename T> class MakeFinally{
   private:
       MakeFinally(){};//只有MakeFinally的友类才可以构造MakeFinally
       ~MakeFinally(){};
   friend T;
};

class MyClass:public virtual  MakeFinally<MyClass>{};//MyClass是不可派生类

//由于虚继承，所以D要直接负责构造MakeFinally类，从而导致编译报错，所以D作为派生类是不合法的。
class D: public MyClass{};
```

（好像也不行）

- 父类写一个纯虚函数 —— 子类**必须**实现这一函数
- 这个纯虚函数放在 `private` 区域 —— 子类**不能**实现这一函数
