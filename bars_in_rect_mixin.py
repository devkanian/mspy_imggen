from PIL import ImageDraw
from bar_in_rect_config import BarInRectConfig

from coordinates_transform_helper import CoordinatesTranfromHelper


class BarsInRectMixin:
    cth: CoordinatesTranfromHelper
    bar: BarInRectConfig

    _custom_rect = None

    @property
    def custom_rect(self) -> list:
        return self._custom_rect

    @custom_rect.setter
    def custom_rect(self, value):
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

        if value[0][0] is None:
            value[0] = (self.cth.content_box_coord[0], value[0][1])
        if value[0][1] is None:
            value[0] = (value[0][0], self.cth.content_box_coord[1])
        if value[1][0] is None:
            value[1] = (self.cth.content_box_coord[2], value[1][1])
        if value[1][1] is None:
            value[1] = (value[1][0], self.cth.content_box_coord[3])
        self._custom_rect = value

    def __init__(self, *args, **kwargs) -> None:
        super(BarsInRectMixin, self).__init__(*args, **kwargs)
        self.bar = BarInRectConfig()
        print("BarsInRectMixin")

    # @property
    # def rect(self):
    #     return [(self.cth.content_box_coord[0], self.cth.content_box_coord[1]),
    #             (self.cth.content_box_coord[0]+self.cth.content_box_width, self.cth.content_box_coord[1]+self.cth.content_box_height)]

    def draw_bars_in_rect(self, img: ImageDraw, percents: list,
                          dist_percent=None,
                          bar_height=None
                          ):
        ######################################################################################################
        # TODO: Possible parameters
        #   rect = [(x_start, y_start), (x_end, y_end)]   <--- custom
        ######################################################################################################
        # TODO: features
        #   colors per value - list
        #   fixed_bar_height (must be smaller than calcualated)
        #   scale
        #   texts
        #   icons
        ######################################################################################################
        percents_no = len(percents)

        if self.custom_rect is not None:
            [(x_start, y_start), (x_end, y_end)] = self.custom_rect
            (canvas_width, canvas_heigth) = (x_end-x_start, y_end-y_start)
        else:
            (canvas_width, canvas_heigth) = (self.cth.content_box_width,
                                             self.cth.content_box_height)
            x_start = self.cth.content_box_coord[0]
            y_start = self.cth.content_box_coord[1]

        if dist_percent:
            self.bar.dist_by_percent(
                dist_percent, percents_no, canvas_heigth)

        bar_height = self.calc_bar_height(percents_no, canvas_heigth)
        bar_width_max = (canvas_width - 2 * self.bar.margin)
        bar_top_list = [self.bar.margin + i * (bar_height+self.bar.dist)
                        for i in range(percents_no)]

        for i, percent in enumerate(percents):
            ith_bar_width = percent/100*bar_width_max
            rect = [(x_start + self.bar.margin, y_start + bar_top_list[i]),
                    (x_start + self.bar.margin + ith_bar_width, y_start + bar_top_list[i] + bar_height)]

            img.rectangle(rect, fill=self.bar.color_fill,
                          outline=self.bar.color_outline, width=self.bar.outline_width)

    def calc_bar_height(self, percents_no: int, canvas_heigth: int):
        return (canvas_heigth - (percents_no-1) * (self.bar.dist) - 2*self.bar.margin) / percents_no
