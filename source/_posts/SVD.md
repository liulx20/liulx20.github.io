---
title: SVD
date: 2020-08-06 22:42:45
tags: 数学
mathjax: true
---
## 一些结论

---
$rank(A) = rank(A^{T}A)$

只需说明$AX = 0$ 与 $A^{T}AX =0$同解.

若$X$满足$AX = 0$,显然有$A^{T}AX = 0$成立.

反之，若$A^{T}AX = 0$,左乘$X^{T}$,有$X^{T}A^{T}AX = 0$. 

即$(AX)^{T}AX = 0$,令$Y=AX$,有$Y^{T}Y = 0$,$Y = AX = 0$.
<!-- More -->

---

实矩阵$A_{m\times n}$, $A^{T}A$的特征值都为非负实数。

设$\lambda$ 为$A^{T}A$的复特征值，有$AX=\lambda X$

记$\overline{\lambda}$为$\lambda$的共轭，有

$A\overline{X} = \overline{A}\overline{X} = \overline{AX} = \overline{\lambda X} = \overline{\lambda} \overline{X} $.

从而

$\overline{X}^{T}AX = \overline{X}^{T} \lambda X = \lambda \overline{X}^{T} X$.

和

$\overline{X}^{T}AX = \overline{X}^{T}\overline{A}^{T}X = \overline{AX}^{T}X = (\overline{\lambda} \overline{X})^{T}X = \overline{\lambda} \overline{X}^{T}X $.

进而有$(\lambda - \overline{\lambda})\overline{X}^{T}X = 0$,

所以$\lambda - \overline{\lambda} = 0$，即$\lambda$为实数.


设$\lambda$为$A^{T}A$的特征值，有

$\left \| AX \right \|^{2} = X^{T}A^{T}AX = \lambda X^{T}X = \lambda \left \\| X\right \\|^{2}$.

所以$\lambda = \frac{\left \\| AX\right \\|^{2}}{\left \\| X\right \\|^{2}} \geq 0$.

---

$A \in \mathbb{R}^{m\times n}$ 则$A$存在奇异值分解：

$A = U\Sigma V^{T}$,其中$U$是$m$阶正交矩阵,$V$是$n$阶正交矩阵,$\Sigma$是$m\times n$矩形对角矩阵,其对角线元素非负,且按降序排列.

证明: $A^{T}A$的特征值都为实数，因而存在有正交矩阵$V$，使得$V^{T}(A^{T}A)V = \Lambda$ 成立.

其中$\Lambda$为对角矩阵，对角线元素为$A^{T}A$的特征值,调整特征值的顺序，使其按降序排列，满足$\lambda_{1} \geq \lambda_{2} \geq \lambda_{3}\cdots \geq \lambda_{n} \geq 0$.

令 $V_{1} = \begin{bmatrix} \nu _{1} & \nu_{2}  & \cdots  & \nu_{r} \end{bmatrix}$,$V_{2} = \begin{bmatrix} \nu _{r+1}  & \cdots  & \nu_{n} \end{bmatrix}$

其中$\nu_{1} \cdots \nu_{r}$为$A^{T}A$正特征值对应的特征向量，$\nu_{r+1} \cdots \nu_{n}$为$A^{T}A$零特征值的对应的特征向量.

$V = \begin{bmatrix} V_{1} & V_{2} \end{bmatrix}$即为奇异值分解中的$V$.

记$\sigma_{i} = \sqrt\lambda_{i}$,令

$\Sigma _{1} = \begin{bmatrix} \sigma_{1} &  &  & 
\\\ &\sigma_{2}  &  & 
\\\  &  &\ddots   & 
\\\  &  &  & \sigma_{r} \end{bmatrix}$

于是$m\times n$对角矩阵可以表示为$\Sigma = \begin{bmatrix}\Sigma_{1} & 0 
\\\ 0 & 0 \end{bmatrix}$.

构造$U$,令$u_{j} = \frac{1}{\sigma_{j}}A\nu_{j}$,


$U_{1} = \begin{bmatrix} u_{1} & u_{2} & \cdots & u_{r} \end{bmatrix}$,有$AV_{1} = U_{1}\Sigma_{1}$

$u_{i}^{T}u_{j} = (\frac{1}{\sigma_{i}}\nu_{i}^{T}A^{T})(\frac{1}{\sigma_{j}}A\nu_{j}) = \frac{1}{\sigma_{i}\sigma_{j}}\nu_{i}^{T}(A^{T}A\nu_{j}) = \frac{\sigma_{j}}{\sigma_{i}}\nu_{i}\nu_{j}$
所以$u_{1},u_{2},\cdots,u_{r}$构成一组标准正交基.

令$U_{2} = u_{r+1},\cdots,u_{n}$为$R(A)^{\perp }$的一组标准正交基,记$U = \begin{bmatrix} U_{1} & U_{2} \end{bmatrix}$

$U\Sigma V^{T} = \begin{bmatrix}U_{1} & U_{2} \end{bmatrix}\begin{bmatrix}\Sigma_{1} & 0\\\ 0 & 0 \end{bmatrix}\begin{bmatrix}V_{1}^{T}\\\ 
                 V_{2}^{T}\end{bmatrix}=U_{1}\Sigma_{1}V_{1}^{T} = AV_{1}V_{1}^{T} = A$.
                                                              