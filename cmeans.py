from loader import read_data


def generate_points(sample, tags):
    """参照传入的参考样本点，为传入的每一种类型生成一个点
    Args:
        sample: 参考样本点
        tags: 样本点的所有类型
    Returns:
        points: 一组样本点
    Raise:
        
    """
    pass

def cluster(X, tags):
    """聚类过程
    Args:
        X: 待聚类的样本点
    Returns:
        一组聚类中心点
    """
    # 根据样本生成指定数量的聚类中心点
    C = generate_points(X[0], tags)
    # 设置隶属度矩阵
    U = []
    # 设置模糊度
    m = 2
    # 开始迭代
    iter_num = 0
    while iter_num:
        iter_num += 1
        # 根据 C 计算最优隶属度矩阵 U
        U = count_membership_matrix(X, m, C)
        # 根据隶属度矩阵 U 计算新的聚类中心点 C1
        C1 = count_cluster_center(X, m, U)
        # 收敛
        if distance_between(C, C1) < alpha:
            C = C1
            break
        # 更新聚类中心
        C = C1
    # 返回新的聚类中心点
    return C
    
def main():
    """ 先聚类再分类
    """
    # 读取数据
    data, tags = read_data()
    if len(data) < 1:
        raise Exception("数据读取异常")

    # 开始聚类
    cluster(data, tags)

if __name__ == "__main__":
    main()