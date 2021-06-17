from loader import read_data
from myutils import cal_distance_matrix, cal_laplacian_matrix
from knn import myKNN
import numpy as np
from sklearn.cluster import KMeans


# 读取数据
data, label = read_data("./iris.txt")

# 1. 根据相似度矩阵 S，构建邻接矩阵 W
S = cal_distance_matrix(data)
W = myKNN(S, k=10)

# 2. 计算度矩阵 D，拉普拉斯矩阵 L，并将其标准化得到 Laplacian
Laplacian = cal_laplacian_matrix(W)

# 3. 计算 Laplacian 的特征值 x 和对应的特征向量 fs
x, fs = np.linalg.eig(Laplacian)
x = zip(x, range(len(x)))
x = sorted(x, key=lambda x:x[0])

# 4. 将最小的 k 个特征值对应的特征向量 f 组成的矩阵按行标准化，最终组成 n×k 维的特征矩阵 F
k = 3
F = np.vstack([fs[:,i] for (v, i) in x[:k]]).T

# 5. 把 F 中的每一行作为一个 k 维的样本，共 n 个样本，用传统聚类方法进行聚类，聚类维数为 K'
sp_kmeans = KMeans(n_clusters=3).fit(F)

# 6. 得到簇划分 (C1, C2, ..., CK')。
C = sp_kmeans.labels_

print("标准化后的拉普拉斯矩阵：\n", Laplacian)
print("前 %d 个最小的特征值：\n"%k, x[:k])
print("前 %d 个最小的特征值对应的特征向量：\n", fs[:k])
print("特征矩阵：\n", F)
print("得到的簇划分：\n%s"%str(C))
