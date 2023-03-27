class ImageFrame:
    _line_width: int

    @property
    def line_width(self) -> int:
        return self._line_width

    @line_width.setter
    def line_width(self, width: int):
        self._line_width = width

    @property
    def frames(self) -> tuple:
        output = tuple((self._line_width for _ in range(4)))
        return output

      