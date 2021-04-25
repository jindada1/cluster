
filename = "./iris.txt"

class Item(object):
    """item to cluster"""
    def __init__(self, props, tag):
        
        self._props = props
        self._tag = tag
        
    @property
    def props(self):
        """The props property."""
        return self._props

    @property
    def tag(self):
        """The tag property."""
        return self._tag
        
        
def parse_line(line):
    
    if len(line) < 1:
        return None
    serp = '\t'
    nums = list(map(lambda s : float(s), line.split(serp)))
    tag = nums.pop(-1)

    return Item(nums, tag)

def read_data():
    items = []
    # read content in file
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            item = parse_line(line)
            if not item:
                continue
            items.append(item)

    return items

def show():
    for data in read_data():
        print(data.props, data.tag)

if __name__ == "__main__":
    show()