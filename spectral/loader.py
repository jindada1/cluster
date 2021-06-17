import numpy as np

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
    props = list(map(lambda s : float(s), line.split(serp)))
    label = props.pop(-1)

    return props, label

def read_data(filename):
    """从文件中读取数据
    Args:
        filename: 存放数据的文件路径
    Returns:
        一组 Point 对象
    """
    data = []
    labels = []
    # 读取文件的内容
    f = open(filename)
    lines = f.readlines()
    # 解析文件内容
    for line in lines:
        props, label = parse_line(line)
        if not props:
            continue
        
        data.append(props)
        labels.append(label)

    # 关闭文件
    f.close()
    return np.array(data), np.array(labels)

def show(filename):
    """展示文件中的数据
    """
    data, labels = read_data(filename)
    print(data, labels)


if __name__ == "__main__":

    filename = "./iris.txt"
    data, label = read_data(filename)
    print(data.dtype, label.dtype)