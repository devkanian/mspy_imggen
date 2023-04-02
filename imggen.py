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

    def __init__(self, width: int, height: int, *args, **kwargs) -> None:
        super(ImageGenerator, self).__init__(*args, **kwargs)
        self.size = ImageSize()
        self.margin = ImageMargin()
        self.frame = ImageFrame()
        self.colors = ColorsPalette()
        self.cth = CoordinatesTranfromHelper(self.size, self.margin, self.frame)
        (self.size.width, self.size.height) = (width, height)

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

    def draw_frame(self, canvas: ImageDraw):
        canvas.rectangle(
            self.frame_coordinates,
            fill=self.colors._frame_bg,
            outline=self.colors._frame_outline,
            width=self.frame.line_width,
        )

    def draw(self):
        img = Image.new("RGB", self.size.size, self.colors._img_bg)
        canvas = ImageDraw.Draw(img, mode="RGBA")
        self.draw_frame(canvas)
        self.write_on_margin(canvas, "TOP-LEFT", TxtPos.TOP, TxtAlign.LEFT)
        self.write_on_margin(canvas, "TOP-CENTER", TxtPos.TOP, TxtAlign.CENTER)
        self.write_on_margin(canvas, "TOP-RIGHT", TxtPos.TOP, TxtAlign.RIGTH)
        self.write_on_margin(canvas, "BOTTOM-LEFT", TxtPos.BOTTOM, TxtAlign.LEFT)
        self.write_on_margin(canvas, "BOTTOM-CENTER", TxtPos.BOTTOM, TxtAlign.CENTER)
        self.write_on_margin(canvas, "BOTTOM-RIGHT", TxtPos.BOTTOM, TxtAlign.RIGTH)
        self.draw_bars_in_rect(
            img=canvas,
            percents=[
                (66, "01:03:34  Run"),
                (10, "02:04:54  Weight Lifting"),
                (60, "00:23:53  Indoor Cycling"),
                (90, "01:02:34  Roller skating"),
                (33, "00:30:00  Yoga"),
            ],
        )
        img.save("misc/test.png")
        img.show()

    def write_on_margin(
        self,
        canvas: ImageDraw,
        text: str,
        positon=TxtPos.TOP,
        alignment=TxtAlign.CENTER,
    ):
        font = ImageFont.truetype("fonts//AmaticSC-Bold.ttf", 32)
        w, h = canvas.textsize(text, font=font)
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
        canvas.text((text_x, text_y), text, (0, 0, 0), font=font)


class ImageGeneratorWithBars(ImageGenerator, BarsInRectMixin):
    pass


if __name__ == "__main__":
    ig = ImageGeneratorWithBars(1000, 1000)
    ig.margin.margin = 90
    ig.margin.bottom = 200
    ig.frame.line_width = 16
    ig.bar.dist = 8
    ig.bar.outline_width = 4
    ig.bar.margin = 16
    ig.custom_rect = [(None, None), (None, 500)]
    # ig.fixed_bar_height = 100
    
    # ig.bar_text.font_filename = "fonts//AmaticSC-Bold.ttf"
    ig.bar_text.set_fixed_font_size(80)
    ig.bar_text.set_relative_font_size(1)
    # ig.bar_text.set_fixed_left_margin(100)
    ig.draw()

    print(ig)
