from image_size import ImageSize


class ImageMargin:
    _top, _bottom, _left, _right = (None, None, None, None)
    _img_size = ImageSize

    @property
    def bottom(self) -> int:
        return self._bottom

    @property
    def top(self) -> int:
        return self._top

    @property
    def left(self) -> int:
        return self._left

    @property
    def right(self) -> int:
        return self._right

    @bottom.setter
    def bottom(self, value: int):
        self._bottom = max(value, 0)

    @top.setter
    def top(self, value: int):
        self._top = max(value, 0)

    @left.setter
    def left(self, value: int):
        self._left = max(value, 0)

    @right.setter
    def right(self, value: int):
        self._right = max(value, 0)

    @property
    def margin(self):
        if self.bottom == self.top == self.left == self.right:
            return self.bottom
        elif (self.bottom == self.top) and (self.left == self.right):
            return (self.left, self.bottom)
        else:
            return self.margins

    @property
    def margins(self):
        return (self.left, self.right, self.bottom, self.top)

    @margin.setter
    def margin(self, value: int):
        if type(value) == int:
            (self.bottom, self.top, self.left, self.right) = (
                value, value, value, value)
        elif type(value) == tuple:
            if len(value) == 2:
                (self.left, self.right) = (value[0], value[0])
                (self.bottom, self.top) = (value[1], value[1])
            if len(value) == 4:
                (self.left, self.right, self.bottom, self.top) = (
                    value[0], value[1], value[2], value[3])


