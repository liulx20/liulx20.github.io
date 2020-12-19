---
title: haskell
date: 2020-08-27 10:34:16
tags: haskell
---

## Introduction to Haskell

* Functions are first-class, that is, functions are values which can be used in exactly the same ways as any other sort of value.

* The meaning of Haskell programs is centered around evaluating expressions rather than executing instructions.
<!-- More -->
### 安装
```
sudo apt-get install haskell-platform
```
开启交互模式
```
ghci
```
`Ctrl + z` 退出交互模式

导入`test.hs`文件
```
:l test.hs
```
### type

GHCi is an interactive Haskell REPL (Read-Eval-Print-Loop) that comes with GHC. At the GHCi prompt, you can evaluate expressions, load Haskell files with :load (:l) (and reload them with :reload (:r)), ask for the type of an expression with :type (:t), and many other things (try :? for a list of commands).
```
ex01 = 3 + 2
ex02 = 8 / 2 --(4.0)
ex03 = mod 19 3
ex04 = 19 `mod` 3
ex05 = 7 ^ 222
ex06 = (-3) * (-7)
```
* `backticks` make a function name into an infix operator.
* negative numbers must often be surrounded by parentheses, to avoid having the negation sign parsed as subtraction.

```
-- badArith1 = i + n
```
* Addition is only between values of the same numeric type, Haskell does not do implicit conversion,you must explicitly convert with:
 
  fromIntegral: converts from any integral type (Int or Integer) to any other numeric type.

  round, floor, ceiling: convert floating-point numbers to Int or Integer.
```
-- badArith2 = i / i
```
* This is an error since / performs floating-point division only. For integer division we can use div.
```
ex07 = i `div` i
```

### Boolean logic
```
ex08 = True && False
ex09 = not (False || True)
ex10 = 2 /= 3 (/= 不等于)
```
*  `if-expressions`: if b then t else f

the else part is required for an if-expression, since the if-expression must result in some value. 

### function

* function application has higher precedence than any infix operators

### List

```
hello1 :: [Char]
hello1 = ['h', 'e', 'l', 'l', 'o']

hello2 :: String
hello2 = "hello"

helloSame = hello1 == hello2
```

##  Algebraic Data Types 

### Enumeration types
```
data Thing = Shoe 
           | Ship 
           | SealingWax 
           | Cabbage 
           | King
  deriving Show
```
* The deriving Show is a magical incantation which tells GHC to automatically generate default code for converting Things to Strings.
```
shoe :: Thing
shoe = Shoe

listO'Things :: [Thing]
listO'Things = [Shoe, SealingWax, King, Cabbage, King]
```

* We can write functions on Things by pattern-matching.
```
isSmall :: Thing -> Bool
isSmall Shoe       = True
isSmall Ship       = False
isSmall SealingWax = True
isSmall Cabbage    = True
isSmall King       = False
```
or
```
isSmall2 :: Thing -> Bool
isSmall2 Ship = False
isSmall2 King = False
isSmall2 _    = True
```

### Beyond enumerations
```
data FailableDouble = Failure
                    | OK Double
  deriving Show
```
```
ex01 = Failure
ex02 = OK 3.4
```
```
safeDiv :: Double -> Double -> FailableDouble
safeDiv _ 0 = Failure
safeDiv x y = OK (x / y)
```
```
failureToZero :: FailableDouble -> Double
failureToZero Failure = 0
failureToZero (OK d)  = d
```

* Data constructors can have more than one argument.
```
-- Store a person's name, age, and favourite Thing.
data Person = Person String Int Thing
  deriving Show

brent :: Person
brent = Person "Brent" 31 SealingWax

stan :: Person
stan  = Person "Stan" 94 Cabbage

getAge :: Person -> Int
getAge (Person _ a _) = a
```

* the type constructor and data constructor are both named Person.

### Algebraic data types in general

```
data AlgDataType = Constr1 Type11 Type12
                 | Constr2 Type21
                 | Constr3 Type31 Type32 Type33
                 | Constr4
```

* This specifies that a value of type AlgDataType can be constructed in one of four ways.

*  type and data constructor names must always start with a capital letter; variables (including names of functions) must always start with a lowercase letter.

### Pattern-matching

