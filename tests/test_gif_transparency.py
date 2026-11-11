from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def make_palette_gif_with_transparent_background():
    # Palette source: index 1 is the transparent background, index 0 is blue.
    img = Image.new("P", (40, 40), 0)
    img.putpalette([0, 0, 255, 0, 0, 0] + [0, 0, 0] * 254)
    for x in range(20):
        for y in range(40):
            img.putpixel((x, y), 1)
    img.info["transparency"] = 1
    buffer = BytesIO()
    img.save(buffer, "GIF", transparency=1)
    return buffer.getvalue()


def test_resized_gif_keeps_transparency_index():
    config = Config(PILLOW_PRESERVE_INDEXED_MODE=True)
    engine = Engine(Context(config=config))
    source = Image.open(BytesIO(make_palette_gif_with_transparent_background()))
    engine.image = source
    engine.original_mode = source.mode
    engine.extension = ".gif"

    engine.resize(80, 80)
    output = engine.read(".gif")

    result = Image.open(BytesIO(output))
    assert result.info.get("transparency") is not None
