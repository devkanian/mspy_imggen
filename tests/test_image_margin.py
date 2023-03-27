import pytest
from image_margin import ImageMargin
from image_size import ImageSize


class TestMarginProperty:
    def test_pass(self):
        im = ImageMargin()
        m = im.margin
        assert m is None

    @pytest.mark.parametrize("left, right, bottom, top, margin", [(1, 2, 3, 4, (1, 2, 3, 4)),
                                                                  (1, 1, 2, 2, (1, 2)),
                                                                  (1, 1, 1, 1, (1)),
                                                                  ])
    def test_margin(self, left, right, bottom, top, margin):
        im = ImageMargin()
        (im.left, im.right, im.bottom, im.top) = (left, right, bottom, top)
        assert im.margin == margin

    @pytest.mark.parametrize("left, right, bottom, top, margin", [(1, 2, 3, 4, (1, 2, 3, 4)),
                                                                  (1, 1, 2, 2, (1, 2)),
                                                                  (1, 1, 1, 1, 1),
                                                                  (0, 0, 0, 0, -1),
                                                                  ])
    def test_margin_setter(self, left, right, bottom, top, margin):
        im = ImageMargin()
        im.margin = margin
        
        assert im.margins == (left, right, bottom, top)