We could write something like
```
foo (Constr1 a b)   = ...
foo (Constr2 a)     = ...
foo (Constr3 a b c) = ...
foo Constr4         = ...
```

* parentheses are required around patterns consisting of more than just a single constructor.

* An underscore _ can be used as a “wildcard pattern” which matches anything.

* A pattern of the form x@pat can be used to match a value against the pattern pat, but also give the name x to the entire value being matched. For example:
```
baz :: Person -> String
baz p@(Person n _ _) = "The name field of (" ++ show p ++ ") is " ++ n

*Main> baz brent
"The name field of (Person \"Brent\" 31 SealingWax) is Brent"
```

* 字符串用++连接

* Patterns can be nested. For example:
```
checkFav :: Person -> String
checkFav (Person n _ SealingWax) = n ++ ", you're my kind of person!"
checkFav (Person n _ _)          = n ++ ", your favorite thing is lame."

*Main> checkFav brent
"Brent, you're my kind of person!"
*Main> checkFav stan
"Stan, your favorite thing is lame."
```

In general, the following grammar defines what can be used as a pattern:

```
pat ::= _
     |  var
     |  var @ ( pat )
     |  ( Constructor pat1 pat2 ... patn )
```

### Case expressions
```
case exp of
  pat1 -> exp1
  pat2 -> exp2
  ...
```
like this:
```
ex03 = case "Hello" of
           []      -> 3
           ('H':s) -> length s
           _       -> 7
```

### Recursive data types

* A list is either empty, or a single element followed by a remaining list.

```
data IntList = Empty | Cons Int IntList
```
* Use recursive functions to process recursive data types.
```
intListProd :: IntList -> Int
intListProd Empty      = 1
intListProd (Cons x l) = x * intListProd l
```
* we can define a type of binary trees with an Int value stored at each internal node, and a Char stored at each leaf:
```
data Tree = Leaf Char
          | Node Tree Int Tree
  deriving Show
```

## Haskell Prelude function

### 乘方函数
* ^ 的底数可为小数，也可为整数，指数是正整数；
* ^^ 的底数是小数，指数是任意整数；
* ** 的底数和指数都是小数)

### 数值函数
* signum 取符号 `signum (-3) == -1`
* negate 相反数 `negate (-1) == 1`
* abs 绝对值 
* recip 倒数
* floor 向下取整
* ceiling 向上取整
* round 四舍五入
* truncate 取整
* exp e的次幂
* subtract 减去 `subtract 3 5 == 2`
* gcd lcm
* sqrt
* max min
* compare 比较 `compare 3 5 == LT` `compare 5 3 == GT` `compare 5 5 == EQ`

### 三角函数
* pi
* sin cos
* tan 
* asin acos
* atan atan2
* sinh cosh tanh asinh acosh atanh

### 对数函数
* log     exp为底
* logBase `logBase 10 10 == 1.0`

### 判断奇偶
* odd even

### pair函数
* fst snd

