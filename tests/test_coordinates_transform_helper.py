import pytest
from coordinates_transform_helper import CoordinatesTranfromHelper
from image_frame import ImageFrame
from image_margin import ImageMargin
from image_size import ImageSize


@pytest.fixture(scope="session")
def isize():
    isize = ImageSize()
    isize.size = (0, 0)
    return isize


@pytest.fixture(scope="session")
def imargin():
    imargin = ImageMargin()
    imargin.margin = 0
    return imargin


@pytest.fixture(scope="session")
def iframe():
    iframe = ImageFrame()
    iframe.line_width = 0
    return iframe


@pytest.fixture(scope="session")
def cth(isize, imargin, iframe):
    cth = CoordinatesTranfromHelper(size=isize, margin=imargin, frame=iframe)
    return cth


class TestCoordinatesTranfromHelper:

    @pytest.mark.parametrize("loop, sum", [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (-5, 0)])
    def test_fixtures(self,
                      isize: ImageSize, imargin: ImageMargin, iframe: ImageFrame,
                      loop, sum):

        isize.width += loop
        isize.height += loop
        imargin.left += loop
        imargin.right += loop
        imargin.bottom += loop
        imargin.top += loop
        iframe.line_width += loop
        assert isize.size == (sum, sum)
        assert imargin.margins == (sum, sum, sum, sum)
        assert iframe.line_width == sum

    @pytest.mark.parametrize("size, margin, frame, point, result", [
        ((1000, 2000), (100, 200, 300, 400), 10, (111, 311), (1, 1)),
        ((1000, 2000), (100, 200, 300, 400), 10, (500, 1500), (390, 1190)),
        ((1000, 2000), (100, 200, 300, 400), 10, (-500, -500), (390, 1190)),
    ])
    def test_to_content_xy(self,
                           cth: CoordinatesTranfromHelper, isize: ImageSize, imargin: ImageMargin, iframe: ImageFrame,  # <--- fixtures
                           size, margin, frame, point, result):                                                         # <--- parametrize
        isize.size = size
        imargin.margin = margin
        iframe.line_width = frame
        (cx, cy) = cth.to_content_xy(point)
        assert (cx, cy) == result

    @pytest.mark.parametrize("size, margin, frame, point, result", [
        ((1000, 2000), (100, 200, 300, 400), 10, (0, 0), (110, 310)),
        ((1000, 2000), (100, 200, 300, 400), 10, (0, -1), (110, 1589)),
        ((1000, 2000), (100, 200, 300, 400), 10, (-1, 0), (789, 310)),
        ((1000, 2000), (100, 200, 300, 400), 10, (-1, -1), (789, 1589)),
        ((1000, 2000), 0, 10, (-1, -1), (989, 1989)),
        ((1000, 2000), 0, 0, (-1, -1), (999, 1999)),
    ])
    def test_to_global_xy(self,
                          cth: CoordinatesTranfromHelper, isize: ImageSize, imargin: ImageMargin, iframe: ImageFrame,  # <--- fixtures
                          size, margin, frame, point, result):                                                         # <--- parametrize
        isize.size = size
        imargin.margin = margin
        iframe.line_width = frame
        (cx, cy) = cth.to_global_xy(point)
        assert (cx, cy) == result

    @pytest.mark.parametrize("size, margin, frame, result", [
        ((1000, 2000), (100, 200, 300, 400), 10, (680, 1280)),
        ((1000, 2000), 0, 0, (1000, 2000)),
        ((1000, 2000), 1, 0, (998, 1998)),
        ((1000, 2000), 0, 1, (998, 1998)),
        ((1000, 2000), 1, 1, (996, 1996)),
        ((1000, 2000), 500, 500, (0, 0)),
    ])
    def test_box_content_size(self,
                              cth: CoordinatesTranfromHelper, isize: ImageSize, imargin: ImageMargin, iframe: ImageFrame,   # <--- fixtures
                              size, margin, frame, result):                                                                 # <--- parametrize
        isize.size = size
        imargin.margin = margin
        iframe.line_width = frame
        assert cth.content_box_size == result
