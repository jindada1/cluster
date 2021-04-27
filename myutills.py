from point import Point

def distance_of_two_points(point1:Point, point2:Point) -> float:
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