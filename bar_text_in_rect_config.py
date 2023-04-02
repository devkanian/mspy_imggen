from os.path import exists

DEFAULT_FONT_FILE = "fonts//Overlock-Black.ttf"


class BarTextInRectConfig:
    DEFAULT_FONT_SIZE_INDEX = 0.7
    DEFAULT_LEFT_MARGIN = 0.1
    DEFAULT_FONT_FILE = "fonts//Overlock-Black.ttf"
    DEFAULT_UPDOWN_CORRECTION = 0.13

    _font_size_fixed = False
    _font_size = DEFAULT_FONT_SIZE_INDEX

    _left_margin_fixed = False
    _left_margin = DEFAULT_LEFT_MARGIN

    _font_filename = DEFAULT_FONT_FILE

    updown_correction = DEFAULT_UPDOWN_CORRECTION

    # FONT SIZE SECTION

    def get_font_size(self, bar_height: int, line_width: int):
        if self.font_size_fixed:
            return self._font_size
        else:
            return round((bar_height - 2 * line_width) * self._font_size)

    def set_fixed_font_size(self, font_size: int):
        if font_size > 0:
            self.font_size_fixed = True
            self._font_size = font_size

    def set_relative_font_size(self, font_size_index: float):
        if font_size_index > 0:
            self.font_size_relative = True
            self._font_size = font_size_index

    @property
    def font_size_fixed(self) -> bool:
        return self._font_size_fixed

    @font_size_fixed.setter
    def font_size_fixed(self, value):
        self._font_size_fixed = value

    @property
    def font_size_relative(self) -> bool:
        return not self._font_size_fixed

    @font_size_relative.setter
    def font_size_relative(self, value):
        self._font_size_fixed = not value

    # LEFT MARGIN SECTION

    def get_left_margin(self, bar_height: int):
        if self.left_margin_fixed:
            return self._left_margin
        else:
            return round(bar_height * self._left_margin)

    def set_fixed_left_margin(self, left_margin: int):
        if left_margin > 0:
            self.left_margin_fixed = True
            self._left_margin = left_margin

    def set_relative_left_margin(self, left_margin_index: float):
        if left_margin_index > 0:
            self.left_margin_relative = True
            self._left_margin = left_margin_index

    @property
    def left_margin_fixed(self) -> bool:
        return self._left_margin_fixed

    @left_margin_fixed.setter
    def left_margin_fixed(self, value):
        self._left_margin_fixed = value

    @property
    def left_margin_relative(self) -> bool:
        return not self._left_margin_fixed

    @left_margin_relative.setter
    def left_margin_relative(self, value):
        self._left_margin_fixed = not value

    # FONT FILENAME SECTION

    @property
    def font_filename(self) -> str:
        return self._font_filename

    @font_filename.setter
    def font_filename(self, value: str):
        file_has_font_ext = value[-4:] == ".ttf"
        file_exists = exists(value)
        print(file_exists)
        print(file_has_font_ext)
        if file_exists and file_has_font_ext:
            self._font_filename = value
