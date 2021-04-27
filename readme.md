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

## 实践

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

    <img src="https://render.githubusercontent.com/render/math?math=U%3D%5Cbegin%7Bpmatrix%7Du_%7B11%7D%20%26%20...%20%26%20u_%7B1k%7D%20%5C%5C%20...%20%26%20%26%20...%20%5C%5Cu_%7Bn1%7D%20%26%20...%20%26%20u_%7Bnk%7D%20%5Cend%7Bpmatrix%7D" height=60> 

    对于其中的任意一个样本 <img src="https://render.githubusercontent.com/render/math?math=p">，它对于所有类别的隶属度（概率）之和为 1 ，即 <img src="https://render.githubusercontent.com/render/math?math=%5Csum_%7Bj%3D1%7D%5E%7Bk%7D%20u_%7Bpj%7D=1"> 

+ 定义样本点 <img src="https://render.githubusercontent.com/render/math?math=x_{j}"> 到类中心 <img src="https://render.githubusercontent.com/render/math?math=c_{i}"> 的距离为： <img src="https://render.githubusercontent.com/render/math?math=d_%7Bij%7D%5E2%20%3D%20%7C%7C%20x_j%20-%20c_i%20%7C%7C%5E2%20">   


则所有点 <img src="https://render.githubusercontent.com/render/math?math=X"> 到所有类 <img src="https://render.githubusercontent.com/render/math?math=C"> 的距离之和为：<img src="https://render.githubusercontent.com/render/math?math=J(U,C_{k})%20%3D%20%5Csum_%7Bi%3D1%7D%5Ek%20%5Csum_%7Bj%3D1%7D%5En%20u_%7Bij%7D%5Em%20d_%7Bij%7D%5E2%20">，其中 <img src="https://render.githubusercontent.com/render/math?math=m"> 代表模糊系数

我们认为一个好的聚类应该意味着**总距离尽可能的小**

于是问题变为：在约束条件 <img src="https://render.githubusercontent.com/render/math?math=%5Csum_%7Bj%3D1%7D%5E%7Bk%7D%20u_%7Bpj%7D=1"> 下，求 <img src="https://render.githubusercontent.com/render/math?math=min(J(U,C_{k}))">。这个优化问题通常使用交互式策略求解，即给定 <img src="https://render.githubusercontent.com/render/math?math=U"> 关于 <img src="https://render.githubusercontent.com/render/math?math=C_{k}"> 求最小，再给定 <img src="https://render.githubusercontent.com/render/math?math=C_{k}"> 关于 <img src="https://render.githubusercontent.com/render/math?math=U"> 求最小。

使用拉格朗日乘数法计算得到：

当 <img src="https://render.githubusercontent.com/render/math?math=C_{k}"> 一定时，点 <img src="https://render.githubusercontent.com/render/math?math=p"> 对样本 <img src="https://render.githubusercontent.com/render/math?math=q"> 的隶属度  <img src="https://render.githubusercontent.com/render/math?math=u_%7Bpq%7D%20%3D%20%20%5Cfrac%7B1%7D%7B%20%5Csum_%7Bi%3D1%7D%5Ek%20(%5Cfrac%7B||x_{p}-c_{q}||%7D%7B||x_{p}-c_{i}||%7D)%5E%7B%5Cfrac%7B2%7D%7Bm-1%7D%7D%20%7D" height="70"> 

当 <img src="https://render.githubusercontent.com/render/math?math=U"> 一定时，聚类中心点 <img src="https://render.githubusercontent.com/render/math?math=i"> 为，<img src="https://render.githubusercontent.com/render/math?math=c_i%20%3D%20%5Cfrac%7B%20\sum_{j=1}^n%20u_%7Bij%7D%5Em%20%20x_j%20%7D%7B%5Csum_%7Bj%3D1%7D%5E%7Bn%7D%20u_%7Bij%7D%5Em%7D" height="70">

#### 算法

伪码如下：

```
设置模糊参数 m、误差阈值 alpha、随机初始化聚类中心点 C[]

loop:
    计算最优隶属度矩阵 U[][]
    根据隶属度矩阵计算新的聚类中心点 C'[]
    if C[] 和 C'[] 的距离 < 误差阈值 precise:
        将 C 更新为 C‘
        break
    将 C 更新为 C‘

用 C 对样本进行分类
```

#### 代码实现

见 `cmeans.py`

#### 实验结果

