---
title: haskell-hw
date: 2020-08-27 18:07:23
tags: haskell
---
homework of CIS194
## [hw1](https://www.seas.upenn.edu/~cis194/spring13/hw/01-intro.pdf)
<!--More-->
```haskell
-- Exercise 01
toDigits :: Integer -> [Integer]
toDigits x
   | x >= 0 && x < 10 = [x]
   | x > 10 = toDigits (x `div` 10) ++ [x `mod` 10]
   | otherwise = []

toDigitsRev :: Integer -> [Integer]
toDigitsRev x
   | x >= 0 && x < 10 = [x]
   | x > 10 = (x `mod` 10):toDigitsRev(x `div` 10)
   | otherwise = []


-- Exercise 02
len :: [Integer] -> Integer
len [] = 0
len (_:y) = 1 + len(y)


doubleEveryOther :: [Integer] -> [Integer]
doubleEveryOther [] = []
doubleEveryOther (x:[])= [x]
doubleEveryOther (x:y:z)= if(len(z) `mod` 2 == 0) then (x*2 : y : doubleEveryOther(z)) else (x:y*2:doubleEveryOther(z))

-- Exercise 3
sumDigit :: Integer -> Integer
sumDigit x
    | x < 10  = x
    | otherwise = (x `mod` 10) + sumDigit (x `div` 10) 

sumDigits :: [Integer] -> Integer
sumDigits [] = 0
sumDigits (x:y) = sumDigit(x) + sumDigits(y)

-- Exercise 4
validate :: Integer -> Bool
validate num
   | sumDigits(doubleEveryOther(toDigits(num))) `mod` 10 == 0 = True
   | otherwise = False

-- Exercise 5
type Peg = String
type Move = (Peg, Peg)
hanoi :: Integer -> Peg -> Peg -> Peg -> [Move]
hanoi n a b c
     | n == 1 = [(a,b)]
     | otherwise = (hanoi (n-1) a c b) ++ [(a,b)] ++ (hanoi (n-1) c b a)

-- Exercise 6

len2 :: [Move] -> Integer
len2 [] = 0
len2 (_:y) = 1 + len2 y

hanoi2 :: Integer -> Peg -> Peg -> Peg -> Peg -> [Move]
hanoi2 n a b c d
     | n == 1 = [(a,b)]
     | n == 2 = [(a,d),(a,b),(d,b)]
     | otherwise = (hanoi2 (n-2) a c b d) ++[(a,d),(a,b),(d,b)] ++ (hanoi2 (n-2) c b a d)


```
## [hw2](https://www.seas.upenn.edu/~cis194/spring13/hw/02-ADTs.pdf)
```haskell
{-# OPTIONS_GHC -Wall #-}
module LogAnalysis where

import Log

-- Exercise 1

parseMessage :: String -> LogMessage
parseMessage msg
      |msg!!0 == 'I' = LogMessage Info (read ((words msg)!!1)::Int)  (unwords(drop 2 (words msg)))
      |msg!!0 == 'W' = LogMessage Warning (read ((words msg)!!1)::Int)  (unwords(drop 2(words msg)))
      |msg!!0 == 'E' = LogMessage (Error (read ((words msg)!!1)::Int)) (read ((words msg)!!2)::Int)  (unwords(drop 3 (words msg)))
      |otherwise = Unknown msg



parse :: String -> [LogMessage]
parse msg
     |msg == "" = []
     |otherwise = [parseMessage ((lines msg)!!0)] ++ parse(unlines(tail(lines msg)))

-- Exercise 2

insert :: LogMessage -> MessageTree -> MessageTree
insert (Unknown _) t = t
insert (LogMessage a b c) (Node x (LogMessage w y v) z) = if b < y then Node (insert (LogMessage a b c) x) (LogMessage w y v) z
                                                              else Node x (LogMessage w y v) (insert (LogMessage a b c) z)
insert (LogMessage a b c) Leaf = Node Leaf (LogMessage a b c) Leaf
insert (LogMessage a b c) _ = Node Leaf (LogMessage a b c) Leaf

-- Exercise 3

build :: [LogMessage] -> MessageTree
build [] = Leaf
build (x:y) = insert x (build y)

-- Exercise 4

inOrder :: MessageTree -> [LogMessage]
inOrder Leaf = []
inOrder (Node x y z) = inOrder x ++ [y] ++ inOrder z



-- Exercise 5
select :: [LogMessage] -> [LogMessage]
select [] = []
select ((LogMessage (Error x) y z) : w) = if x > 50 then [(LogMessage (Error x) y z)] ++ (select w) else (select w)
select (_:y) = select y

getMsg::[LogMessage] -> [String]
getMsg [] = []
getMsg ((LogMessage _ _ z):w) = [z] ++ (getMsg w)
getMsg _ = []

whatWentWrong :: [LogMessage] -> [String]
whatWentWrong msg = (getMsg (inOrder(build(select msg))))


```
## [hw3](https://www.seas.upenn.edu/~cis194/spring13/hw/03-rec-poly.pdf)
```haskell
-- Exercise 1 Hopscotch

sk::Int->Int -> [a] -> [a]
sk n x ls
    | n + x > length(ls) = [ls !! (x-1)]
    | otherwise = [ls !! (x-1)]  ++ (sk n (x+n) ls)

skip::Int->[a] -> [[a]]
skip n ls
     | n == length(ls) = [(sk n n ls)]
     | otherwise = [(sk n n ls)] ++ (skip (n+1) ls)

skips :: [a] -> [[a]]
skips [] = []
skips ls = (skip 1 ls)

-- Exercise 2 Local maxima
getMax :: Integer -> [Integer] -> [Integer]
getMax _ [] = []
getMax _ [x] = []
getMax a (x:y:z) =  if (x > a  &&  x > y) then [x] ++ (getMax x (y:z)) else (getMax x (y:z))

localMaxima :: [Integer] -> [Integer]
localMaxima [] = []
localMaxima ls = getMax (ls !! 0) ls

-- Exercise 3 Histogram
count :: Integer -> [Integer] -> [Integer]
count 10 _ = []
count n ls = [(toInteger(length(filter ( == n) ls)))] ++ (count (n+1) ls)

line :: [Integer] -> String
line [] = "\n"
line (x:y) = if x > 0 then "*" ++ line(y) else " " ++ line(y)

sub :: Integer -> Integer
sub x = x - 1

toString::[Integer] -> String
toString ls
     |(length(filter (> 0) ls)) == 0 = ""
     |otherwise = toString(map sub ls) ++ line(ls)


histogram :: [Integer] -> String
histogram ls = (toString(count 0 ls) ++ "0123456789\n")
```

