from image_frame import ImageFrame
from image_margin import ImageMargin
from image_size import ImageSize


class CoordinatesTranfromHelper:
    _margin: ImageMargin
    _size: ImageSize
    _frame: ImageFrame

    def __init__(self, size: ImageSize, margin: ImageMargin,  frame: ImageFrame) -> None:
        self._size = size
        self._margin = margin
        self._frame = frame

    @property
    def content_box_width(self) -> int:
        size = self._size.size
        margins = self._margin.margins
        width_tuple = self._frame.frames
        width = size[0] - margins[0] - margins[1] - \
            width_tuple[0] - width_tuple[1]
        return max(0, width)

    @property
    def content_box_height(self) -> int:
        size = self._size.size
        margins = self._margin.margins
        width_tuple = self._frame.frames
        height = (size[1] - margins[2] - margins[3] -
                  width_tuple[2] - width_tuple[3])
        return max(0, height)

    @property
    def content_box_size(self) -> tuple:
        return (self.content_box_width, self.content_box_height)

    @property
    def content_box_coord(self) -> tuple:
        return (self._margin.left + self._frame.frames[0],
                self._margin.top + self._frame.frames[2],
                self._size.width - self._margin.right - self._frame.frames[1],
                self._size.height - self._margin.bottom - self._frame.frames[3])

    def to_content_xy(self, gpoint: tuple) -> tuple:
        (xin, yin) = gpoint
        (ml, _, mb, _) = self._margin.margins
        (fl, _, fb, _) = self._frame.frames
        (img_width, img_height) = self._size.size
        if xin < 0:
            xin = img_width+xin
        if yin < 0:
            yin = img_height+yin
        xout = xin - ml - fl
        yout = yin - mb - fb
        return (xout, yout)

    def to_global_xy(self, cpoint: tuple) -> tuple:
        (xin, yin) = cpoint
        (ml, mr, mb, mt) = self._margin.margins
        (fl, fr, fb, ft) = self._frame.frames
        (img_width, img_height) = self._size.size
        xout = xin + ml + fl if xin >= 0 else img_width - mr - fr + xin
        yout = yin + mb + fb if yin >= 0 else img_height - mt - ft + yin
        return (xout, yout)
