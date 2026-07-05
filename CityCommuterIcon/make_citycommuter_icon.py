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
    img = Image.new("RGBA", (SIZE, SIZE), (4, 15, 18, 255))
    pix = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            nx = x / (SIZE - 1)
            ny = y / (SIZE - 1)
            center_lift = max(0, 1 - (((nx - 0.48) ** 2 + (ny - 0.38) ** 2) ** 0.5) * 1.55)
            lower_glow = max(0, 1 - abs(ny - 0.84) * 5.8) * max(0, 1 - abs(nx - 0.5) * 1.35)
            r = int(5 + 10 * center_lift + 8 * lower_glow)
            g = int(17 + 34 * center_lift + 40 * lower_glow)
            b = int(22 + 45 * center_lift + 55 * lower_glow)
            pix[x, y] = (r, g, b, 255)

    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((54, 54, SIZE - 54, SIZE - 54), radius=208, outline=(226, 255, 247, 28), width=3)
    draw.rounded_rectangle((80, 80, SIZE - 80, SIZE - 80), radius=182, outline=(94, 234, 212, 22), width=2)
    draw.line((210, 780, 814, 780), fill=(255, 207, 90, 38), width=5)
    draw.line((246, 812, 778, 812), fill=(94, 234, 212, 32), width=3)
    return img


def text_mask():
    mask = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(mask)
    fnt = font(514)
    bbox = draw.textbbox((0, 0), "C", font=fnt)
    c_w = bbox[2] - bbox[0]
    kern = -70
    total_w = c_w * 2 + kern
    x = (SIZE - total_w) // 2 + 4
    y = 246
    draw.text((x, y), "C", font=fnt, fill=255)
    draw.text((x + c_w + kern, y), "C", font=fnt, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.15))


def make_shadow_layer(mask):
    long_shadow = Image.new("L", (SIZE, SIZE), 0)
    for i in range(1, 62):
        shifted = ImageChops.offset(mask, i * 3, i * 4)
        opacity = max(0, 0.28 - i * 0.0038)
        long_shadow = ImageChops.lighter(long_shadow, shifted.point(lambda p, o=opacity: int(p * o)))
    long_shadow = long_shadow.filter(ImageFilter.GaussianBlur(8))

    soft = ImageChops.offset(mask, 18, 36).filter(ImageFilter.GaussianBlur(18))
    combined = ImageChops.lighter(long_shadow, soft.point(lambda p: int(p * 0.36)))
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    layer.alpha_composite(Image.composite(Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 160)), layer, combined))
    return layer


def make_highlight_layer(mask):
    rim = ImageChops.subtract(ImageChops.offset(mask, -5, -4), mask)
    rim = rim.filter(ImageFilter.GaussianBlur(1.2)).point(lambda p: min(160, int(p * 1.25)))

    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    layer.alpha_composite(Image.composite(Image.new("RGBA", (SIZE, SIZE), (94, 234, 212, 112)), layer, rim))

    draw = ImageDraw.Draw(layer, "RGBA")
    draw.rounded_rectangle((704, 704, 770, 726), radius=11, fill=(255, 207, 90, 66))
    return layer


def make_type_layer(mask):
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    fill = Image.new("RGBA", (SIZE, SIZE), (245, 249, 244, 255))
    layer.alpha_composite(Image.composite(fill, layer, mask))

    top = ImageChops.subtract(mask, ImageChops.offset(mask, 0, 9)).filter(ImageFilter.GaussianBlur(0.8))
    layer.alpha_composite(Image.composite(Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 42)), Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0)), top))
    return layer


def save_sizes(master):
    out_dir = EXPORTS / "RawSized"
    out_dir.mkdir(exist_ok=True)
    for size in [16, 20, 29, 32, 40, 58, 60, 64, 76, 80, 87, 120, 128, 152, 167, 180, 256, 512, 1024]:
        master.resize((size, size), Image.Resampling.LANCZOS).save(out_dir / f"CityCommuter-{size}.png")


def main():
    mask = text_mask()
    background = gradient_background()
    shadow = make_shadow_layer(mask)
    highlight = make_highlight_layer(mask)
    type_layer = make_type_layer(mask)

    background.save(SOURCE / "01-background.png")
    shadow.save(SOURCE / "02-commuter-shadow.png")
    highlight.save(SOURCE / "03-mint-amber-highlight.png")
    type_layer.save(SOURCE / "04-CC-type.png")

    preview = background.copy()
    for layer in (shadow, highlight, type_layer):
        preview.alpha_composite(layer)
    preview.putalpha(rounded_mask())
    preview.save(EXPORTS / "CityCommuter-preview-1024.png")
    save_sizes(preview)


if __name__ == "__main__":
    main()
