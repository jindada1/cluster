from loader import read_data


def generate_points(sample, tags):
    """参照传入的参考样本点，为传入的每一种类型生成一个点
    Args:
        sample: 参考样本点
        tags: 样本点的所有类型
    Returns:
        list: 一组样本点
    """
    return []


def count_membership_matrix(samples, fuzzy, centers):
    """根据聚类中心点计算隶属度矩阵

    Args:
        samples (list): 样本
        fuzzy (float): 模糊度
        centers (list): 聚类中心点

    Returns:
        list: 隶属度矩阵
    """
    return []


def count_cluster_center(samples, fuzzy, membership):
    """根据隶属度矩阵更新聚类中心点

    Args:
        samples (list): 样本
        fuzzy (float): 模糊度
        membership (list): 隶属度矩阵

    Returns:
        list: 一组聚类中心点
    """
    return []


def distance_between(points1, points2):
    """计算两组样本点之间的欧氏距离

    Args:
        points1 (list): 第一组样本点
        points2 (list): 第二组样本点

    Returns:
        float: 两组样本点的欧氏距离
    """
    return 0


def cluster(X, tags, fuzzy=2, precise=0.00001):
    """模糊聚类过程

    Args:
        X (list): 待聚类的样本点
        tags (list): 类别
        fuzzy (int, optional): 模糊度. Defaults to 2.
        precise (float, optional): 精度. Defaults to 0.00001.

    Returns:
        list: 一组聚类中心点
    """
    # 根据样本生成指定数量的聚类中心点
    C = generate_points(X[0], tags)
    # 设置隶属度矩阵
    U = []
    # 开始迭代
    iter_num = 0
    while iter_num:
        iter_num += 1
        # 根据 C 计算最优隶属度矩阵 U
        U = count_membership_matrix(X, fuzzy, C)
        # 根据隶属度矩阵 U 计算新的聚类中心点 C1
        C1 = count_cluster_center(X, fuzzy, U)
        # 收敛
        if distance_between(C, C1) < precise:
            C = C1
            break
        # 更新聚类中心
        C = C1
    # 返回新的聚类中心点
    return C


def main():
    """ 先聚类再分类
    """
    filename = "./iris.txt"
    # 读取数据
    data, tags = read_data(filename)
    if len(data) < 1:
        raise Exception("数据读取异常")

    # 开始聚类
    cluster(data, tags)


if __name__ == "__main__":
    main()
