class Point(object):
    """待聚类的样本点类型
    Attributes:
        props: 样本点的属性（坐标）
        tag: 样本点所属的类别
    """
    def __init__(self, props, tag):
        
        self._props = props
        self._tag = tag
        
    @property
    def props(self):
        """The props property."""
        return self._props
    @props.setter
    def props(self, new_props):
        if not len(new_props) == len(self._props):
            raise Exception("属性维度不应发生改变")
        self._props = new_props

    @property
    def tag(self):
        """The tag property."""
        return self._tag
    
        

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
    for data in samples:
        print(data.props, data.tag)
    print(tags)


if __name__ == "__main__":
    show()