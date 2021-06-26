# 计算智能课程练习

## 目录

* [需求](#需求)
* [快速运行](#快速运行)
* [Fuzzy c-means Clustering](#fuzzy-c-means-clustering)
  + [问题分析](#问题分析)
  + [算法表述](#算法表述)
  + [源代码](#源代码)
  + [运行结果](#运行结果)
* [Spectral Clustering](#spectral-clustering)
  + [问题分析](#问题分析-1)
  + [算法表述](#算法表述-1)
  + [源代码](#源代码-1)
  + [运行结果](#运行结果-1)
* [参考资料](#参考资料)
* [附录](#附录)



## 需求

数据：文件 `iris.txt` 中包含了 `iris` 数据，其中每行的前四个数据代表一个样本，最后一个数据表示该样本的类别。

1. 用C-means的方法对iris数据作聚类，要求聚成 3类。要求给出下列数据：

    + 初始类中心点
    + 迭代次数
    + 聚类结果（每类包含的样本，类中心）
    + 错误率
2. 用谱聚类方法对 `iris` 数据作聚类
3. 递交实验报告，源代码



## 快速运行

运行 Fuzzy c-means

```bash
$ cd .\cmeans\
$ python .\cmeans.py
```

运行 Spectral

```bash
$ cd .\spectral\
$ pip install -r .\requirements.txt
$ python .\spectral.py
```



## Fuzzy c-means Clustering

### 问题分析

令：

+ <img valign="middle" src="https://render.githubusercontent.com/render/math?math=X+=+\{x_{1},x_{2},x_{3},...,x_{n}\}"> 表示 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=n" style=""> 个样本

+ <img valign="middle" src="https://render.githubusercontent.com/render/math?math=C+=+\{c_{1},c_{2},...,c_{k}\}"> 表示 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=k"> 个类别

+ 对于样本<img valign="middle" src="https://render.githubusercontent.com/render/math?math=p"> 来说，其属于类别 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=j"> 的概率为 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=u_{pj}">，则可以构建一个概率矩阵，称之为**隶属度矩阵** U

    <p align="center">
        <img valign="middle" src="https://render.githubusercontent.com/render/math?math=U=\begin{pmatrix}u_{11}%26%20...%20%26%20u_{1k}\\%20...%20%26%20%26%20...\\u_{n1}%26%20...%20%26%20u_{nk}\end{pmatrix}" height=60>
    </p>

    对于其中的任意一个样本 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=p">，它对于所有类别的隶属度（概率）之和为 1 ，即 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=\sum_{j=1}^{k}u_{pj}=1"> 

+ 定义样本点 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=x_{j}"> 到类中心 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=c_{i}"> 的距离为： <img valign="middle" src="https://render.githubusercontent.com/render/math?math=d_{ij}^2%20=%20%7C%7C%20x_j%20-%20c_i%20%7C%7C^2%20">   


则所有点 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=X"> 到所有类 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=C"> 的距离之和为：<img valign="middle" src="https://render.githubusercontent.com/render/math?math=J(U,C_{k})%20=\sum_{i=1}^k\sum_{j=1}^n%20u_{ij}^m%20d_{ij}^2%20">，其中 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=m"> 代表模糊系数

我们认为一个好的聚类应该意味着**总距离尽可能的小**

于是问题变为：在约束条件 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=\sum_{j=1}^{k}u_{pj}=1"> 下，求 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=min(J(U,C_{k}))">。这个优化问题通常使用交互式策略求解，即给定 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=U"> 关于 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=C_{k}"> 求最小，再给定 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=C_{k}"> 关于 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=U"> 求最小。

使用拉格朗日乘数法计算得到：

当 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=C_{k}"> 一定时，点 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=p"> 对样本 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=q"> 的隶属度：

<p align="center">
  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=u_{pq}=\frac{1}{\sum_{i=1}^k%20(\frac{||x_{p}-c_{q}||}{||x_{p}-c_{i}||})^{\frac{2}{m-1}}}" height="70">
</p>



当 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=U"> 一定时，聚类中心点 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=i"> 为：

<p align="center">
  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=c_i%20=\frac{\sum_{j=1}^n%20u_{ji}^m%20%20x_j%20}{\sum_{j=1}^{n}u_{ji}^m}" height="70">
</p>

### 算法表述

伪码如下：

```
设置模糊参数 m、误差阈值 precise、随机初始化聚类中心点 C[]

loop:
    计算最优隶属度矩阵 U[][]
    根据隶属度矩阵计算新的聚类中心点 C'[]
    if C[] 和 C'[] 的距离 < 误差阈值 precise:
        将 C 更新为 C‘
        break
    将 C 更新为 C‘

用 C 对样本进行分类
```

### 源代码

见 `cmeans.py`

### 运行结果

以下输出包含：初始类中心点、迭代次数、聚类结果（每类包含的样本，类中心）、正确率

计算得错误率 = 1 - 正确率 = 0.106667

```
(ml) PS D:\Projects\cluster> python .\cmeans.py
初始类中心点
[5.199999999999999, 3.6, 1.5, 0.30000000000000004] 0.0
[7.1, 3.3000000000000003, 4.8, 1.5] 1.0
[6.3999999999999995, 3.4, 6.1, 2.6] 2.0
在第15次迭代时收敛
聚类后的类中心
[5.003966319284148, 3.4140814490387914, 1.4828276178642037, 0.2535517357359567] 0.0
[5.889081869565415, 2.7611232276170203, 4.364170157821359, 1.3974276857268302] 1.0
[6.77519207409717, 3.052434885440432, 5.647007100459471, 2.0536335619897863] 2.0
聚类准确率为0.893333
聚类的结果如下
属于第0.0类的样本有
[5.1, 3.5, 1.4, 0.2] 0.0
[4.9, 3.0, 1.4, 0.2] 0.0
[4.7, 3.2, 1.3, 0.2] 0.0
[4.6, 3.1, 1.5, 0.2] 0.0
[5.0, 3.6, 1.4, 0.2] 0.0
[5.4, 3.9, 1.7, 0.4] 0.0
[4.6, 3.4, 1.4, 0.3] 0.0
[5.0, 3.4, 1.5, 0.2] 0.0
[4.4, 2.9, 1.4, 0.2] 0.0
[4.9, 3.1, 1.5, 0.1] 0.0
[5.4, 3.7, 1.5, 0.2] 0.0
[4.8, 3.4, 1.6, 0.2] 0.0
[4.8, 3.0, 1.4, 0.1] 0.0
[4.3, 3.0, 1.1, 0.1] 0.0
[5.8, 4.0, 1.2, 0.2] 0.0
[5.7, 4.4, 1.5, 0.4] 0.0
[5.4, 3.9, 1.3, 0.4] 0.0
[5.1, 3.5, 1.4, 0.3] 0.0
[5.7, 3.8, 1.7, 0.3] 0.0
[5.1, 3.8, 1.5, 0.3] 0.0
[5.4, 3.4, 1.7, 0.2] 0.0
[5.1, 3.7, 1.5, 0.4] 0.0
[4.6, 3.6, 1.0, 0.2] 0.0
[5.1, 3.3, 1.7, 0.5] 0.0
[4.8, 3.4, 1.9, 0.2] 0.0
[5.0, 3.0, 1.6, 0.2] 0.0
[5.0, 3.4, 1.6, 0.4] 0.0
[5.2, 3.5, 1.5, 0.2] 0.0
[5.2, 3.4, 1.4, 0.2] 0.0
[4.7, 3.2, 1.6, 0.2] 0.0
[4.8, 3.1, 1.6, 0.2] 0.0
[5.4, 3.4, 1.5, 0.4] 0.0
[5.2, 4.1, 1.5, 0.1] 0.0
[5.5, 4.2, 1.4, 0.2] 0.0
[4.9, 3.1, 1.5, 0.2] 0.0
[5.0, 3.2, 1.2, 0.2] 0.0
[5.5, 3.5, 1.3, 0.2] 0.0
[4.9, 3.6, 1.4, 0.1] 0.0
[4.4, 3.0, 1.3, 0.2] 0.0
[5.1, 3.4, 1.5, 0.2] 0.0
[5.0, 3.5, 1.3, 0.3] 0.0
[4.5, 2.3, 1.3, 0.3] 0.0
[4.4, 3.2, 1.3, 0.2] 0.0
[5.0, 3.5, 1.6, 0.6] 0.0
[5.1, 3.8, 1.9, 0.4] 0.0
[4.8, 3.0, 1.4, 0.3] 0.0
[5.1, 3.8, 1.6, 0.2] 0.0
[4.6, 3.2, 1.4, 0.2] 0.0
[5.3, 3.7, 1.5, 0.2] 0.0
[5.0, 3.3, 1.4, 0.2] 0.0
属于第1.0类的样本有
[6.4, 3.2, 4.5, 1.5] 1.0
[5.5, 2.3, 4.0, 1.3] 1.0
[6.5, 2.8, 4.6, 1.5] 1.0
[5.7, 2.8, 4.5, 1.3] 1.0
[6.3, 3.3, 4.7, 1.6] 1.0
[4.9, 2.4, 3.3, 1.0] 1.0
[6.6, 2.9, 4.6, 1.3] 1.0
[5.2, 2.7, 3.9, 1.4] 1.0
[5.0, 2.0, 3.5, 1.0] 1.0
[5.9, 3.0, 4.2, 1.5] 1.0
[6.0, 2.2, 4.0, 1.0] 1.0
[6.1, 2.9, 4.7, 1.4] 1.0
[5.6, 2.9, 3.6, 1.3] 1.0
[6.7, 3.1, 4.4, 1.4] 1.0
[5.6, 3.0, 4.5, 1.5] 1.0
[5.8, 2.7, 4.1, 1.0] 1.0
[6.2, 2.2, 4.5, 1.5] 1.0
[5.6, 2.5, 3.9, 1.1] 1.0
[5.9, 3.2, 4.8, 1.8] 1.0
[6.1, 2.8, 4.0, 1.3] 1.0
[6.3, 2.5, 4.9, 1.5] 1.0
[6.1, 2.8, 4.7, 1.2] 1.0
[6.4, 2.9, 4.3, 1.3] 1.0
[6.6, 3.0, 4.4, 1.4] 1.0
[6.8, 2.8, 4.8, 1.4] 1.0
[6.0, 2.9, 4.5, 1.5] 1.0
[5.7, 2.6, 3.5, 1.0] 1.0
[5.5, 2.4, 3.8, 1.1] 1.0
[5.5, 2.4, 3.7, 1.0] 1.0
[5.8, 2.7, 3.9, 1.2] 1.0
[6.0, 2.7, 5.1, 1.6] 1.0
[5.4, 3.0, 4.5, 1.5] 1.0
[6.0, 3.4, 4.5, 1.6] 1.0
[6.7, 3.1, 4.7, 1.5] 1.0
[6.3, 2.3, 4.4, 1.3] 1.0
[5.6, 3.0, 4.1, 1.3] 1.0
[5.5, 2.5, 4.0, 1.3] 1.0
[5.5, 2.6, 4.4, 1.2] 1.0
[6.1, 3.0, 4.6, 1.4] 1.0
[5.8, 2.6, 4.0, 1.2] 1.0
[5.0, 2.3, 3.3, 1.0] 1.0
[5.6, 2.7, 4.2, 1.3] 1.0
[5.7, 3.0, 4.2, 1.2] 1.0
[5.7, 2.9, 4.2, 1.3] 1.0
[6.2, 2.9, 4.3, 1.3] 1.0
[5.1, 2.5, 3.0, 1.1] 1.0
[5.7, 2.8, 4.1, 1.3] 1.0
[5.8, 2.7, 5.1, 1.9] 2.0
[4.9, 2.5, 4.5, 1.7] 2.0
[5.7, 2.5, 5.0, 2.0] 2.0
[6.0, 2.2, 5.0, 1.5] 2.0
[5.6, 2.8, 4.9, 2.0] 2.0
[6.3, 2.7, 4.9, 1.8] 2.0
[6.2, 2.8, 4.8, 1.8] 2.0
[6.1, 3.0, 4.9, 1.8] 2.0
[6.3, 2.8, 5.1, 1.5] 2.0
[6.0, 3.0, 4.8, 1.8] 2.0
[5.8, 2.7, 5.1, 1.9] 2.0
[6.3, 2.5, 5.0, 1.9] 2.0
[5.9, 3.0, 5.1, 1.8] 2.0
属于第2.0类的样本有
[7.0, 3.2, 4.7, 1.4] 1.0
[6.9, 3.1, 4.9, 1.5] 1.0
[6.7, 3.0, 5.0, 1.7] 1.0
[6.3, 3.3, 6.0, 2.5] 2.0
[7.1, 3.0, 5.9, 2.1] 2.0
[6.3, 2.9, 5.6, 1.8] 2.0
[6.5, 3.0, 5.8, 2.2] 2.0
[7.6, 3.0, 6.6, 2.1] 2.0
[7.3, 2.9, 6.3, 1.8] 2.0
[6.7, 2.5, 5.8, 1.8] 2.0
[7.2, 3.6, 6.1, 2.5] 2.0
[6.5, 3.2, 5.1, 2.0] 2.0
[6.4, 2.7, 5.3, 1.9] 2.0
[6.8, 3.0, 5.5, 2.1] 2.0
[5.8, 2.8, 5.1, 2.4] 2.0
[6.4, 3.2, 5.3, 2.3] 2.0
[6.5, 3.0, 5.5, 1.8] 2.0
[7.7, 3.8, 6.7, 2.2] 2.0
[7.7, 2.6, 6.9, 2.3] 2.0
[6.9, 3.2, 5.7, 2.3] 2.0
[7.7, 2.8, 6.7, 2.0] 2.0
[6.7, 3.3, 5.7, 2.1] 2.0
[7.2, 3.2, 6.0, 1.8] 2.0
[6.4, 2.8, 5.6, 2.1] 2.0
[7.2, 3.0, 5.8, 1.6] 2.0
[7.4, 2.8, 6.1, 1.9] 2.0
[7.9, 3.8, 6.4, 2.0] 2.0
[6.4, 2.8, 5.6, 2.2] 2.0
[6.1, 2.6, 5.6, 1.4] 2.0
[7.7, 3.0, 6.1, 2.3] 2.0
[6.3, 3.4, 5.6, 2.4] 2.0
[6.4, 3.1, 5.5, 1.8] 2.0
[6.9, 3.1, 5.4, 2.1] 2.0
[6.7, 3.1, 5.6, 2.4] 2.0
[6.9, 3.1, 5.1, 2.3] 2.0
[6.8, 3.2, 5.9, 2.3] 2.0
[6.7, 3.3, 5.7, 2.5] 2.0
[6.7, 3.0, 5.2, 2.3] 2.0
[6.5, 3.0, 5.2, 2.0] 2.0
[6.2, 3.4, 5.4, 2.3] 2.0
```

## Spectral Clustering

### 问题分析

**定义问题：**

+ <img valign="middle" src="https://render.githubusercontent.com/render/math?math=V+=+\{v_{1},v_{2},v_{3},...,v_{n}\}"> 表示 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=n"> 个样本

+ 每两个样本之间或多或少都有联系，如果样本 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=i"> 和样本 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=j"> 之间的联系用 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=w_{ij}"> 来衡量（ <img valign="middle" src="https://render.githubusercontent.com/render/math?math=i,j{\in}[1,n]">），则所有的联系可以构成一个 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=n{\times}n"> 的矩阵：
  
    <p align="center">
      <img valign="middle" src="https://render.githubusercontent.com/render/math?math=W=\begin{pmatrix}w_{11}%26\ldots%20%26%20w_{1n}\\\ldots%20%26%20%26{\ldots}\\w_{n1}%26{\ldots}%26%20w_{nn}\end{pmatrix}" height=70>
    </p>
    
    使用基于高斯径向核RBF的全连接法计算样本之间的联系，即：
    
    <p align="center">
      <img valign="middle" src="https://render.githubusercontent.com/render/math?math=w_{ij}=exp(-\frac{||x_i-x_j||_2^2}{2\sigma^2})" height=50 style="margin: 20px auto">
    </p>
    

**分析问题：**

将样本视为一组点，点与点之间的联系视为带权值的边，则可以构造出一个图 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=G(V,E)"> 其中 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=W{\Leftrightarrow}E">，**聚类的过程就转化为对图的一种划分**（切图），将样本聚为 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=k"> 类等价于将图 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=G"> 切成 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=k"> 个子图：<img valign="middle" src="https://render.githubusercontent.com/render/math?math=cut(G)=(A_{1},A_{2},...,A_{k})" height=20> 

一个好的聚类意味着子图之间的联系尽可能少，子图内部的点聚合度尽可能高

**再定义：**

+ 将两个不相交的子图 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=A"  height=14> 和 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=B"  height=14> 之间的联系定义为所有连接两个子图的边权重之和，即：

    <p align="center">
      <img valign="middle" src="https://render.githubusercontent.com/render/math?math=W(A,B)=\displaystyle\sum_{i{\in}A,j{\in}B}w_{ij}" height=40 style="margin: 20px auto">
    </p>

+ 将点 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=v_i"> 的度记为 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=d_i"> ，定义为与 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=v_i"> 相连的所有边的权重之和，即：

    <p align="center">
        <img valign="middle" src="https://render.githubusercontent.com/render/math?math=d_i=\displaystyle\sum_{j=1}^{n}w_{ij}" height=60 style="margin: 20px auto">
    </p>
    进一步得到一个 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=n\times%20n"> 对角矩阵 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=D">，只有主对角线有值，第 i 行第 i 个元素的值对应着 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=v_i"> 的度 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=d_i"> ，即：

    <p align="center">
      <img valign="middle" src="https://render.githubusercontent.com/render/math?math=D=\begin{pmatrix}d_1%260%26\ldots%20%260\\0%26d_2%20%26\ldots%20%260\\\vdots%20%26\vdots%20%26\ddots%20%26\vdots\\0%260%26\ldots%20%26%20d_n\end{pmatrix}" height="100">
    </p>

+ 将一个子图 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=A"  height=14> 内部的聚合度定义为其中所有点的度数之和，即：

    <p align="center">
      <img valign="middle" src="https://render.githubusercontent.com/render/math?math=vol(A)=\displaystyle\sum_{i{\in}A}d_i" height=40 style="margin: 20px auto">
    </p>
    

+ 对于一个子图 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=A"  height=14> ，可以定义一个指标 α = A 与外界的联系度 ÷ A 内部的聚合度，即：

<p align="center">
  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=\alpha=\frac{W(A,\overline{A})}{Vol(A)}" height=40 style="margin: 20px auto">
</p>

+ 对于一种切分<img valign="middle" src="https://render.githubusercontent.com/render/math?math=cut(G)=(A_{1},A_{2},...,A_{k})" height=20> ，我们定义该切分的聚类程度为每个字图的 α 之和，即：

    <p align="center">
      <img valign="middle" src="https://render.githubusercontent.com/render/math?math=NCut(A_1,A_2,...A_k)=\displaystyle\sum_{i=1}^{k}\frac{W(A_i,\overline{A}_i)}{Vol(A_i)}" height=50 style="margin: 10px auto">
    </p>

**再分析问题：**

聚类的过程就需要优化（最小化）上述的：<img valign="middle" src="https://render.githubusercontent.com/render/math?math=NCut(A_1,A_2,...A_k)" height=18> 。

**再定义：**

+ 对于切图中的某个子图<img valign="middle" src="https://render.githubusercontent.com/render/math?math=A_i" height=18> ，我们对它定义一个 n 维（n为样本数）的指示（列）向量 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=h_i" height=18> ，如果点 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=v_j" height=18> 属于子图 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=A_i" height=18> ，则指示向量 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=h_i" height=18> 的第 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=j" height=18> 个元素 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=h_{ij}" height=18> 等于  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=\frac{1}{\sqrt{vol(A_i)}}" height=50 valign="middle"> ，即：
  
    <p align="center">
      <img valign="middle" src="https://render.githubusercontent.com/render/math?math=h_{ij}=\begin{cases}0%26{v_j\notin%20A_i}\\\frac{1}{\sqrt{vol(A_i)}}%26%20{%20v_j\in%20A_i}\end{cases}" height=90 style="margin: 20px auto">
    </p>
    
    记：<img valign="middle" src="https://render.githubusercontent.com/render/math?math=L=D-W" height=16> ，<img valign="middle" src="https://render.githubusercontent.com/render/math?math=L" height=16> 是拉普拉斯矩阵，会发现：
    
    <p align="center">
      <img valign="middle" src="https://render.githubusercontent.com/render/math?math=h_i^TLh_i=\frac{cut(A_i,\overline{A}_i)}{|A_i|}" height=50 style="margin: 20px auto">
    </p>
    
    > 怎么发现的见[附录](#附录)

**再分析问题：**

所以要最小化的目标：


<p align="center">
  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=NCut(A_1,A_2,...A_k)=\displaystyle\sum_{i=1}^{k}h_i^TLh_i=\sum_{i=1}^{k}(H^TLH)_{ii}=tr(H^TLH)" height=60> 
</p>

其中：<img valign="middle" src="https://render.githubusercontent.com/render/math?math=H=(h_1,h_2,...,h_k)" height=20>，一个 n 行、k 列的矩阵

问题变成求解：

<p align="center">
  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=\underbrace{arg\%3Bmin}_H\%3Btr(H^TLH)\%3B\%3Bs.t.\%3BH^TDH=I" height=40  style="margin: 10px auto">
</p>

令 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=H=D^{-1/2}F" height=16> ，则问题变成：

<p align="center">
  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=\underbrace{arg\%3Bmin}_F\%3Btr(F^TD^{-1/2}LD^{-1/2}F)\%3B\%3Bs.t.\%3BF^TF=I" height=40  style="margin: 20px auto">
</p>

再令 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=L'=D^{-1/2}LD^{-1/2}" height=16> ，则问题变为：

<p align="center">
  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=\underbrace{arg\%3Bmin}_H\%3Btr(H^TL'H)\%3B\%3Bs.t.\%3BF^TF=I" height=40  style="margin: 20px auto">
</p>

我们要求出 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=L^{'}"> 最小的前 k 个特征值。一般来说，k 远小于 n，也就是说将从 n 维降到了 k 维。另外，<img valign="middle" src="https://render.githubusercontent.com/render/math?math=L^{'}"> 相当于对 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=L"> 做了标准化：

<p align="center">
  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=L'=\frac{L_{ij}}{\sqrt{d_i*d_j}}" height=54  style="margin: 20px auto">
</p>

接着求出对应的 k 个特征向量，可以得到一个 n×k 的矩阵，即为我们的 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=H"> 。

然后对 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=H"> 按行做标准化，即：

<p align="center">
  <img valign="middle" src="https://render.githubusercontent.com/render/math?math=h_{ij}^*=\frac{h_{ij}}{(\sum_{t=1}^kh_{it}^{2})^{1/2}}" height=54  style="margin: 20px auto">
</p>

由于我们在使用维度规约的时候损失了少量信息，导致得到的优化后的指示向量 h 对应的 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=H"> 现在不能完全指示各样本的归属，因此一般在得到 n×k 的矩阵 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=H"> 后还需要对每一行进行一次传统的聚类，比如使用 K-Means 。

### 算法表述

1. 构建邻接矩阵 W，度矩阵 D，计算出拉普拉斯矩阵 L
2. 构建标准化后的拉普拉斯矩阵 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=L'=D^{-1/2}LD^{-1/2}" height=14>
3. 计算 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=L^{'}" height=12> 最小的 k 个特征值所各自对应的特征向量 f
4. 将各自对应的特征向量 f 组成的矩阵按行标准化，最终组成 n×k 维的特征矩阵 F
5. 把 F 中的每一行作为一个 k 维的样本，共 n 个样本，用传统聚类方法进行聚类，聚类维数为 K
6. 得到簇划分<img valign="middle" src="https://render.githubusercontent.com/render/math?math=C(c_1,c_2,...c_K)" height=18>。

### 源代码

见 `spectral.py`

### 运行结果

```
标准化后的拉普拉斯矩阵：
 [[ 0.94760147  0.          0.         ...  0.          0.
   0.        ]
 [ 0.          0.9124808  -0.07256349 ...  0.          0.
   0.        ]
 [ 0.         -0.07256349  0.93417065 ...  0.          0.
   0.        ]
 ...
 [ 0.          0.          0.         ...  0.9315538  -0.07011117
   0.        ]
 [ 0.          0.          0.         ... -0.07011117  0.89498362
   0.        ]
 [ 0.          0.          0.         ...  0.          0.
   0.91567561]]
前 3 个最小的特征值：
 [(-5.551115123125783e-17, 0), (1.214306433183765e-16, 50), (0.019842972248943297, 51)]
前 %d 个最小的特征值对应的特征向量：
 [[-0.16906564  0.10816728 -0.15672531 -0.13092652 -0.0490668   0.08781605
   0.06457376 -0.04246249  0.11012205  0.00328772  0.36972239  0.0194687
   0.1895311  -0.10465268 -0.1244069   0.02046343 -0.04346536  0.02242108
   0.1164522  -0.03286019  0.03175442  0.09528833 -0.0135314   0.10715087
  -0.03400193 -0.16064558 -0.00453491  0.04555546 -0.02760322 -0.26332282
  -0.28866898 -0.18933231 -0.00156389 -0.13418623 -0.09859749  0.15621798
  -0.3753152  -0.30066783 -0.15279305  0.048503   -0.01907583 -0.00132372
  -0.05783982  0.14763368  0.27460392 -0.1000876   0.09770901  0.0441368
  -0.03487257 -0.00889804  0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.        ]
 [-0.13081671 -0.15612145  0.01066228  0.26777019 -0.02883947  0.18248695
   0.24215817 -0.05770441 -0.0157502   0.10591291  0.07574946 -0.08797724
  -0.17008025 -0.04200753  0.08909346 -0.07950693  0.08998358 -0.04573212
   0.24510485 -0.00094442  0.08759288  0.12942972  0.23513007 -0.02795797
  -0.28698108  0.14814041  0.08243547  0.06133251 -0.5027385   0.06759108
   0.04861763 -0.01020471 -0.04203467  0.04115469 -0.12280525  0.07634075
  -0.05732899  0.03683833  0.11128786  0.15137554  0.21586559 -0.18696691
   0.0834821  -0.04903204  0.05434949  0.03377982  0.01855217 -0.15843772
   0.06962382  0.07529264  0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.        ]
 [-0.15083604 -0.20011291  0.07194666 -0.07769783 -0.00252465  0.11929617
   0.01122155  0.31393715 -0.0306828  -0.09223113 -0.05934368  0.17460319
   0.13831238  0.16024527 -0.2324454   0.01138916 -0.0092682   0.05096698
  -0.09431016 -0.18375396 -0.08024428 -0.16203505 -0.14031008 -0.094478
   0.27479935  0.09022724  0.00139943 -0.13361664  0.02284891  0.03650127
  -0.09096278 -0.03098912 -0.16999457 -0.07214325 -0.21963327  0.28970899
   0.04043035  0.02244718  0.33441921  0.07838977  0.07737128 -0.12162577
   0.00459616  0.00859246  0.12234634  0.1075786   0.08370802 -0.28698959
   0.11609811  0.12139216  0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.
   0.          0.          0.          0.          0.          0.        ]]
特征矩阵：
 [[-1.69065640e-01  0.00000000e+00  0.00000000e+00]
 [-1.30816712e-01  0.00000000e+00  0.00000000e+00]
 [-1.50836039e-01  0.00000000e+00  0.00000000e+00]
 [-1.50378236e-01  0.00000000e+00  0.00000000e+00]
 [-1.51228227e-01  0.00000000e+00  0.00000000e+00]
 [-1.33322622e-01  0.00000000e+00  0.00000000e+00]
 [-1.39693150e-01  0.00000000e+00  0.00000000e+00]
 [-1.65027995e-01  0.00000000e+00  0.00000000e+00]
 [-1.29046567e-01  0.00000000e+00  0.00000000e+00]
 [-1.37074119e-01  0.00000000e+00  0.00000000e+00]
 [-1.48774520e-01  0.00000000e+00  0.00000000e+00]
 [-1.25906123e-01  0.00000000e+00  0.00000000e+00]
 [-1.54484980e-01  0.00000000e+00  0.00000000e+00]
 [-1.25643645e-01  0.00000000e+00  0.00000000e+00]
 [-1.18248578e-01  0.00000000e+00  0.00000000e+00]
 [-1.15384152e-01  0.00000000e+00  0.00000000e+00]
 [-1.33302748e-01  0.00000000e+00  0.00000000e+00]
 [-1.61326453e-01  0.00000000e+00  0.00000000e+00]
 [-1.26011215e-01  0.00000000e+00  0.00000000e+00]
 [-1.61687718e-01  0.00000000e+00  0.00000000e+00]
 [-1.29377262e-01  0.00000000e+00  0.00000000e+00]
 [-1.50827010e-01  0.00000000e+00  0.00000000e+00]
 [-1.19658848e-01  0.00000000e+00  0.00000000e+00]
 [-1.34295154e-01  0.00000000e+00  0.00000000e+00]
 [-1.22481374e-01  0.00000000e+00  0.00000000e+00]
 [-1.34599284e-01  0.00000000e+00  0.00000000e+00]
 [-1.41537997e-01  0.00000000e+00  0.00000000e+00]
 [-1.69394298e-01  0.00000000e+00  0.00000000e+00]
 [-1.42510202e-01  0.00000000e+00  0.00000000e+00]
 [-1.55000157e-01  0.00000000e+00  0.00000000e+00]
 [-1.45393286e-01  0.00000000e+00  0.00000000e+00]
 [-1.30026853e-01  0.00000000e+00  0.00000000e+00]
 [-1.31819480e-01  0.00000000e+00  0.00000000e+00]
 [-1.21709499e-01  0.00000000e+00  0.00000000e+00]
 [-1.47321098e-01  0.00000000e+00  0.00000000e+00]
 [-1.30124763e-01  0.00000000e+00  0.00000000e+00]
 [-1.33948687e-01  0.00000000e+00  0.00000000e+00]
 [-1.45569976e-01  0.00000000e+00  0.00000000e+00]
 [-1.29424777e-01  0.00000000e+00  0.00000000e+00]
 [-1.64906163e-01  0.00000000e+00  0.00000000e+00]
 [-1.55920394e-01  0.00000000e+00  0.00000000e+00]
 [-1.10867882e-01  0.00000000e+00  0.00000000e+00]
 [-1.33794414e-01  0.00000000e+00  0.00000000e+00]
 [-1.29276702e-01  0.00000000e+00  0.00000000e+00]
 [-1.22043520e-01  0.00000000e+00  0.00000000e+00]
 [-1.54380873e-01  0.00000000e+00  0.00000000e+00]
 [-1.48352457e-01  0.00000000e+00  0.00000000e+00]
 [-1.41439492e-01  0.00000000e+00  0.00000000e+00]
 [-1.70547921e-01  0.00000000e+00  0.00000000e+00]
 [-1.56000486e-01  0.00000000e+00  0.00000000e+00]
 [ 0.00000000e+00 -8.92192209e-02 -1.92146575e-02]
 [ 0.00000000e+00 -9.87751752e-02 -3.32238252e-02]
 [ 0.00000000e+00 -8.98822021e-02 -1.88482911e-02]
 [ 0.00000000e+00 -1.08636196e-01 -1.39353670e-01]
 [ 0.00000000e+00 -1.21356911e-01 -3.14896392e-02]
 [ 0.00000000e+00 -1.02276687e-01 -9.92187557e-02]
 [ 0.00000000e+00 -9.74148319e-02 -2.98008180e-02]
 [ 0.00000000e+00 -8.41257105e-02 -1.13786482e-01]
 [ 0.00000000e+00 -1.02503769e-01 -3.35826306e-02]
 [ 0.00000000e+00 -1.03547763e-01 -1.33059710e-01]
 [ 0.00000000e+00 -8.36850546e-02 -1.12933864e-01]
 [ 0.00000000e+00 -9.91931169e-02 -8.97633730e-02]
 [ 0.00000000e+00 -9.13884600e-02 -1.02798241e-01]
 [ 0.00000000e+00 -1.09531289e-01 -3.72869732e-02]
 [ 0.00000000e+00 -9.49252193e-02 -1.24153519e-01]
 [ 0.00000000e+00 -9.13953628e-02 -2.77165392e-02]
 [ 0.00000000e+00 -9.79267337e-02 -1.00030935e-01]
 [ 0.00000000e+00 -1.09400226e-01 -1.35420948e-01]
 [ 0.00000000e+00 -8.65317644e-02 -2.68373983e-02]
 [ 0.00000000e+00 -1.13389671e-01 -1.47899067e-01]
 [ 0.00000000e+00 -9.06753630e-02 -2.45553614e-02]
 [ 0.00000000e+00 -9.80333812e-02 -9.85729183e-02]
 [ 0.00000000e+00 -1.01265110e-01 -1.21522341e-02]
 [ 0.00000000e+00 -9.77047823e-02 -3.86561984e-02]
 [ 0.00000000e+00 -9.89651340e-02 -4.36701167e-02]
 [ 0.00000000e+00 -9.91787038e-02 -3.11218223e-02]
 [ 0.00000000e+00 -9.06770895e-02 -1.48128678e-02]
 [ 0.00000000e+00 -9.77258602e-02  3.10741569e-02]
 [ 0.00000000e+00 -1.12435895e-01 -6.34250448e-02]
 [ 0.00000000e+00 -1.01127893e-01 -1.33788318e-01]
 [ 0.00000000e+00 -1.10394108e-01 -1.44859638e-01]
 [ 0.00000000e+00 -1.06796520e-01 -1.40796536e-01]
 [ 0.00000000e+00 -1.13626239e-01 -1.42083076e-01]
 [ 0.00000000e+00 -1.09027305e-01  1.62647191e-03]
 [ 0.00000000e+00 -9.32088957e-02 -9.96336868e-02]
 [ 0.00000000e+00 -8.95884770e-02 -4.01821652e-02]
 [ 0.00000000e+00 -9.23342021e-02 -1.99987915e-02]
 [ 0.00000000e+00 -8.74512807e-02 -4.02727759e-02]
 [ 0.00000000e+00 -1.06510529e-01 -1.24146744e-01]
 [ 0.00000000e+00 -1.15726377e-01 -1.48502003e-01]
 [ 0.00000000e+00 -9.78728313e-02 -1.15119945e-01]
 [ 0.00000000e+00 -1.06483859e-01 -4.34847803e-02]
 [ 0.00000000e+00 -1.16839225e-01 -1.45760610e-01]
 [ 0.00000000e+00 -8.52412114e-02 -1.15114665e-01]
 [ 0.00000000e+00 -1.16533062e-01 -1.40814531e-01]
 [ 0.00000000e+00 -1.03482996e-01 -1.18634535e-01]
 [ 0.00000000e+00 -1.10876203e-01 -1.24318892e-01]
 [ 0.00000000e+00 -1.02593902e-01 -4.92833732e-02]
 [ 0.00000000e+00 -8.18492595e-02 -1.10748617e-01]
 [ 0.00000000e+00 -1.23008999e-01 -1.47351333e-01]
 [ 0.00000000e+00 -8.73561344e-02  1.12770677e-01]
 [ 0.00000000e+00 -1.01643809e-01 -3.21351509e-03]
 [ 0.00000000e+00 -1.10283292e-01  1.56484641e-01]
 [ 0.00000000e+00 -9.44354052e-02  8.93926467e-02]
 [ 0.00000000e+00 -1.08665976e-01  1.33759250e-01]
 [ 0.00000000e+00 -8.50754907e-02  1.29074666e-01]
 [ 0.00000000e+00 -8.02898456e-02 -8.00422326e-02]
 [ 0.00000000e+00 -9.42388620e-02  1.38394854e-01]
 [ 0.00000000e+00 -9.59280996e-02  1.09543830e-01]
 [ 0.00000000e+00 -8.75384023e-02  1.26548001e-01]
 [ 0.00000000e+00 -9.43812996e-02  9.17979941e-02]
 [ 0.00000000e+00 -1.01791400e-01  6.71373928e-02]
 [ 0.00000000e+00 -1.26722161e-01  1.55036660e-01]
 [ 0.00000000e+00 -9.20514411e-02 -1.20067524e-02]
 [ 0.00000000e+00 -8.63893541e-02  1.65098833e-03]
 [ 0.00000000e+00 -1.04413599e-01  1.16838478e-01]
 [ 0.00000000e+00 -1.08273555e-01  1.12162476e-01]
 [ 0.00000000e+00 -7.55464034e-02  1.14805114e-01]
 [ 0.00000000e+00 -7.51263282e-02  1.14297061e-01]
 [ 0.00000000e+00 -9.07018166e-02 -4.48529533e-03]
 [ 0.00000000e+00 -1.15100002e-01  1.55955897e-01]
 [ 0.00000000e+00 -9.29656757e-02 -1.46751586e-02]
 [ 0.00000000e+00 -8.20473518e-02  1.24247957e-01]
 [ 0.00000000e+00 -1.12083036e-01  5.53634615e-03]
 [ 0.00000000e+00 -1.13580072e-01  1.48203571e-01]
 [ 0.00000000e+00 -1.03284019e-01  1.49467021e-01]
 [ 0.00000000e+00 -1.17826459e-01 -1.59569885e-02]
 [ 0.00000000e+00 -1.12349953e-01 -6.68139214e-03]
 [ 0.00000000e+00 -9.88185729e-02  1.09185424e-01]
 [ 0.00000000e+00 -9.37081811e-02  1.29615129e-01]
 [ 0.00000000e+00 -9.42849887e-02  1.38224215e-01]
 [ 0.00000000e+00 -7.79712203e-02  1.17903343e-01]
 [ 0.00000000e+00 -1.04768340e-01  1.18555027e-01]
 [ 0.00000000e+00 -1.08035340e-01  7.97688438e-03]
 [ 0.00000000e+00 -8.56510025e-02  4.15288215e-02]
 [ 0.00000000e+00 -8.98049446e-02  1.34513766e-01]
 [ 0.00000000e+00 -8.96486755e-02  1.15405692e-01]
 [ 0.00000000e+00 -1.04556189e-01  1.11153949e-01]
 [ 0.00000000e+00 -1.12412376e-01 -2.10137921e-02]
 [ 0.00000000e+00 -1.04743674e-01  1.32540338e-01]
 [ 0.00000000e+00 -1.14993132e-01  1.47510353e-01]
 [ 0.00000000e+00 -8.92347669e-02  1.00812772e-01]
 [ 0.00000000e+00 -9.86084377e-02 -6.36170881e-03]
 [ 0.00000000e+00 -1.03685594e-01  1.41706088e-01]
 [ 0.00000000e+00 -9.77899770e-02  1.28179689e-01]
 [ 0.00000000e+00 -9.10048460e-02  1.07508989e-01]
 [ 0.00000000e+00 -1.00406027e-01 -4.37014531e-05]
 [ 0.00000000e+00 -1.09487385e-01  1.07395741e-01]
 [ 0.00000000e+00 -8.83914491e-02  1.07021833e-01]
 [ 0.00000000e+00 -9.86420695e-02 -7.58702211e-03]]
得到的簇划分：
[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 2 2 2 2 1 2 2 2 2
 2 2 1 1 2 2 2 2 1 2 1 2 1 2 2 1 1 2 2 2 2 2 1 2 2 2 2 1 2 2 2 1 2 2 2 1 2
 2 1]
```

> 聚类准确率为：0.9

## 参考资料

1. https://blog.csdn.net/changyuanchn/article/details/80427893
2. https://en.wikipedia.org/wiki/Fuzzy_clustering
3. https://zhuanlan.zhihu.com/p/85244505
4. https://www.bilibili.com/video/BV1kt411X7Zh
5. https://www.cnblogs.com/pinard/p/6221564.html

## 附录

拉普拉斯矩阵 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=L=D-W" height=14> 具有以下性质：

1. 拉普拉斯矩阵是对称矩阵，这可以由DD和WW都是对称矩阵而得

2. 由于拉普拉斯矩阵是对称矩阵，则它的所有的特征值都是实数

3. 对于任意的向量 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=f" height=16>我们有：<img valign="middle" src="https://render.githubusercontent.com/render/math?math=f^TLf=\frac{1}{2}\sum_{i,j=1}^{n}w_{ij}(f_i-f_j)^2" height=36>

    证明如下：

<img valign="middle" src="https://render.githubusercontent.com/render/math?math=\begin{equation}\begin{aligned}f^TLf={}%26f^TDf%20-%20f^TWf\\={}%26\sum_{i=1}^{n}d_if_i^2%20-\sum_{i%2Cj=1}^{n}w_{ij}f_if_j\\={}%26\frac{1}{2}(\sum_{i=1}^{n}d_if_i^2-2\sum_{i%2Cj=1}^{n}w_{ij}f_if_j%2B\sum_{j=1}^{n}d_jf_j^2)\\%20={}%26\frac{1}{2}\sum_{i%2Cj=1}^{n}w_{ij}(f_i-f_j)^2\end{aligned}\end{equation}" height="180">

4. 拉普拉斯矩阵是半正定的，且对应的 n 个实数特征值都 ≥ 0，即 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=0=\lambda_1\leq\lambda_2\leq...\leq\lambda_n">。且最小的特征值为 0，这个由性质 3 很容易得出。

基于以上性质，我们的指示向量 <img valign="middle" src="https://render.githubusercontent.com/render/math?math=h_i" height=18> 利用拉普拉斯矩阵的性质三可以得出：

<img valign="middle" src="https://render.githubusercontent.com/render/math?math=\begin{equation}\begin{aligned}h_i^TLh_i%20%26%20=\frac{1}{2}\sum_{m=1}\sum_{n=1}w_{mn}(h_{im}-h_{in})^2\\%26%20=\frac{1}{2}(\sum_{m\in%20A_i%2C%20n\notin%20A_i}w_{mn}(\frac{1}{\sqrt{%7CA_i%7C}}-%200)^2%20%2B\sum_{m\notin%20A_i%2C%20n\in%20A_i}w_{mn}(0%20-\frac{1}{\sqrt{%7CA_i%7C}})^2\\%26%20=\frac{1}{2}(\sum_{m\in%20A_i%2C%20n\notin%20A_i}w_{mn}\frac{1}{%7CA_i%7C}%2B\sum_{m\notin%20A_i%2C%20n\in%20A_i}w_{mn}\frac{1}{%7CA_i%7C}\\%26%20=\frac{1}{2}(cut(A_i%2C\overline{A}_i)\frac{1}{%7CA_i%7C}%2B%20cut(\overline{A}_i%2C%20A_i)\frac{1}{%7CA_i%7C})\\%26%20=\frac{cut(A_i%2C\overline{A}_i)}{%7CA_i%7C}\end{aligned}\end{equation}" height="260">
