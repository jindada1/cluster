# 计算智能课程练习

## 需求

数据：文件 `iris.txt` 中包含了 `iris` 数据，其中每行的前四个数据代表一个样本，最后一个数据表示该样本的类别。

1. 用C-means的方法对iris数据作聚类，要求聚成 3类。要求给出下列数据：

    + 初始类中心点
    + 迭代次数
    + 聚类结果（每类包含的样本，类中心）
    + 错误率
2. 用谱聚类方法对 `iris` 数据作聚类
3. 递交实验报告，源代码

## 实现

### Fuzzy c-means clustering

**参考**

> https://blog.csdn.net/changyuanchn/article/details/80427893
>
> https://en.wikipedia.org/wiki/Fuzzy_clustering
>
> https://zhuanlan.zhihu.com/p/85244505

#### 问题分析

令：

+ <img src="https://render.githubusercontent.com/render/math?math=X+=+\{x_{1},x_{2},x_{3},...,x_{n}\}"> 表示 <img src="https://render.githubusercontent.com/render/math?math=n"> 个样本

+ <img src="https://render.githubusercontent.com/render/math?math=C+=+\{c_{1},c_{2},...,c_{k}\}"> 表示 <img src="https://render.githubusercontent.com/render/math?math=k"> 个类别

+ 对于样本<img src="https://render.githubusercontent.com/render/math?math=p"> 来说，其属于类别 <img src="https://render.githubusercontent.com/render/math?math=j"> 的概率为 <img src="https://render.githubusercontent.com/render/math?math=u_{pj}">，则可以构建一个概率矩阵，称之为**隶属度矩阵** U

    <img src="https://render.githubusercontent.com/render/math?math=U%3D\begin{pmatrix}u_{11}%20%26%20...%20%26%20u_{1k}%20\\%20...%20%26%20%26%20...%20\\u_{n1}%20%26%20...%20%26%20u_{nk}%20\end{pmatrix}" height=60> 

    对于其中的任意一个样本 <img src="https://render.githubusercontent.com/render/math?math=p">，它对于所有类别的隶属度（概率）之和为 1 ，即 <img src="https://render.githubusercontent.com/render/math?math=\sum_{j%3D1}%5E{k}%20u_{pj}=1"> 

+ 定义样本点 <img src="https://render.githubusercontent.com/render/math?math=x_{j}"> 到类中心 <img src="https://render.githubusercontent.com/render/math?math=c_{i}"> 的距离为： <img src="https://render.githubusercontent.com/render/math?math=d_{ij}%5E2%20%3D%20%7C%7C%20x_j%20-%20c_i%20%7C%7C%5E2%20">   


则所有点 <img src="https://render.githubusercontent.com/render/math?math=X"> 到所有类 <img src="https://render.githubusercontent.com/render/math?math=C"> 的距离之和为：<img src="https://render.githubusercontent.com/render/math?math=J(U,C_{k})%20%3D%20\sum_{i%3D1}%5Ek%20\sum_{j%3D1}%5En%20u_{ij}%5Em%20d_{ij}%5E2%20">，其中 <img src="https://render.githubusercontent.com/render/math?math=m"> 代表模糊系数

我们认为一个好的聚类应该意味着**总距离尽可能的小**

于是问题变为：在约束条件 <img src="https://render.githubusercontent.com/render/math?math=\sum_{j%3D1}%5E{k}%20u_{pj}=1"> 下，求 <img src="https://render.githubusercontent.com/render/math?math=min(J(U,C_{k}))">。这个优化问题通常使用交互式策略求解，即给定 <img src="https://render.githubusercontent.com/render/math?math=U"> 关于 <img src="https://render.githubusercontent.com/render/math?math=C_{k}"> 求最小，再给定 <img src="https://render.githubusercontent.com/render/math?math=C_{k}"> 关于 <img src="https://render.githubusercontent.com/render/math?math=U"> 求最小。

使用拉格朗日乘数法计算得到：

当 <img src="https://render.githubusercontent.com/render/math?math=C_{k}"> 一定时，点 <img src="https://render.githubusercontent.com/render/math?math=p"> 对样本 <img src="https://render.githubusercontent.com/render/math?math=q"> 的隶属度  <img src="https://render.githubusercontent.com/render/math?math=u_{pq}%20%3D%20%20\frac{1}{%20\sum_{i%3D1}%5Ek%20(\frac{||x_{p}-c_{q}||}{||x_{p}-c_{i}||})%5E{\frac{2}{m-1}}%20}" height="70"> 

当 <img src="https://render.githubusercontent.com/render/math?math=U"> 一定时，聚类中心点 <img src="https://render.githubusercontent.com/render/math?math=i"> 为，<img src="https://render.githubusercontent.com/render/math?math=c_i%20%3D%20\frac{%20\sum_{j=1}^n%20u_{ji}%5Em%20%20x_j%20}{\sum_{j%3D1}%5E{n}%20u_{ji}%5Em}" height="70">

#### 算法表述

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

#### 源代码

见 `cmeans.py`

#### 运行结果

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

### spectral clustering

**参考**

> https://www.bilibili.com/video/BV1kt411X7Zh
>
> https://www.cnblogs.com/pinard/p/6221564.html

#### 问题分析

+ <img src="https://render.githubusercontent.com/render/math?math=V+=+\{v_{1},v_{2},v_{3},...,v_{n}\}"> 表示 <img src="https://render.githubusercontent.com/render/math?math=n"> 个样本
+ 每两个样本之间或多或少都有联系，如果样本 <img src="https://render.githubusercontent.com/render/math?math=i"> 和样本 <img src="https://render.githubusercontent.com/render/math?math=j"> 之间的联系用 <img src="https://render.githubusercontent.com/render/math?math=w_{ij}"> 来衡量（ <img src="https://render.githubusercontent.com/render/math?math=i,j{\in}[1,n]">），则所有的联系可以构成一个 <img src="https://render.githubusercontent.com/render/math?math=n{\times}n"> 的矩阵 <img src="https://render.githubusercontent.com/render/math?math=W=\begin{pmatrix}w_{11}%20%26%20...%20%26%20w_{1n}%20\\%20...%20%26%20%26%20...%20\\w_{n1}%20%26%20...%20%26%20w_{nn}%20\end{pmatrix}" height=60>
+ 将样本视为一组点，点与点之间的联系视为带权值的边，则可以构造出一个图 <img src="https://render.githubusercontent.com/render/math?math=G(V,E)"> 其中 <img src="https://render.githubusercontent.com/render/math?math=W{\Leftrightarrow}E">，**聚类的过程就转化为对图的一种划分**（切图），将样本聚为 <img src="https://render.githubusercontent.com/render/math?math=k"> 类等价于将图 <img src="https://render.githubusercontent.com/render/math?math=G"> 切成 <img src="https://render.githubusercontent.com/render/math?math=k"> 个子图：<img src="https://render.githubusercontent.com/render/math?math=cut(G)=(A_{1},A_{2},...,A_{k})"> 
+ 一个好的聚类意味着子图之间的联系尽可能少，子图内部的点聚合度尽可能高（这些子图**高内聚低耦合**）
+ 

#### 算法表述

#### 源代码

#### 运行结果