### 列表函数
* (!!) 获取列表第几个元素 `[0,1,2,3] !! 1 == 1`
* lookup `lookup 2 [(1, 'a'), (2, 'b'), (3, 'c')]== 'b'` 获取列表中第一个元素为2的元组中第二个元素
* elem notElem 判断元素是否在列表中 `elem 2 [1,2,3] == True`
* null 判断列表是否为空 `null [] == True`
* and or 用于Bool列表 `and [False,True,True] == False`
* all any 判断列表是否所有(存在)元素满足条件 `all even [2,3,4] == False`
* (++) 列表连接
* length 求列表长度
* head 列表第一个元素
* tail 取列表除了第一个元素的所有元素
* last 取列表最后一个元素
* init 取列表除最后一个元素
* reverse 列表反转
* cycle 反复出现列表
* repeat 反复出现某一值
* replicate 重复出现某一值一定次数 `replicate 3 1 == [1,1,1]`
* take `take 2 [1, 2, 3, 4] == [1,2]` 取列表前两个元素
* drop `drop 2 [1, 2, 3, 4] == [3,4]` 去除列表前两个元素
* splitAt `splitAt 1 [1,2,3,4] == ([1],[2,3,4])`分割列表
* takeWhile `takeWhile even [2, 4, 5] == [2,4]` `takeWhile odd [2, 4, 5] == []` 获取满足某一条件的前几个元素
* dropWhile `dropWhile odd [2, 4, 5] == [5]` `dropWhile odd [2, 4, 5] == [2,4,5]`丢弃满足某一条件的前几个元素
* span `span even [2, 4, 5] == ([2,4],[5])` 分割列表，规则同 takeWhile
* break `break odd [2, 4, 5] == ([2,4],[5])`分割列表，规则同 dropWhile
* maximum 列表最大元素
* minimum
* sum
* product 列表元素乘积
* enumFrom `enumFrom 2 == [2,3,4,...]`
* enumFromThen `enumFromThen 5 3 == [5,3,1,-1,...]`
* enumFromThenTo `enumFromThenTo 5 3 1 == [5,3,1]`
* enumFromTo `enumFromTo 3 5 == [3,4,5]` `enumFromTo 3 1 == []`
* show `show [2,3] == "[2,3]"` `show "2" == "\"2\""`
* read `read "233"::Int == 233` `read "12"::Double == 12.0`
* iterate creates an infinite list where the first item is calculated by applying the function on the second argument, the second item by applying the function on the previous result and so on.
` take 4 (iterate (2*) 1) == [1,2,4,8]` `take 4 (iterate (\x -> (x+3)*2) 1) == [1,8,22,50]`
* until applies a function which is passed as the second argument to the third argument and it comapares the result with the condition, if the condition evaluates to True, it prints the result, if not, it passes the result to the finction and repeats the cycle as long as the condition is matched
`until (> 100) (*2) 1 == 128` `until odd ( `div` 2) 400 == 25`
* zip `zip [1, 2] [4, 5] = [(1,4),(2,5)]`
* zip3 `zip3 [1, 2] [4, 5] [7, 8] = [(1,4,7),(2,5,8)]`
* zipWith `zipWith (+) [1, 2, 3] [4, 5, 6] = [5,7,9]`
* zipWith3 `zipWith3 (\x y z -> x + y + z) [1, 2, 3] [4, 5, 6] [7, 8, 9] == [12,15,18]`
* unzip `unzip [(1, 4), (2, 5), (3, 6)] == ([1,2,3],[4,5,6])`
* unzip3 `unzip3 [(1, 4, 7), (2, 5, 8), (3, 6, 9)] == ([1,2,3],[4,5,6],[7,8,9])`


#### String
* lines 分割行 `lines "abc\n123\ndef\n" == ["abc","123","def"]`
* words 分割单词 ` words "abc\n123 def\t" == ["abc","123","def"]`
* unlines 合并行 `unlines ["a","b","c"] == "a\nb\nc\n"`
* unwords 合并单词 `unwords ["a","b"] == "a b"`

### 其他
* (.) 函数复合 (f.g) x == f(g x)
* ($) apply 函数，通常是为了省写括号
`(map Char.toUpper . filter Char.isLower) "ABCdef" == "DEF"`
`map Char.toUpper . filter Char.isLower $ "ABCdef" == "DEF"`

## Recursion patterns, polymorphism, and the Prelude

### Recursion patterns

#### Map
```
ls = [1,2,3]
addOne x = x+1
map addOne ls
```

#### Filter
When we want to keep only some elements of a list, and throw others away, based on a test.

#### Fold
“summarize” the elements of the list

### Polymorphism

#### Polymorphic data types
First, let’s see how to declare a polymorphic data type.
```haskell
data List t = E | C t (List t)
```
非泛型
```haskell
data IntList = Empty | Cons Int IntList
  deriving Show
```
* We have data List t = ... The t is a type variable which can stand for any type. 
* data List t = ... means that the List type is parameterized by a type, in much the same way that a function can be parameterized by some input.
```
lst1 :: List Int
lst1 = C 3 (C 5 (C 2 E))

lst2 :: List Char
lst2 = C 'x' (C 'y' (C 'z' E))

lst3 :: List Bool
lst3 = C True (C False E)
```

#### Polymorphic functions
```haskell
filterList :: (t -> Bool) -> List t -> List t    
filterList _ E = E
filterList p (C x xs)
  | p x       = C x (filterList p xs)
  | otherwise = filterList p xs
```
```haskell
mapList :: (a -> b) -> List a -> List b
mapList _ E        = E
mapList f (C x xs) = C (f x) (mapList f xs)
```

