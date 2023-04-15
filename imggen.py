from enum import Enum
from PIL import Image, ImageDraw, ImageFont
from bars_in_rect_mixin import BarsInRectMixin

from coordinates_transform_helper import CoordinatesTranfromHelper
from image_colors import ColorsPalette
from image_frame import ImageFrame
from image_margin import ImageMargin
from image_size import ImageSize


class TxtPos(Enum):
    TOP = 0
    BOTTOM = 1


class TxtAlign(Enum):
    LEFT = 0
    CENTER = 1
    RIGTH = 2


class ImageGenerator:
    size: ImageSize
    margin: ImageMargin
    frame: ImageFrame
    cth: CoordinatesTranfromHelper
    colors: ColorsPalette

    _img: Image
    _canvas: ImageDraw

    def __init__(self, width: int, height: int, *args, **kwargs) -> None:
        super(ImageGenerator, self).__init__(*args, **kwargs)
        self.size = ImageSize()
        self.margin = ImageMargin()
        self.frame = ImageFrame()
        self.colors = ColorsPalette()
        self.cth = CoordinatesTranfromHelper(self.size, self.margin, self.frame)
        (self.size.width, self.size.height) = (width, height)

        self._img = Image.new("RGB", self.size.size, self.colors._img_bg)
        self._canvas = ImageDraw.Draw(self._img, mode="RGBA")

    def __str__(self) -> str:
        return (
            f"self.size.width:      {self.size.width}\n"
            f"self.size.height:     {self.size.height}\n"
            f"self.margin.left:     {self.margin.left}\n"
            f"self.margin.right:    {self.margin.right}\n"
            f"self.margin.bottom:   {self.margin.bottom}\n"
            f"self.margin.top       {self.margin.top}\n"
            f"self.frame.line_width {self.frame.line_width}\n"
        )

    @property
    def frame_coordinates(self) -> list:
        start_point = (self.margin.left, self.margin.top)
        end_point = (
            self.size.width - self.margin.right,
            self.size.height - self.margin.bottom,
        )
        return [start_point, end_point]

    def draw_frame(self):
        self._canvas.rectangle(
            self.frame_coordinates,
            fill=self.colors._frame_bg,
            outline=self.colors._frame_outline,
            width=self.frame.line_width,
        )

    def show(self):
        self._img.save("misc/test.png")
        self._img.show()

    def write_on_margin(
        self,
        text: str,
        positon=TxtPos.TOP,
        alignment=TxtAlign.CENTER,
    ):
        font = ImageFont.truetype("fonts//AmaticSC-Bold.ttf", 32)
        # font = ImageFont.truetype("fonts//Overlock-Black.ttf", 32)

        ascent, descent = font.getmetrics()
        w = font.getmask(text).getbbox()[2]
        # h = font.getmask(text).getbbox()[3]   <--- this would show height for specific text        
        h = ascent + descent   # <--- this is height for font (text independent)

        match positon:
            case positon.TOP:
                text_y = (self.margin.top - h) // 2
            case positon.BOTTOM:
                text_y = self.size.height - self.margin.bottom + (self.margin.bottom - h) // 2
        match alignment:
            case TxtAlign.LEFT:
                text_x = self.margin.left
            case TxtAlign.CENTER:
                text_x = (self.size.width - w + self.margin.left - self.margin.right) // 2
            case TxtAlign.RIGTH:
                text_x = self.size.width - self.margin._right - w
        self._canvas.text((text_x, text_y), text, (0, 0, 0), font=font)
        
        


class ImageGeneratorWithBars(ImageGenerator, BarsInRectMixin):
    pass


if __name__ == "__main__":
    ig = ImageGeneratorWithBars(1000, 1000)
    ig.margin.margin = 40
    # ig.margin.bottom = 200
    ig.frame.line_width = 16
    ig.bar.dist = 8
    ig.bar.outline_width = 4
    ig.bar.margin = 16
    ig.custom_bar_rect = [(None, None), (None, 500)]
    # ig.fixed_bar_height = 100

    # ig.bar_text.font_filename = "fonts//AmaticSC-Bold.ttf"
    ig.bar_text.set_fixed_font_size(80)
    ig.bar_text.set_relative_font_size(1)
    # ig.bar_text.set_fixed_left_margin(100)
    ig.draw_frame()
    ig.write_on_margin("TOP-LEFT", TxtPos.TOP, TxtAlign.LEFT)
    ig.write_on_margin("TOP-CENTER", TxtPos.TOP, TxtAlign.CENTER)
    ig.write_on_margin("TOP-RIGHT", TxtPos.TOP, TxtAlign.RIGTH)
    ig.write_on_margin("BOTTOM-LEFTj", TxtPos.BOTTOM, TxtAlign.LEFT)
    ig.write_on_margin("BOTTOM-CENTERÓ", TxtPos.BOTTOM, TxtAlign.CENTER)
    ig.write_on_margin("BOTTOM-RIGHT", TxtPos.BOTTOM, TxtAlign.RIGTH)
    ig.draw_bars_in_rect(
        percents=[
            (66, "01:03:34  Run"),
            (10, "02:04:54  Weight lifting"),
            (60, "00:23:53  Indoor Cycling"),
            (90, "01:02:34  Roller skating"),
            (33, "00:30:00  Yoga"),
        ],
    )
    ig.show()
    # print(ig)
