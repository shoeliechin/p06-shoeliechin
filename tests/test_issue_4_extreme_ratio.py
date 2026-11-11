# tests/test_issue_4_extreme_ratio.py
from tornado.testing import gen_test

from tests.base import TestCase
from tests.fixtures.transformer_test_data import TestData
from thumbor.transformer import Transformer


class ExtremeRatioTestCase(TestCase):
    @gen_test
    async def test_stretch_to_wide_strip_has_at_least_one_row(self):
        data = TestData(
            source_width=16,
            source_height=16,
            target_width=800,
            target_height=20,
            halign="center",
            valign="middle",
            focal_points=[],
            crop_left=None,
            crop_top=None,
            crop_right=None,
            crop_bottom=None,
        )
        ctx = data.to_context()
        engine = ctx.modules.engine
        await Transformer(ctx).transform()

        for crop in engine.calls["crop"]:
            assert crop["bottom"] - crop["top"] >= 1
            assert crop["right"] - crop["left"] >= 1

    @gen_test
    async def test_fit_in_1x1_on_wide_source_gives_one_pixel_side(self):
        data = TestData(
            source_width=940,
            source_height=2,
            target_width=1,
            target_height=1,
            halign="center",
            valign="middle",
            focal_points=[],
            crop_left=None,
            crop_top=None,
            crop_right=None,
            crop_bottom=None,
        )
        ctx = data.to_context()
        ctx.request.fit_in = True
        engine = ctx.modules.engine
        await Transformer(ctx).transform()

        assert len(engine.calls["resize"]) == 1
        assert engine.calls["resize"][0]["width"] >= 1
        assert engine.calls["resize"][0]["height"] >= 1