### The Prelude

#### Maybe
```
data Maybe a = Nothing | Just a
```
* A value of type Maybe a either contains a value of type a (wrapped in the Just constructor), or it is Nothing (representing some sort of failure or error). The Data.Maybe module has functions for working with Maybe values.

```
maybe False odd (Just 3) == True
```

#### Total and partial functions

* Functions which have certain inputs that will make them recurse infinitely are also called partial.
* Functions which are well-defined on all possible inputs are known as total functions.
* head is what is known as a partial function: there are certain inputs for which head will crash.
* tail, init, last, and (!!) are partial functions
```
head([])
*** Exception: Prelude.head: empty list
```
#### Replacing partial functions
Replace
```
doStuff1 :: [Int] -> Int
doStuff1 []  = 0
doStuff1 [_] = 0
doStuff1 xs  = head xs + (head (tail xs)) 
```
as
```
doStuff2 :: [Int] -> Int
doStuff2 []        = 0
doStuff2 [_]       = 0
doStuff2 (x1:x2:_) = x1 + x2
```

### Writing partial functions

What if you find yourself writing a partial functions?

#### Change the output type of the function to indicate the possible failure.

```
data Maybe a = Nothing | Just a
```
We could rewrite `head` safely like this
```
safeHead :: [a] -> Maybe a
safeHead []    = Nothing
safeHead (x:_) = Just x
```
#### if some condition is really guaranteed, then the types ought to reflect the guarantee! Then the compiler can enforce your guarantees for you.
```
data NonEmptyList a = NEL a [a]

nelToList :: NonEmptyList a -> [a]
nelToList (NEL x xs) = x:xs

listToNel :: [a] -> Maybe (NonEmptyList a)
listToNel []     = Nothing
listToNel (x:xs) = Just $ NEL x xs

headNEL :: NonEmptyList a -> a
headNEL (NEL a _) = a

tailNEL :: NonEmptyList a -> [a]
tailNEL (NEL _ as) = as
```

## Higher-order programming and type inference

### Anonymous functions

```haskell
gt100 :: Integer -> Bool
gt100 x = x > 100

greaterThan100 :: [Integer] -> [Integer]
greaterThan100 xs = filter gt100 xs
```
anonymous function:
```haskell
greaterThan100_2 :: [Integer] -> [Integer]
greaterThan100_2 xs = filter (\x -> x > 100) xs
```
* \x -> x > 100 (the backslash is supposed to look kind of like a lambda with the short leg missing) is the function which takes a single argument x and outputs whether x is greater than 100.
* lambda abstractions can also have multiple arguments.
```
(\x y z -> [x,2*y,3*z]) 5 6 3 == [5,12,9]
```
*  if ? is an operator, then (?y) is equivalent to the function \x -> x ? y, and (y?) is equivalent to \x -> y ? x.
```
(>100) 102 == True
(100>) 102 == False
```
`(- 1) 2`不可行？ 

### Function composition
``` 
foo :: (b -> c) -> (a -> b) -> (a -> c)
foo f g = \x -> f (g x)
```
* foo is really called (.), and represents function composition. That is, if f and g are functions, then f . g is the function which does first g and then f.

```
myTest :: [Integer] -> Bool
myTest xs = even (length (greaterThan100 xs))
```
We can rewrite this as:
```
myTest :: [Integer] -> Bool
myTest xs = even.length.greaterThan100 xs
```
```
Prelude> :t (.)
(.) :: (b -> c) -> (a -> b) -> a -> c
```

### Currying and partial application
```
f :: Int -> Int -> Int
f x y = 2*x + y
```
equivalently write f’s type like this:
```
f' :: Int -> (Int -> Int)
f' x y = 2*x + y
```
* representing multi-argument functions as one-argument functions returning functions
* If we want to actually represent a function of two arguments we can use a single argument which is a tuple.
```
f'' :: (Int,Int) -> Int
f'' (x,y) = 2*x + y
```
* In order to convert between the two representations of a two-argument function, the standard library defines functions called curry and uncurry, defined like this
```
schönfinkel :: ((a,b) -> c) -> a -> b -> c
schönfinkel f x y = f (x,y)

unschönfinkel :: (a -> b -> c) -> (a,b) -> c
unschönfinkel f (x,y) = f x y
```
* uncurry in particular can be useful when you have a pair and want to apply a function to it. For example:
```
Prelude> uncurry (+) (2,3)
5
```
#### Partial application

