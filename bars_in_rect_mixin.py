from PIL import ImageDraw, ImageFont
from bar_in_rect_config import BarInRectConfig

from coordinates_transform_helper import CoordinatesTranfromHelper

# DEFAULT_FONT_FILE = "fonts\Alkatra-VariableFont_wght.ttf"
# DEFAULT_FONT_FILE = "fonts\MartianMono-VariableFont_wdth,wght.ttf.ttf"
DEFAULT_FONT_FILE = "fonts\AmaticSC-Bold.ttf"


class BarsInRectMixin:
    cth: CoordinatesTranfromHelper
    bar: BarInRectConfig

    _custom_rect = None
    _fixed_bar_height = None

    def __init__(self, *args, **kwargs) -> None:
        super(BarsInRectMixin, self).__init__(*args, **kwargs)
        self.bar = BarInRectConfig()

    @property
    def custom_rect(self) -> list:
        return self._custom_rect

    @custom_rect.setter
    def custom_rect(self, value):
        # Verify if value is list of 2 tuples of 2 ints or Nones
        # eg. [(100,100), (900,900)]
        # eg. [(None,None), (None,height/2)]    <--- TOP HALF OF image within margins
        if type(value) == list and len(value) == 2:
            for val in value:
                if type(val) == tuple and len(val) == 2:
                    for v in val:
                        if type(v) != int or v <= 0 and v is not None:
                            self._custom_rect = None
                else:
                    self._custom_rect = None
        else:
            self._custom_rect = None

        # Replaces Nones with content box corners
        if value[0][0] is None:
            value[0] = (self.cth.content_box_coord[0], value[0][1])
        if value[0][1] is None:
            value[0] = (value[0][0], self.cth.content_box_coord[1])
        if value[1][0] is None:
            value[1] = (self.cth.content_box_coord[2], value[1][1])
        if value[1][1] is None:
            value[1] = (value[1][0], self.cth.content_box_coord[3])
        self._custom_rect = value

    @property
    def fixed_bar_height(self) -> float:
        return self._fixed_bar_height

    @fixed_bar_height.setter
    def fixed_bar_height(self, value):
        self._fixed_bar_height = value if type(
            value) == int and value > 0 else None

    @property
    def full_rect(self):
        return [(self.cth.content_box_coord[0], self.cth.content_box_coord[1]),
                (self.cth.content_box_coord[0]+self.cth.content_box_width, self.cth.content_box_coord[1]+self.cth.content_box_height)]

    def draw_bars_in_rect(self, img: ImageDraw, percents: list, font_filename=DEFAULT_FONT_FILE):
        ######################################################################################################
        # TODO: features
        #   colors per value - list
        #   scale
        #   icons
        ######################################################################################################
        percents_no = len(percents)

        x_start, y_start, x_end, y_end = self._get_content_rect()
        canvas_width, canvas_height = x_end-x_start, y_end-y_start

        bar_height = self._get_bar_height(percents_no, canvas_height)

        bar_max_width = (canvas_width - 2 * self.bar.margin)
        bar_y_start_list = [self.bar.margin + i * (bar_height+self.bar.dist)
                            for i in range(percents_no)]

        font_percent = 0.5
        font_size = round((bar_height - 2*self.bar.outline_width)*font_percent)
        font = ImageFont.truetype(font=font_filename, size=font_size)

        for i, percent in enumerate(percents):
            ith_bar_width, ith_bar_text = self._get_bar_details(
                bar_max_width, percent)

            rect = self.get_bar_rect(
                x_start, y_start, bar_height, bar_y_start_list, i, ith_bar_width)

            img.rectangle(rect,
                          fill=self.bar.color_fill,
                          outline=self.bar.color_outline,
                          width=self.bar.outline_width)

            if ith_bar_text:
                img.text(self._get_bar_text_start_point(bar_height, rect, font_size),
                         ith_bar_text,
                         (0, 0, 0),
                         font=font)

    def get_bar_rect(self, x_start, y_start, bar_height, bar_y_start_list, i, ith_bar_width):
        rect = [(x_start + self.bar.margin, y_start + bar_y_start_list[i]),
                (x_start + self.bar.margin + ith_bar_width, y_start + bar_y_start_list[i] + bar_height)]

        return rect

    def _get_bar_details(self, bar_max_width, percent):
        if type(percent) == tuple:
            (ith_bar_width, ith_bar_text) = (
                percent[0]/100*bar_max_width, percent[1])
        elif type(percent) in [int, float]:
            ith_bar_width = percent/100*bar_max_width
            ith_bar_text = None
        else:
            ith_bar_width = 0
            ith_bar_text = None
        return ith_bar_width, ith_bar_text

    def _get_bar_height(self, percents_no, canvas_height):
        bar_height = self._calc_bar_height(percents_no, canvas_height)
        if self.fixed_bar_height is not None:
            bar_height = min(bar_height, self.fixed_bar_height)
        return bar_height

    def _get_content_rect(self):
        if self.custom_rect is None:
            [(x_start, y_start), (x_end, y_end)] = self.full_rect
        else:
            [(x_start, y_start), (x_end, y_end)] = self.custom_rect
        return x_start, y_start, x_end, y_end

    def _get_bar_text_start_point(self, bar_height, rect, font_size):
        x_text = rect[0][0] + self.bar.outline_width + max(1, bar_height//10)
        y_text = rect[0][1] + self.bar.outline_width + \
            (bar_height-(1.3*font_size)-2*self.bar.outline_width)//2
        return (x_text, y_text)

    def _calc_bar_height(self, percents_no: int, canvas_heigth: int):
        return (canvas_heigth - (percents_no-1) * (self.bar.dist) - 2*self.bar.margin) / percents_no