## [hw4](https://www.seas.upenn.edu/~cis194/spring13/hw/04-higher-order.pdf)
```haskell
-- Exercise 1: Wholemeal programming
fun1 :: [Integer] -> Integer
fun1 [] = 1
fun1 (x:xs)
    |even x = (x - 2) * fun1 xs
    |otherwise = fun1 xs

fun1' :: [Integer]->Integer
fun1' = product.map (\x-> x-2).filter even

fun2 :: Integer -> Integer
fun2 1 = 0
fun2 n | even n = n + fun2 (n `div` 2)
       | otherwise = fun2 (3 * n + 1)

fun2' :: Integer -> Integer
fun2'  = sum.filter even.takeWhile (>1).iterate(\x -> if even x then (x `div` 2) else (3*x + 1))

-- Exercise 2:Folding with trees
data Tree a = Leaf
            | Node Integer (Tree a) a (Tree a)
  deriving (Show, Eq)

foldTree :: [a] -> Tree a
foldTree = foldr insertNode Leaf

insertNode :: a -> Tree a -> Tree a
insertNode x Leaf = Node 0 Leaf x Leaf
insertNode x (Node h ln y rn)
  | treeHeight ln < treeHeight rn =
    let nn = insertNode x ln
    in Node (treeHeight nn + 1) nn y rn
  | otherwise =
    let nn = insertNode x rn
    in Node (treeHeight nn + 1) ln y nn

treeHeight :: Tree a -> Integer
treeHeight Leaf = -1
treeHeight (Node h _ _ _) = h


-- Exercise 3: More folds!
xor :: [Bool] -> Bool
xor = foldr (\x y -> if ((x == True && y == False) || (x == False && y == True)) then True else False) False

map' :: (a -> b) -> [a] -> [b]
map' f = foldr (\x y -> [f(x)] ++ y) []

myFoldl :: (a -> b -> a) -> a -> [b] -> a
myFoldl f base xs = foldr (flip f) base (reverse xs)

-- Exercise 4:Finding primes
cartProd :: [a] -> [b] -> [(a, b)]
cartProd xs ys = [(x,y) | x <- xs, y <- ys]

sieveSundaram :: Integer -> [Integer]
sieveSundaram n = map (\x -> x*2 + 1) (filter (\x -> notElem x (map (\(i,j) -> 2*i*j + i + j) (filter (\(i,j)->2*i*j+i+j <= n) (cartProd [1..n] [1..n]))))  [1..n])

```

