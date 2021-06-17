import numpy as np

def rbf_kernel_distance(x, y, gamma=0.1) -> float:
    """ RBF 距离

    Args:
        x ([type]): [description]
        y ([type]): [description]
        gamma (int, optional): [description]. Defaults to 1.

    Returns:
        float: [description]
    """
    euclid_dis = np.sum((x-y)**2)
    d = 2 * gamma ** 2
    return 1 / np.exp(euclid_dis / d)


def euclid_distance(x, y):
    """计算欧几里得距离

    Args:
        x ([type]): [description]
        y ([type]): [description]

    Returns:
        [type]: [description]
    """
    return np.sum((x-y)**2)


def cal_distance_matrix(X):
    """生成距离矩阵

    Args:
        X (numpy.ndarray): 一组样本点

    Returns:
        numpy.ndarray: 样本点构成的距离矩阵
    """
    X = np.array(X)
    S = np.zeros((len(X), len(X)))
    for i in range(len(X)):
        for j in range(i+1, len(X)):
            S[i][j] = 1.0 * euclid_distance(X[i], X[j])
            # S[i][j] = 1.0 * rbf_kernel_distance(X[i], X[j])
            S[j][i] = S[i][j]
    return S


def cal_laplacian_matrix(adjacentMatrix):

    # compute the Degree Matrix: D=sum(A)
    degreeMatrix = np.sum(adjacentMatrix, axis=1)

    # compute the Laplacian Matrix: L=D-A
    laplacianMatrix = np.diag(degreeMatrix) - adjacentMatrix

    # normailze
    # D^(-1/2) L D^(-1/2)
    sqrtDegreeMatrix = np.diag(1.0 / (degreeMatrix ** (0.5)))
    return np.dot(np.dot(sqrtDegreeMatrix, laplacianMatrix), sqrtDegreeMatrix)
