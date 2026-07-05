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
    "/Library/Fonts/SF-Compact-Display-Heavy.otf",
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
    img = Image.new("RGBA", (SIZE, SIZE), (8, 12, 18, 255))
    pix = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            nx = x / (SIZE - 1)
            ny = y / (SIZE - 1)
            upper_lift = max(0, 1 - (((nx - 0.38) ** 2 + (ny - 0.22) ** 2) ** 0.5) * 1.55)
            blue_wash = max(0, 1 - (((nx - 0.66) ** 2 + (ny - 0.48) ** 2) ** 0.5) * 1.6)
            green_floor = max(0, 1 - abs(ny - 0.82) * 5.2) * max(0, 1 - abs(nx - 0.56) * 1.7)
            r = int(8 + 12 * upper_lift + 3 * blue_wash + 2 * green_floor)
            g = int(12 + 18 * upper_lift + 30 * blue_wash + 42 * green_floor)
            b = int(18 + 28 * upper_lift + 58 * blue_wash + 28 * green_floor)
            pix[x, y] = (r, g, b, 255)

    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((54, 54, SIZE - 54, SIZE - 54), radius=208, outline=(219, 238, 255, 28), width=3)
    draw.rounded_rectangle((80, 80, SIZE - 80, SIZE - 80), radius=182, outline=(76, 154, 255, 24), width=2)
    draw.line((250, 790, 774, 790), fill=(76, 154, 255, 34), width=5)
    draw.line((318, 824, 706, 824), fill=(49, 215, 92, 38), width=4)
    return img


def text_mask():
    mask = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(mask)
    fnt = font(468)
    n_box = draw.textbbox((0, 0), "N", font=fnt)
    m_box = draw.textbbox((0, 0), "M", font=fnt)
    n_w = n_box[2] - n_box[0]
    m_w = m_box[2] - m_box[0]
    kern = -34
    total_w = n_w + m_w + kern
    x = (SIZE - total_w) // 2 - 2
    y = 268
    draw.text((x, y), "N", font=fnt, fill=255)
    draw.text((x + n_w + kern, y), "M", font=fnt, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.15))


def make_shadow_layer(mask):
    long_shadow = Image.new("L", (SIZE, SIZE), 0)
    for i in range(1, 68):
        shifted = ImageChops.offset(mask, i * 3, i * 4)
        opacity = max(0, 0.31 - i * 0.0039)
        long_shadow = ImageChops.lighter(long_shadow, shifted.point(lambda p, o=opacity: int(p * o)))
    long_shadow = long_shadow.filter(ImageFilter.GaussianBlur(8))

    soft = ImageChops.offset(mask, 20, 38).filter(ImageFilter.GaussianBlur(19))
    combined = ImageChops.lighter(long_shadow, soft.point(lambda p: int(p * 0.42)))
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    layer.alpha_composite(Image.composite(Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 172)), layer, combined))
    return layer


def make_highlight_layer(mask):
    rim = ImageChops.subtract(ImageChops.offset(mask, -5, -4), mask)
    rim = rim.filter(ImageFilter.GaussianBlur(1.2)).point(lambda p: min(160, int(p * 1.25)))

    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    layer.alpha_composite(Image.composite(Image.new("RGBA", (SIZE, SIZE), (76, 154, 255, 118)), layer, rim))

    draw = ImageDraw.Draw(layer, "RGBA")
    draw.rounded_rectangle((670, 704, 748, 728), radius=12, fill=(49, 215, 92, 74))
    draw.ellipse((736, 694, 764, 722), fill=(49, 215, 92, 62))
    return layer


def make_type_layer(mask):
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    fill = Image.new("RGBA", (SIZE, SIZE), (246, 248, 244, 255))
    layer.alpha_composite(Image.composite(fill, layer, mask))

    top = ImageChops.subtract(mask, ImageChops.offset(mask, 0, 9)).filter(ImageFilter.GaussianBlur(0.8))
    layer.alpha_composite(
        Image.composite(
            Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 42)),
            Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0)),
            top,
        )
    )
    return layer


def save_sizes(master, prefix, out_dir):
    out_dir.mkdir(exist_ok=True)
    for size in [16, 20, 29, 32, 40, 58, 60, 64, 76, 80, 87, 120, 128, 152, 167, 180, 256, 512, 1024]:
        master.resize((size, size), Image.Resampling.LANCZOS).save(out_dir / f"{prefix}-{size}.png")


def main():
    mask = text_mask()
    background = gradient_background()
    shadow = make_shadow_layer(mask)
    highlight = make_highlight_layer(mask)
    type_layer = make_type_layer(mask)

    background.save(SOURCE / "01-background.png")
    shadow.save(SOURCE / "02-mobile-shadow.png")
    highlight.save(SOURCE / "03-blue-green-highlight.png")
    type_layer.save(SOURCE / "04-NM-type.png")

    preview = background.copy()
    for layer in (shadow, highlight, type_layer):
        preview.alpha_composite(layer)
    preview.putalpha(rounded_mask())
    preview.save(EXPORTS / "NativeMobile-preview-1024.png")
    save_sizes(preview, "NativeMobile", EXPORTS / "RawSized")


if __name__ == "__main__":
    main()
