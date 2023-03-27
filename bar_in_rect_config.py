
class BarInRectConfig:
    _dist = 8
    _outline_width = 2
    color_fill = (255, 255, 255, 128)
    color_outline = (0, 0, 0, 224)

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value: int):
        self._dist = max(0, value)

    @property
    def outline_width(self):
        return self._outline_width

    @outline_width.setter
    def outline_width(self, value: int):
        self._outline_width = max(0, value)

    def dist_by_percent(self, percent: int, bars_no: int, height: int):
        dist_no = bars_no + 1
        self.dist = max(1, round(height*percent/100/dist_no))
        print (self.dist)
