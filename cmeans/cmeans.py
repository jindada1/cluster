from point import Point
import myutills as utils
from loader import read_data, Point, print_points


def generate_points(samples: list, tags: list) -> list:
    """参照传入的样本点，为传入的每一种类型生成一个点

    Args:
        samples: 参考样本点
        tags: 样本点的所有类型

    Returns:
        list: 一组样本点
    """
    points = []
    step = len(samples) // len(tags)
    start = 0
    for tag in tags:
        ps = [prop + 0.1 for prop in samples[start].props]
        points.append(Point(ps, tag))
        start += step

    return points


def count_memberships(sample: Point, fuzzy: float, centers: list) -> list:
    """计算某一个样本到所有聚类中心点的隶属度

    Args:
        sample (Point): 样本
        fuzzy (float): 模糊度
        centers (list): 聚类中心点

    Returns:
        list: 一组隶属度
    """
    row = []
    for c in centers:
        Dpq = utils.distance_of_two_points(sample, c)
        array = [(Dpq / utils.distance_of_two_points(sample, i)) ** (1 / (fuzzy - 1))
                 for i in centers]
        row.append(1 / sum(array))

    return row


def count_membership_matrix(samples: list, fuzzy: float, centers: list) -> list:
    """根据聚类中心点计算隶属度矩阵，M[point][center]

    Args:
        samples (list): 一组样本
        fuzzy (float): 模糊度
        centers (list): 聚类中心点

    Returns:
        list: 隶属度矩阵
    """
    matrix = []
    for sample in samples:
        # 计算该样本到各个中心点的隶属度
        mem_row = count_memberships(sample, fuzzy, centers)
        # print(mem_row)
        matrix.append(mem_row)

    return matrix


def count_cluster_center(samples: list, fuzzy: float, membership: list) -> list:
    """根据隶属度矩阵更新聚类中心点

    Args:
        samples (list): 样本
        fuzzy (float): 模糊度
        membership (list): 隶属度矩阵

    Returns:
        list: 一组聚类中心点
    """
    C = membership[0]
    for i in range(len(C)):
        down = [(row[i] ** fuzzy) for row in membership]
        up_points = [utils.point_mul(p, u) for u, p in zip(down, samples)]
        up_point = utils.point_sum(up_points)
        C[i] = utils.point_sub(up_point, sum(down))

    return C


def updateC(to: list, _from: list):
    """更新聚类中心点的坐标

    Args:
        to (list): 原中心点
        _from (list): 新坐标的中心点

    Raises:
        Exception: 新旧中心点数量不同
    """
    if not len(to) == len(_from):
        raise Exception("无法更新两批长度不同的样本")

    for i in range(len(to)):
        to[i].props = _from[i].props


def cluster(X: list, tags: list, fuzzy=2, precise=0.0000001) -> list:
    """模糊聚类过程

    Args:
        X (list): 待聚类的样本点
        tags (list): 类别
        fuzzy (int, optional): 模糊度. Defaults to 2.
        precise (float, optional): 精度. Defaults to 0.0000001.

    Returns:
        list: 一组聚类中心点
    """
    # 根据样本生成指定数量的聚类中心点
    C = generate_points(X, tags)
    print("初始类中心点")
    print_points(C)
    # 设置隶属度矩阵
    U = []
    # 开始迭代
    iter_num = 0
    while iter_num < 1000:
        iter_num += 1
        # 根据 C 计算最优隶属度矩阵 U
        U = count_membership_matrix(X, fuzzy, C)
        # 根据隶属度矩阵 U 计算新的聚类中心点 C1
        C1 = count_cluster_center(X, fuzzy, U)
        # 收敛
        if utils.distance_between(C, C1) < precise:
            updateC(C, C1)
            print("在第%d次迭代时收敛" % iter_num)
            break
        # 更新聚类中心
        updateC(C, C1)
    # 返回新的聚类中心点
    return C


def classify(sample: Point, centers: list) -> float:
    """判断样本点在传入类别中属于哪个类别

    Args:
        sample (Point): 样本点
        centers (list): 一组聚类中心

    Returns:
        float: 类别
    """
    mindis = utils.distance_of_two_points(sample, centers[0])
    tag = centers[0].tag
    for center in centers:
        dis = utils.distance_of_two_points(sample, center)
        if mindis > dis:
            mindis = dis
            tag = center.tag

    return tag


def verify(samples: list, centers: list) -> (float, dict):
    """验证聚类中心的准确度

    Args:
        samples (list): 样本点
        centers (list): 聚类中心

    Returns:
        float: 准确率
    """
    res = {}
    for c in centers:
        res[c.tag] = []

    right = 0
    for sample in samples:
        predict = classify(sample, centers)
        right += (predict == sample.tag)
        res[predict].append(sample)

    return right / len(samples), res


def main():
    """ 先聚类再分类
    """
    filename = "./iris.txt"
    # 读取数据
    data, tags = read_data(filename)
    if len(data) < 1:
        raise Exception("数据读取异常")

    # 开始聚类
    C = cluster(data, tags)
    print("聚类后的类中心")
    print_points(C)
    # 检查聚类效果
    accuracy, res = verify(data, C)
    print("聚类准确率为%f"%accuracy)
    print("聚类的结果如下")
    for key in res:
        print("属于第%s类的样本有"%key)
        print_points(res[key])


if __name__ == "__main__":
    main()
