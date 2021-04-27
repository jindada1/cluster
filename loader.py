from point import Point

def parse_line(line):
    """解析一行文本，规则为：由制表符 \\t 分割数据，最后一个数据为类别
    Args:
        line: 待解析的文本
    Returns:
        一个 Point 对象
    """
    if len(line) < 1:
        return None
    serp = '\t'
    nums = list(map(lambda s : float(s), line.split(serp)))
    tag = nums.pop(-1)

    return Point(nums, tag)


def read_data(filename):
    """从文件中读取数据
    Args:
        filename: 存放数据的文件路径
    Returns:
        一组 Point 对象
    Raise:
        
    """
    points = []
    tags = []
    # 读取文件的内容
    f = open(filename)
    lines = f.readlines()
    # 解析文件内容
    for line in lines:
        point = parse_line(line)
        if not point:
            continue
        # 去重，统计所有的类型    
        if not point.tag in tags:
            tags.append(point.tag)

        points.append(point)

    # 关闭文件
    f.close()
    return points, tags

def show():
    """展示文件中的数据
    """
    filename = "./iris.txt"
    samples, tags = read_data(filename)
    print_points(samples)
    print(tags)

def print_points(samples):
    """将样本点输出到控制台
    
    Args:
        samples (list): 样本点        
    """
    for data in samples:
        print(data.props, data.tag)

if __name__ == "__main__":
    show()