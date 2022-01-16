---
title: pytorch备忘
date: 2021-07-22 14:34:58
tags:
---

### Tensor操作

创建：

```python
torch.zeros(2,3)#全零
torch.ones(2,3)#全一
torch.Tensor([[1,2,3],[4,5,6]])# from list
npy = np.random.rand(2,3)
torch.from_numpy(npy)#from numpy
torch.arange(6)#tensor([0, 1, 2, 3, 4, 5])
```

运算：

```python
import torch
a = torch.Tensor([1,2,3])
b = torch.Tensor([2,3,4])
a + b
#tensor([3., 5., 7.])
a * b
#tensor([ 2.,  6., 12.])
a / b
# tensor([0.5000, 0.6667, 0.7500])
a + 1
#tensor([2., 3., 4.])
torch.dot(a,b)
#tensor(20.)
a.outer(b)
"""
tensor([[ 2.,  3.,  4.],
        [ 4.,  6.,  8.],
        [ 6.,  9., 12.]])
"""
torch.mm#矩阵乘法
```

维度操作：

```python
x = torch.arange(6)#tensor([0, 1, 2, 3, 4, 5])
#view 维度不匹配会RE
x = x.view(2,3)#tensor([[0, 1, 2],[3, 4, 5]])
torch.sum(x,dim = 0)# tensor([3, 5, 7])
torch.transpose(x,0,1)
"""
tensor([[0, 3],
        [1, 4],
        [2, 5]])
"""
```

索引：

```python
indices = torch.LongTensor([0,2])
torch.index_select(x,dim=1,index = indices)
"""
tensor([[0, 2],
        [3, 5]])
"""
row_indices = torch.arange(2).long()
col_indices = torch.LongTensor([0,1])
x[row_indices,col_indices]#((0,0),(1,1))
# tensor([0, 4])
```



连接：

```python
x = torch.arange(6).view(2,3)
torch.cat([x,x],dim = 0)
"""
tensor([[0, 1, 2],
        [3, 4, 5],
        [0, 1, 2],
        [3, 4, 5]])
"""
torch.stack([x,x])
"""
tensor([[[0, 1, 2],
         [3, 4, 5]],

        [[0, 1, 2],
         [3, 4, 5]]])
"""
```



随机数：

```python
torch.rand(2,3)#uniform random
torch.randn(2,3)#random normal
```

requires_grad

```python
x = torch.ones(2,2,requires_grad = True)
x.grad is None#True
y = (x + 2)*(x + 5) + 3
x.grad is None#True
z = y.mean()
z.backward()
x.grad is None#False
```

创建cuda张量

```
torch.cuda.is_avaliable()
device = torch.device("cuda" if torch.cuda.is_avaliable() else "cpu")
x = torch.rand(3,3).to(device)
```



```python
#1. 创建一个张量,在第0维插入一个维度
x = torch.rand(3,3)
x = x.unsqueeze(0)
x.shape
#torch.Size([1, 3, 3])

#2. 去掉该维度
x = x.squeeze(0)
x.shape
# torch.Size([3, 3])
#squeeze对size大于1的维度应用无效

#3. 在区间[3,7]创建一个形状为5x3的随机张量
x = 3 + torch.rand(5,3)*(7-3)

#4. 创建一个具有正态分布(mean = 0, std = 1)的张量
x = torch.rand(3,3)
x.normal_()

#5. 找到 torch.Tensor([1,1,1,0,1])中所有非零元素索引
x = torch.Tensor([1,1,1,0,1])
torch.nonzero(x)
"""
tensor([[0],
        [1],
        [2],
        [4]])
"""

#6. 创建一个大小为（3,1)的随机向量，水平扩展4个副本
x = torch.rand(3,1)
x.expand(3,4)
"""
tensor([[0.0839, 0.0839, 0.0839, 0.0839],
        [0.1283, 0.1283, 0.1283, 0.1283],
        [0.9937, 0.9937, 0.9937, 0.9937]])
"""

#7 返回两个三维矩阵的乘积
a = torch.rand(3,4,5)
b = torch.rand(3,5,4)
torch.bmm(a,b).shape
torch.Size([3, 4, 4])

#8 返回一个三维矩阵和一个二维矩阵的乘积
a = torch.rand(3,4,5)
b = torch.rand(5,4)
torch.bmm(a,b.unsqueeze(0).expand(a.size(0), *b.size()))

```