* In Haskell there are no functions of multiple arguments! 
* Every function can be “partially applied” to its first (and only) argument, resulting in a function of the remaining arguments.
* Haskell doesn’t make it easy to partially apply to an argument other than the first. 
* he one exception is infix operators, which as we’ve seen, can be partially applied to either of their two arguments using an operator section. 

#### Wholemeal programming
```
foobar :: [Integer] -> Integer
foobar []     = 0
foobar (x:xs)
  | x > 3     = (7*x + 2) + foobar xs
  | otherwise = foobar xs
```
```
foobar' :: [Integer] -> Integer
foobar' = sum . map (\x -> 7*x + 2) . filter (>3)
```

### Folds
We have one more recursion pattern on lists to talk about: folds. 
all of them somehow “combine” the elements of the list into a final answer.

```haskell
sum' :: [Integer] -> Integer
sum' []     = 0
sum' (x:xs) = x + sum' xs

product' :: [Integer] -> Integer
product' [] = 1
product' (x:xs) = x * product' xs

length' :: [a] -> Int
length' []     = 0
length' (_:xs) = 1 + length' xs
``` 

define higher-order functions:


```haskell
fold :: b -> (a -> b -> b) -> [a] -> b
fold z f []     = z
fold z f (x:xs) = f x (fold z f xs)
```


```haskell
fold f z [a,b,c] == a `f` (b `f` (c `f` z))
```


```haskell
sum''     = fold 0 (+)
product'' = fold 1 (*)
length''  = fold 0 (\_ s -> 1 + s)

(Instead of (\_ s -> 1 + s) we could also write (\_ -> (1+)) or even (const (1+)).)
```

*  fold is already provided in the standard Prelude, under the name foldr
Here are some Prelude functions which are defined in terms of foldr:

```haskell
length :: [a] -> Int
sum :: Num a => [a] -> a
product :: Num a => [a] -> a
and :: [Bool] -> Bool
or :: [Bool] -> Bool
any :: (a -> Bool) -> [a] -> Bool
all :: (a -> Bool) -> [a] -> Bool
```


* There is also foldl, which folds “from the left”. 


```haskell
foldr f z [a,b,c] == a `f` (b `f` (c `f` z))
foldl f z [a,b,c] == ((z `f` a) `f` b) `f` c
```

* you should use foldl' from Data.List instead, which does the same thing as foldl but is more efficient.


## More polymorphism and type classes

### Parametricity

```
f :: a -> a -> a
f x y = x && y
```

The reason this doesn’t work is that the caller of a polymorphic function gets to choose the type. Here we, the implementors, have tried to choose a specific type (namely, Bool), but we may be given String, or Int, or even some type defined by someone using f, which we can’t possibly know about in advance. In other words, you can read the type
```
a -> a -> a
```
as a promise that a function with this type will work no matter what type the caller chooses.

### Two views on parametricity

```
(==) :: Eq a   => a -> a -> Bool
(<)  :: Ord a  => a -> a -> Bool
show :: Show a => a -> String
```
### Type classes

* Num, Eq, Ord, and Show are type classes, and we say that (==), (<), and (+) are “type-class polymorphic”.
* Intuitively, type classes correspond to sets of types which have certain operations defined for them, and type class polymorphic functions work only for types which are instances of the type class(es) in question.
```
class Eq a where
  (==) :: a -> a -> Bool
  (/=) :: a -> a -> Bool
```
* Eq is declared to be a type class with a single parameter, a.
* Any type a which wants to be an instance of Eq must define two functions, (==) and (/=), with the indicated type signatures.

