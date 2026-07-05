from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "SourceLayers"
EXPORTS = ROOT / "Exports"
SOURCE.mkdir(exist_ok=True)
EXPORTS.mkdir(exist_ok=True)

SIZE = 1024
FONT_PATHS = [
    "/Library/Fonts/SF-Pro-Display-Heavy.otf",
    "/Library/Fonts/SF-Pro-Display-Bold.otf",
    "/System/Library/Fonts/SFNS.ttf",
]


def font(size):
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default(size=size)


def rounded_mask(radius=232):
    mask = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, SIZE, SIZE), radius=radius, fill=255)
    return mask


def gradient_background():
    img = Image.new("RGBA", (SIZE, SIZE), (9, 10, 12, 255))
    pix = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            nx = x / (SIZE - 1)
            ny = y / (SIZE - 1)
            vignette = ((nx - 0.35) ** 2 + (ny - 0.22) ** 2) ** 0.5
            lift = max(0, 1 - vignette * 1.55)
            r = int(8 + 18 * lift + 3 * ny)
            g = int(10 + 24 * lift + 5 * ny)
            b = int(13 + 32 * lift + 8 * ny)
            pix[x, y] = (r, g, b, 255)

    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((54, 54, SIZE - 54, SIZE - 54), radius=208, outline=(255, 255, 255, 24), width=3)
    draw.rounded_rectangle((78, 78, SIZE - 78, SIZE - 78), radius=184, outline=(75, 163, 255, 15), width=2)
    return img


def text_mask():
    mask = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(mask)
    fnt = font(508)
    s_box = draw.textbbox((0, 0), "S", font=fnt)
    t_box = draw.textbbox((0, 0), "T", font=fnt)
    s_w = s_box[2] - s_box[0]
    t_w = t_box[2] - t_box[0]
    kern = -42
    total_w = s_w + t_w + kern
    x = (SIZE - total_w) // 2 - 2
    y = 250
    draw.text((x, y), "S", font=fnt, fill=255)
    draw.text((x + s_w + kern, y), "T", font=fnt, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.15))


def make_type_layer(mask):
    base = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    fill = Image.new("RGBA", (SIZE, SIZE), (246, 247, 242, 255))
    base.alpha_composite(Image.composite(fill, base, mask))

    edge = ImageChops.subtract(mask, ImageChops.offset(mask, 0, 10))
    edge = edge.filter(ImageFilter.GaussianBlur(0.8))
    edge_fill = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 44))
    base.alpha_composite(Image.composite(edge_fill, Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0)), edge))
    return base


def make_shadow_layer(mask):
    long_shadow = Image.new("L", (SIZE, SIZE), 0)
    for i in range(1, 72):
        shifted = ImageChops.offset(mask, i * 3, i * 4)
        long_shadow = ImageChops.lighter(long_shadow, shifted.point(lambda p, n=i: int(p * max(0, 0.33 - n * 0.0038))))
    long_shadow = long_shadow.filter(ImageFilter.GaussianBlur(7))

    soft_shadow = ImageChops.offset(mask, 28, 44).filter(ImageFilter.GaussianBlur(22))
    combined = ImageChops.lighter(long_shadow, soft_shadow.point(lambda p: int(p * 0.46)))

    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_fill = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 178))
    layer.alpha_composite(Image.composite(shadow_fill, layer, combined))
    return layer


def make_highlight_layer(mask):
    rim = ImageChops.subtract(ImageChops.offset(mask, -5, -4), mask)
    rim = rim.filter(ImageFilter.GaussianBlur(1.2)).point(lambda p: min(150, int(p * 1.2)))
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    blue = Image.new("RGBA", (SIZE, SIZE), (75, 163, 255, 118))
    layer.alpha_composite(Image.composite(blue, layer, rim))
    return layer


def save_iconset(master):
    sizes = [16, 20, 29, 32, 40, 58, 60, 64, 76, 80, 87, 120, 128, 152, 167, 180, 256, 512, 1024]
    for size in sizes:
        out = master.resize((size, size), Image.Resampling.LANCZOS)
        out.save(EXPORTS / f"ShadowTeep-{size}.png")


def main():
    mask = text_mask()
    bg = gradient_background()
    shadow = make_shadow_layer(mask)
    highlight = make_highlight_layer(mask)
    type_layer = make_type_layer(mask)

    bg.save(SOURCE / "01-background.png")
    shadow.save(SOURCE / "02-steep-shadow.png")
    highlight.save(SOURCE / "03-blue-rim-highlight.png")
    type_layer.save(SOURCE / "04-ST-type.png")

    preview = bg.copy()
    for layer in (shadow, highlight, type_layer):
        preview.alpha_composite(layer)
    preview.putalpha(rounded_mask())
    preview.save(EXPORTS / "ShadowTeep-preview-1024.png")
    save_iconset(preview)


if __name__ == "__main__":
    main()
