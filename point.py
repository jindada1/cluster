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
    @tag.setter
    def tag(self, new_tag):
        self._tag = new_tag