```
(==) :: Eq a => a -> a -> Bool
```
* The Eq a that comes before the => is a type class constraint.
* We can read this as saying that for any type a, as long as a is an instance of Eq, (==) can take two values of type a and return a Bool.
* Let’s make our own type and declare an instance of Eq for it. 
```
data Foo = F Int | G Char

instance Eq Foo where
  (F i1) == (F i2) = i1 == i2
  (G c1) == (G c2) = c1 == c2
  _ == _ = False

  foo1 /= foo2 = not (foo1 == foo2)
```
* the Eq class is actually declared like this:
```
class Eq a where
  (==), (/=) :: a -> a -> Bool
  x == y = not (x /= y)
  x /= y = not (x == y)
```
This means that when we make an instance of Eq, we can define either (==) or (/=), whichever is more convenient; 

* As it turns out, Eq (along with a few other standard type classes) is special: GHC is able to automatically generate instances of Eq for us. Like so:
```
data Foo' = F' Int | G' Char
  deriving (Eq, Ord, Show)
```
This tells GHC to automatically derive instances of the Eq, Ord, and Show type classes for our data type Foo.

#### Type classes and Java interfaces

* Both define a set of types/classes which implement a specified list of operations.

1. When a Java class is defined, any interfaces it implements must be declared. Type class instances, on the other hand, are declared separately from the declaration of the corresponding types, and can even be put in a separate module.
2. The types that can be specified for type class methods are more general and flexible than the signatures that can be given for Java interface methods, especially when multi-parameter type classes enter the picture. For example, consider a hypothetical type class
```
class Blerg a b where
  blerg :: a -> b -> Bool
```
Using blerg amounts to doing multiple dispatch: which implementation of blerg the compiler should choose depends on both the types a and b. There is no easy way to do this in Java.
Haskell type classes can also easily handle binary (or ternary, or …) methods, as in
```
class Num a where
  (+) :: a -> a -> a
```
There is no nice way to do this in Java: for one thing, one of the two arguments would have to be the “privileged” one which is actually getting the (+) method invoked on it, and this asymmetry is awkward. Furthermore, because of Java’s subtyping, getting two arguments of a certain interface type does not guarantee that they are actually the same type, which makes implementing binary operators such as (+) awkward (usually requiring some runtime type checks).

#### Standard type classes
* Ord is for types whose elements can be totally ordered, that is, where any two elements can be compared to see which is less than the other. It provides comparison operations like (<) and (<=), and also the compare function.
* Num is for “numeric” types, which support things like addition, subtraction, and multipication. One very important thing to note is that integer literals are actually type class polymorphic:
```
Prelude> :t 5
5 :: Num a => a
```
This means that literals like 5 can be used as Ints, Integers, Doubles, or any other type which is an instance of Num (Rational, Complex Double, or even a type you define…)
* Show defines the method show, which is used to convert values into Strings.
* Read is the dual of Show.
* Integral represents whole number types such as Int and Integer.

#### A type class example
```
class Listable a where
  toList :: a -> [Int]
```
We can think of Listable as the class of things which can be converted to a list of Ints. Look at the type of toList:
```
toList :: Listable a => a -> [Int]
```
First, an Int can be converted to an [Int] just by creating a singleton list, and Bool can be converted similarly, say, by translating True to 1 and False to 0:
```haskell
instance Listable Int where
  -- toList :: Int -> [Int]
  toList x = [x]

instance Listable Bool where
  toList True  = [1]
  toList False = [0]
```
We don’t need to do any work to convert a list of Int to a list of Int:
```haskell
instance Listable [Int] where
    toList = id
```
Finally, here’s a binary tree type which we can convert to a list by flattening:
```haskell
data Tree a = Empty | Node a (Tree a) (Tree a)
instance Listable (Tree Int) where
    toList Node(x,l,r) = toList l ++ [x] ++ toList r
```
If we implement other functions in terms of toList, they also get a Listable constraint. 
```haskell
sumL x = sum (toList x)
```

ghci informs us that type type of sumL is
```haskell
sumL :: Listable a => a -> Int
```

```haskell
foo x y = sum (toList x) == sum (toList y) || x < y
```
type foo:
```haskell
foo :: (Listable a,Ord a) => a -> a -> Bool
```

```
instance (Listable a, Listable b) => Listable (a,b) where
  toList (x,y) = toList x ++ toList y
```
Notice how we can put type class constraints on an instance as well as on a function type. This says that a pair type (a,b) is an instance of Listable as long as a and b both are. Then we get to use toList on values of types a and b in our definition of toList for a pair. Note that this definition is not recursive! The version of toList that we are defining is calling other versions of toList, not itself.

