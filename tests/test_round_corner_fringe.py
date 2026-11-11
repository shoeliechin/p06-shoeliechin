# Regression test for issue 2: transparent round_corner must not leave a dark ring.

import unittest

from thumbor.ext.filters import _round_corner

WIDTH = 20
HEIGHT = 20
RADIUS = 6
COLOR = (10, 200, 30)


def _solid_rgba():
    data = bytearray()
    for _ in range(WIDTH * HEIGHT):
        data += bytes((COLOR[0], COLOR[1], COLOR[2], 255))
    return bytes(data)


def _apply(transparent):
    return bytearray(
        _round_corner.apply(
            1,
            "RGBA",
            RADIUS,
            RADIUS,
            COLOR[0],
            COLOR[1],
            COLOR[2],
            WIDTH,
            HEIGHT,
            _solid_rgba(),
            transparent,
        )
    )


class RoundCornerFringeTestCase(unittest.TestCase):
    def test_transparent_edge_pixels_keep_source_rgb(self):
        out = _apply(1)
        edge_pixels = 0
        for i in range(0, len(out), 4):
            r, g, b, a = out[i], out[i + 1], out[i + 2], out[i + 3]
            if 0 < a < 255:
                edge_pixels += 1
                self.assertEqual(
                    (r, g, b),
                    COLOR,
                    "edge pixel at byte offset %d darkened" % i,
                )
        self.assertGreater(
            edge_pixels, 0, "no partially transparent edge pixels found"
        )

    def test_opaque_mode_is_unchanged(self):
        out = _apply(0)
        for i in range(0, len(out), 4):
            self.assertEqual(
                (out[i], out[i + 1], out[i + 2], out[i + 3]),
                (COLOR[0], COLOR[1], COLOR[2], 255),
                "opaque pixel at byte offset %d changed" % i,
            )
