import pytest
from os.path import exists
from bar_text_in_rect_config import BarTextInRectConfig


@pytest.fixture(scope="function")
def btirc() -> BarTextInRectConfig:
    btirc = BarTextInRectConfig()
    return btirc


class TestGetFontSize:
    @pytest.mark.parametrize(
        "bar_height, line_width, font_size_index, font_size",
        [
            (100, 10, 1, 80),
            (120, 10, 0.7, 70),
            (100, 0, 0.63, 63),
            (100, 0, -1, (BarTextInRectConfig.DEFAULT_FONT_SIZE_INDEX) * 100),
        ],
    )
    def test_pass_relative(self, btirc, bar_height, line_width, font_size_index, font_size):
        btirc.set_relative_font_size(font_size_index)
        fs = btirc.get_font_size(bar_height, line_width)
        assert fs == font_size

    @pytest.mark.parametrize(
        "bar_height, line_width, font_size",
        [
            (100, 10, 1),
            (200, 20, 2),
            (300, 30, 3),
        ],
    )
    def test_pass_fixed(self, btirc, bar_height, line_width, font_size):
        btirc.set_fixed_font_size(font_size)
        fs = btirc.get_font_size(bar_height, line_width)
        assert fs == font_size

    def test_fail_fixed(self, btirc):
        btirc.set_fixed_font_size(-1)
        fs = btirc.get_font_size(120, 10)
        assert fs != -1
        assert fs == (BarTextInRectConfig.DEFAULT_FONT_SIZE_INDEX) * 100


class TestSetFixedFontSize:
    def test_pass(self, btirc):
        FONT_SIZE = 10
        btirc.set_fixed_font_size(FONT_SIZE)
        assert btirc._font_size == FONT_SIZE
        assert btirc.font_size_fixed is True
        assert btirc.font_size_relative is False


class TestSetRelativeFontsize:
    def test_pass(self, btirc):
        FONT_SIZE_INDEX = 0.53
        btirc.set_relative_font_size(FONT_SIZE_INDEX)
        assert btirc._font_size == FONT_SIZE_INDEX
        assert btirc.font_size_fixed is False
        assert btirc.font_size_relative is True


class TestGetLeftMargin:
    @pytest.mark.parametrize(
        "bar_height, left_margin_index, left_margin",
        [
            (100, 1, 100),
            (100, 0.63, 63),
            (100, -1, (BarTextInRectConfig.DEFAULT_LEFT_MARGIN) * 100),
        ],
    )
    def test_pass_relative(self, btirc, bar_height, left_margin_index, left_margin):
        btirc.set_relative_left_margin(left_margin_index)
        lm = btirc.get_left_margin(bar_height)
        assert lm == left_margin

    @pytest.mark.parametrize("bar_height, left_margin", [(100, 100), (200, 100), (100, 63)])
    def test_pass_fixed(self, btirc, bar_height, left_margin):
        btirc.set_fixed_left_margin(left_margin)
        lm = btirc.get_left_margin(bar_height)
        assert lm == left_margin

    def test_fail_fixed(self, btirc):
        btirc.set_fixed_left_margin(-1)
        lm = btirc.get_left_margin(100)
        assert lm != -1
        assert lm == (BarTextInRectConfig.DEFAULT_LEFT_MARGIN) * 100


class TestSetFixedLeftMargin:
    def test_pass(self, btirc):
        LEFT_MARGIN = 10
        btirc.set_fixed_left_margin(LEFT_MARGIN)
        assert btirc._left_margin == LEFT_MARGIN
        assert btirc.left_margin_fixed is True
        assert btirc.left_margin_relative is False


class TestSetRelativeLeftMargin:
    def test_pass(self, btirc):
        LEFT_MARGIN_INDEX = 0.53
        btirc.set_relative_left_margin(LEFT_MARGIN_INDEX)
        assert btirc._left_margin == LEFT_MARGIN_INDEX
        assert btirc.left_margin_fixed is False
        assert btirc.left_margin_relative is True


class TestFontFilenameSetter:
    def test_pass(self, btirc):
        FONT_FILENAME = "tests//test_fake_font_file.ttf"
        btirc.font_filename = FONT_FILENAME
        assert btirc.font_filename == FONT_FILENAME

    def test_fail_wrong_ext(self, btirc):
        FONT_FILENAME = "tests//test_bar_text_in_rect_config.py"
        btirc.font_filename = FONT_FILENAME
        assert exists(FONT_FILENAME) is True  # <--- confirm that extension is the reason
        assert btirc.font_filename == BarTextInRectConfig.DEFAULT_FONT_FILE

    def test_fail_not_exist(self, btirc):
        FONT_FILENAME = "tests//this_file_doesnt_exist.ttf"
        btirc.font_filename = FONT_FILENAME
        assert btirc.font_filename == BarTextInRectConfig.DEFAULT_FONT_FILE
