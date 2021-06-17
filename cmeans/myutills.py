from point import Point


def distance_of_two_points(point1: Point, point2: Point) -> float:
    """计算两个样本点的欧氏距离

    Args:
        point1 (Point): 第一个样本点
        point2 (Point): 第二个样本点

    Raises:
        Exception: 无法计算不同维度的样本点

    Returns:
        float: 两个样本点的欧式距离
    """
    # 检查两个点
    if not len(point1.props) == len(point2.props):
        raise Exception("不能计算两个不同维度的点之间的距离")

    dis = 0.0
    for a, b in zip(point1.props, point2.props):
        dis += (a - b) ** 2

    return dis


def distance_between(points1, points2):
    """计算两组样本点之间的欧氏距离

    Args:
        points1 (list): 第一组样本点
        points2 (list): 第二组样本点

    Returns:
        float: 两组样本点的欧氏距离
    """
    # 检查两组点
    if not len(points1) == len(points2):
        raise Exception("不能计算不同数量的两组点之间的距离")

    return sum([distance_of_two_points(p1, p2) for p1, p2 in zip(points1, points2)])


def point_mul(point: Point, num: float) -> Point:
    """定义样本点与数的乘法

    Args:
        point (Point): 样本点
        num (float): 数

    Returns:
        Point: 新的样本点
    """
    props = [prop * num for prop in point.props]
    return Point(props, point.tag)


def point_sum(points: list) -> Point:
    """计算一组样本点的和

    Args:
        points (list): 一组样本点

    Returns:
        Point: 新的样本点
    """
    props = [0] * len(points[0].props)
    for point in points:
        props = [a+b for a, b in zip(point.props, props)]

    return Point(props, points[0].tag)


def point_sub(point: Point, num: float) -> Point:
    """计算样本点与数的除法

    Args:
        point (Point): 样本点
        num (float): 数

    Returns:
        Point: 新的样本点
    """
    return Point([prop / num for prop in point.props], point.tag)