## [hw5](https://www.seas.upenn.edu/~cis194/spring13/hw/05-type-classes.pdf)
```haskell
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE TypeSynonymInstances #-}
import ExprT
import Parser
import StackVM
import Data.Maybe
import qualified Data.Map as M
-- Exercise 1

eval :: ExprT->Integer
eval (ExprT.Lit x) = x
eval (ExprT.Add x y) = eval x + eval y
eval (ExprT.Mul x y) = eval x * eval y

-- Exercise 2
evalStr :: String -> Maybe Integer
evalStr str
    |(parseExp ExprT.Lit ExprT.Add ExprT.Mul str == Nothing) = Nothing
    |otherwise = Just(eval (fromJust(parseExp ExprT.Lit ExprT.Add ExprT.Mul str)))

-- Exercise 3
class Expr a where
   lit :: Integer -> a
   add :: a -> a -> a
   mul :: a -> a -> a

instance Expr ExprT where
   lit = ExprT.Lit
   add = ExprT.Add
   mul = ExprT.Mul

reify :: ExprT -> ExprT
reify = id

-- Exercise 4
instance Expr Integer where
    lit  a =  a
    add a b = a + b
    mul a b = a*b

instance Expr Bool where
     lit a = (if a > 0 then True else False)
     add a b = a || b
     mul a b = a && b

newtype MinMax = MinMax Integer deriving (Eq, Show)

instance Expr MinMax where
      lit x = MinMax x
      add (MinMax a) (MinMax b) = MinMax(max a b)
      mul (MinMax a) (MinMax b) = MinMax(min a b)

newtype Mod7 = Mod7 Integer deriving (Eq, Show)

instance Expr Mod7 where
     lit  x = Mod7(x `mod` 7)
     add (Mod7 a) (Mod7 b) = Mod7((a + b) `mod` 7)
     mul (Mod7 a) (Mod7 b) = Mod7((a*b) `mod` 7)

testExp :: Expr a => Maybe a
testExp = parseExp lit add mul "(3 * -4) + 5"
testInteger = testExp :: Maybe Integer
testBool = testExp :: Maybe Bool
testMM = testExp :: Maybe MinMax
testSat = testExp :: Maybe Mod7


-- exercise 5

instance Expr Program where
    lit x = [PushI x]
    add a b = a ++ b ++ [StackVM.Add]
    mul a b = a ++ b ++ [StackVM.Mul]

compile:: String -> Maybe Program
compile str = parseExp lit add mul str :: Maybe Program

-- exercise 6

class HasVars a where
        var :: String -> a

data VarExprT = Lit Integer
                | Var String
                | Add VarExprT VarExprT
                | Mul VarExprT VarExprT

instance HasVars (M.Map String Integer -> Maybe Integer) where
        var = M.lookup

instance Expr (M.Map String Integer -> Maybe Integer) where
        lit int0 _ = Just int0
        add var0 var1 map0 = do int0 <- var0 map0
                                int1 <- var1 map0
                                return (int0 + int1)
        mul var0 var1 map0 = do int0 <- var0 map0
                                int1 <- var1 map0
                                return (int0 * int1)

withVars :: [(String, Integer)]
            -> (M.Map String Integer -> Maybe Integer)
            -> Maybe Integer
withVars vs ex = ex $ M.fromList vs

main :: IO ()
main = do
          print $ withVars [("x", 6)] $ add (lit 3) (var "x")
          print $ withVars [("x", 6)] $ add (lit 3) (var "y")
          print $ withVars  [("x", 6), ("y", 3)] $ mul (var "x") (add (var "y") (var "x"))


```