## Lazy evaluation

### Strict evaluation
* Under a strict evaluation strategy, function arguments are completely evaluated before passing them to the function.
* The benefit of strict evaluation is that it is easy to predict when and in what order things will happen. 

### Side effects and purity
### Lazy evaluation
* Under a lazy evaluation strategy, evaluation of function arguments is delayed as long as possible: they are not evaluated until it actually becomes necessary to do so. 
* When some expression is given as an argument to a function, it is simply packaged up as an unevaluated expression (called a “thunk”, don’t ask me why) without doing any actual work.
### Pattern matching drives evaluation

```haskell
f1 :: Maybe a -> [Maybe a]
f1 m = [m,m]

f2 :: Maybe a -> [a]
f2 Nothing  = []
f2 (Just x) = [x]
```
* f1 uses its argument m, it does not need to know anything about it. m can remain completely unevaluated, and the unevaluated expression is simply put in a list. 
* f2, on the other hand, needs to know something about its argument in order to proceed: was it constructed with Nothing or Just.
* The other important thing to note is that thunks are evaluated only enough to allow a pattern match to proceed, and no further!
* suppose we wanted to evaluate f2 (safeHead [3^500, 49]). f2 would force evaluation of the call to safeHead [3^500, 49], which would evaluate to Just (3^500)—note that the 3^500 is not evaluated

`Expressions are only evaluated when pattern-matched`

`…only as far as necessary for the match to proceed, and no farther!`
### Consequences
#### Purity
#### Understanding space usage
```
-- Standard library function foldl, provided for reference
foldl :: (b -> a -> b) -> b -> [a] -> b
foldl _ z []     = z
foldl f z (x:xs) = foldl f (f z x) xs
```
```
  foldl (+) 0 [1,2,3]
= foldl (+) (0+1) [2,3]
= foldl (+) ((0+1)+2) [3]
= foldl (+) (((0+1)+2)+3) []
= (((0+1)+2)+3)
= ((1+2)+3)
= (3+3)
= 6
```
Since the value of the accumulator is not demanded until recursing through the entire list, the accumulator simply builds up a big unevaluated expression (((0+1)+2)+3), which finally gets reduced to a value at the end.
* One is that it’s simply inefficient: there’s no point in transferring all the numbers from the list into a different list-like thing (the accumulator thunk) before actually adding them up. 
* The second problem is more subtle, and more insidious: evaluating the expression (((0+1)+2)+3) actually requires pushing the 3 and 2 onto a stack before being able to compute 0+1 and then unwinding the stack, adding along the way. 
for very long lists it’s a big problem: there is usually not as much space available for the stack, so this can lead to a stack overflow.
* The solution in this case is to use the foldl' function instead of foldl, which adds a bit of strictness
#### Short-circuiting operators
```
(&&) :: Bool -> Bool -> Bool
True  && x = x
False && _ = False
```
#### User-defined control structures
In Haskell, however, we can define if as a library function!
```
if' :: Bool -> a -> a -> a
if' True  x _ = x
if' False _ y = y
```
#### Infinite data structures
#### Pipelining/wholemeal programming

#### Dynamic programming

Using lazy evaluation we can get the Haskell runtime to work out the proper order of evaluation for us! For example, here is some Haskell code to solve the 0-1 knapsack problem.
```
import Data.Array

knapsack01 :: [Double]   -- values 
           -> [Integer]  -- nonnegative weights
           -> Integer    -- knapsack size
           -> Double     -- max possible value
knapsack01 vs ws maxW = m!(numItems-1, maxW)
  where numItems = length vs
        m = array ((-1,0), (numItems-1, maxW)) $
              [((-1,w), 0) | w <- [0 .. maxW]] ++
              [((i,0), 0) | i <- [0 .. numItems-1]] ++
              [((i,w), best) 
                  | i <- [0 .. numItems-1]
                  , w <- [1 .. maxW]
                  , let best
                          | ws!!i > w  = m!(i-1, w)
                          | otherwise = max (m!(i-1, w)) 
                                            (m!(i-1, w - ws!!i) + vs!!i)
              ]

example = knapsack01 [3,4,5,8,10] [2,3,4,5,9] 20
```