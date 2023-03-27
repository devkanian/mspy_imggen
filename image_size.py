class ImageSize:
    _width: int
    _height: int

    def __init__(self, width=0, height=0) -> None:
        self._width = width
        self._height = height

    @property
    def size(self):
        return (self._width, self._height)

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @size.setter
    def size(self, size: tuple):
        if len(size) == 2 and (type(size[0]) == int) and (type(size[1] == int)) and size[0] > 0 and size[1] > 0:
            (self._width, self._height) = (size)

    @width.setter
    def width(self, width: int):
        self._width = max(0, width)

    @height.setter
    def height(self, height: int):
        self._height = max(0, height)
