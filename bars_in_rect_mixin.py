from PIL import ImageDraw
from bar_in_rect_config import BarInRectConfig

from coordinates_transform_helper import CoordinatesTranfromHelper


class BarsInRectMixin:
    cth: CoordinatesTranfromHelper
    bar: BarInRectConfig

    def __init__(self, *args, **kwargs) -> None:
        super(BarsInRectMixin, self).__init__(*args, **kwargs)
        self.bar = BarInRectConfig()
        print("BarsInRectMixin")

    @property
    def rect(self):
        return [(self.cth.content_box_coord[0], self.cth.content_box_coord[1]),
                (self.cth.content_box_coord[0]+self.cth.content_box_width, self.cth.content_box_coord[1]+self.cth.content_box_height)]

    def draw_bars_in_rect(self, img: ImageDraw, percents: list,
                          rect=None,
                          dist_percent=None,
                          bar_height=None
                          ):
        ######################################################################################################
        # TODO: Possible parameters
        #   rect = [(x_start, y_start), (x_end, y_end)]   <--- custom
        #   dist/margin - auto by %
        ######################################################################################################
        # TODO: features
        #   colors per value - list
        #   fixed_bar_height (must be smaller than calcualated)
        #   scale
        #   texts
        #   icons
        ######################################################################################################
        if dist_percent:
            self.bar.dist_by_percent(dist_percent, len(
                percents), self.cth.content_box_height)

        (canvas_width, canvas_heigth) = (self.cth.content_box_width,
                                         self.cth.content_box_height)

        content_box_x = self.cth.content_box_coord[0]
        content_box_y = self.cth.content_box_coord[1]

        bar_height = self.calc_bar_height(percents, canvas_heigth)
        bar_width_max = (canvas_width - 2 * self.bar.margin)
        bar_top_list = [self.bar.margin + i*(bar_height+self.bar.dist)


                        for i in range(len(percents))]
        for i, percent in enumerate(percents):
            ith_bar_width = percent/100*bar_width_max
            rect = [(content_box_x + self.bar.margin, content_box_y + bar_top_list[i]),
                    (content_box_x + self.bar.margin + ith_bar_width, content_box_y + bar_top_list[i] + bar_height)]

            img.rectangle(rect, fill=self.bar.color_fill,
                          outline=self.bar.color_outline, width=self.bar.outline_width)

    def calc_bar_height(self, percents, canvas_heigth):
        return (canvas_heigth - (len(percents)-1) * (self.bar.dist) - 2*self.bar.margin) / len(percents)
