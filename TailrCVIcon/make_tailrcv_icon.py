from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
VARIANT = ROOT / "HopeWhite"
SOURCE = VARIANT / "SourceLayers"
EXPORTS = VARIANT / "Exports"
ICON_SIZED = EXPORTS / "IconComposerSized"
RAW_SIZED = EXPORTS / "RawSized"

for directory in (SOURCE, EXPORTS, ICON_SIZED, RAW_SIZED):
    directory.mkdir(parents=True, exist_ok=True)

SIZE = 1024
WATCH_SIZE = 1088
SIZES = [16, 20, 29, 32, 40, 58, 60, 64, 76, 80, 87, 120, 128, 152, 167, 180, 256, 512, 1024]

FONT_PATHS = [
    "/Library/Fonts/SF-Pro-Display-Heavy.otf",
    "/Library/Fonts/SF-Pro-Display-Black.otf",
    "/Library/Fonts/SF-Pro-Display-Bold.otf",
    "/System/Library/Fonts/SFNS.ttf",
]

COLORS = {
    "ink": (24, 42, 71, 255),
    "blue": (36, 107, 254, 255),
    "blue_soft": (80, 139, 255, 255),
    "amber": (255, 181, 64, 255),
    "amber_deep": (255, 145, 58, 255),
    "paper": (255, 255, 255, 255),
    "paper_edge": (231, 238, 250, 255),
}


def font(size):
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default(size=size)


def new_layer():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def rounded_mask(size=SIZE, radius=232):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size, size), radius=radius, fill=255)
    return mask


def background_layer():
    img = Image.new("RGBA", (SIZE, SIZE), COLORS["paper"])
    pix = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            nx = x / (SIZE - 1)
            ny = y / (SIZE - 1)
            blue_lift = max(0, 1 - (((nx - 0.52) ** 2 + (ny - 0.35) ** 2) ** 0.5) * 1.75)
            amber_lift = max(0, 1 - (((nx - 0.36) ** 2 + (ny - 0.78) ** 2) ** 0.5) * 2.05)
            r = int(255 - 14 * blue_lift)
            g = int(255 - 7 * blue_lift - 10 * amber_lift)
            b = int(255 - 2 * amber_lift)
            pix[x, y] = (r, g, b, 255)

    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((54, 54, SIZE - 54, SIZE - 54), radius=208, outline=(36, 107, 254, 30), width=3)
    draw.rounded_rectangle((82, 82, SIZE - 82, SIZE - 82), radius=180, outline=(255, 181, 64, 28), width=2)
    return img


def hope_accent_layer():
    layer = new_layer()
    draw = ImageDraw.Draw(layer, "RGBA")

    # Sunrise/horizon cue: hope without turning the icon into a landscape.
    draw.pieslice((194, 630, 830, 1266), start=180, end=360, fill=(255, 181, 64, 86))
    draw.arc((214, 650, 810, 1246), start=181, end=359, fill=(255, 145, 58, 130), width=24)
    draw.arc((282, 704, 742, 1164), start=181, end=359, fill=(255, 181, 64, 94), width=12)
    draw.rounded_rectangle((238, 772, 786, 800), radius=14, fill=(255, 181, 64, 88))
    draw.rounded_rectangle((320, 818, 704, 834), radius=8, fill=(36, 107, 254, 42))

    glow = layer.filter(ImageFilter.GaussianBlur(18))
    glow.alpha_composite(layer)
    return glow


def document_layer():
    layer = new_layer()
    draw = ImageDraw.Draw(layer, "RGBA")

    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow, "RGBA")
    shadow_draw.rounded_rectangle((238, 176, 786, 840), radius=56, fill=(11, 34, 74, 42))
    shadow = ImageChops.offset(shadow, 0, 18).filter(ImageFilter.GaussianBlur(18))
    layer.alpha_composite(shadow)

    draw.rounded_rectangle((230, 156, 778, 820), radius=56, fill=(255, 255, 255, 236), outline=(210, 222, 244, 190), width=4)
    draw.polygon((666, 156, 778, 268, 666, 268), fill=(230, 238, 252, 230))
    draw.line((668, 158, 668, 268), fill=(190, 207, 236, 154), width=3)
    draw.line((666, 268, 778, 268), fill=(190, 207, 236, 120), width=3)

    for y, width, alpha in ((332, 278, 94), (382, 332, 78), (432, 244, 66)):
        draw.rounded_rectangle((346, y, 346 + width, y + 18), radius=9, fill=(36, 107, 254, alpha))

    return layer


def text_mask():
    mask = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(mask)
    fnt = font(414)
    c_box = draw.textbbox((0, 0), "C", font=fnt)
    v_box = draw.textbbox((0, 0), "V", font=fnt)
    c_w = c_box[2] - c_box[0]
    v_w = v_box[2] - v_box[0]
    kern = -24
    total_w = c_w + v_w + kern
    x = (SIZE - total_w) // 2 - 2
    y = 360
    draw.text((x, y), "C", font=fnt, fill=255)
    draw.text((x + c_w + kern, y), "V", font=fnt, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.12))


def type_shadow_layer(mask):
    long_shadow = Image.new("L", (SIZE, SIZE), 0)
    for i in range(1, 42):
        shifted = ImageChops.offset(mask, i * 2, i * 3)
        opacity = max(0, 0.18 - i * 0.0033)
        long_shadow = ImageChops.lighter(long_shadow, shifted.point(lambda p, o=opacity: int(p * o)))
    long_shadow = long_shadow.filter(ImageFilter.GaussianBlur(7))

    layer = new_layer()
    layer.alpha_composite(Image.composite(Image.new("RGBA", (SIZE, SIZE), (12, 29, 62, 138)), layer, long_shadow))
    return layer


def type_layer(mask):
    layer = new_layer()

    fill = Image.new("RGBA", (SIZE, SIZE), COLORS["ink"])
    blue_rim = ImageChops.subtract(ImageChops.offset(mask, -5, -4), mask)
    amber_rim = ImageChops.subtract(ImageChops.offset(mask, 5, 4), mask)

    layer.alpha_composite(Image.composite(fill, layer, mask))
    layer.alpha_composite(
        Image.composite(
            Image.new("RGBA", (SIZE, SIZE), (36, 107, 254, 112)),
            Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0)),
            blue_rim.filter(ImageFilter.GaussianBlur(1.1)),
        )
    )
    layer.alpha_composite(
        Image.composite(
            Image.new("RGBA", (SIZE, SIZE), (255, 181, 64, 92)),
            Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0)),
            amber_rim.filter(ImageFilter.GaussianBlur(1.4)),
        )
    )
    return layer


def glass_highlights_layer(mask):
    layer = new_layer()

    top = ImageChops.subtract(mask, ImageChops.offset(mask, 0, 8)).filter(ImageFilter.GaussianBlur(0.9))
    layer.alpha_composite(
        Image.composite(
            Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 68)),
            Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0)),
            top,
        )
    )
    return layer


def flatten_opaque(img):
    flattened = Image.new("RGBA", img.size, COLORS["paper"])
    flattened.alpha_composite(img)
    return flattened.convert("RGB")


def save_sizes(master, prefix, out_dir):
    out_dir.mkdir(exist_ok=True)
    for size in SIZES:
        master.resize((size, size), Image.Resampling.LANCZOS).save(out_dir / f"{prefix}-{size}.png")


def contact_sheet(master, path):
    sizes = [16, 20, 29, 32, 40, 64, 128, 256]
    cell = 160
    sheet = Image.new("RGB", (cell * 4, cell * 2), (248, 250, 252))
    draw = ImageDraw.Draw(sheet)
    label_font = font(18)
    for idx, size in enumerate(sizes):
        x = (idx % 4) * cell
        y = (idx // 4) * cell
        icon = master.resize((size, size), Image.Resampling.LANCZOS)
        sheet.paste(icon, (x + (cell - size) // 2, y + 34), icon if icon.mode == "RGBA" else None)
        draw.text((x + 12, y + 10), f"{size}px", fill=(76, 88, 112), font=label_font)
    sheet.save(path)


def watch_master(master):
    watch = Image.new("RGBA", (WATCH_SIZE, WATCH_SIZE), COLORS["paper"])
    scaled = master.resize((WATCH_SIZE, WATCH_SIZE), Image.Resampling.LANCZOS)
    watch.alpha_composite(scaled)
    return watch.convert("RGB")


def main():
    mask = text_mask()
    layers = [
        ("01-white-hope-background.png", background_layer()),
        ("02-sunrise-hope-accent.png", hope_accent_layer()),
        ("03-tailored-cv-document.png", document_layer()),
        ("04-CV-type-shadow.png", type_shadow_layer(mask)),
        ("05-CV-typography.png", type_layer(mask)),
        ("06-glass-highlights.png", glass_highlights_layer(mask)),
    ]

    for name, layer in layers:
        layer.save(SOURCE / name)

    preview = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    for _, layer in layers:
        preview.alpha_composite(layer)

    opaque_preview = flatten_opaque(preview)
    opaque_preview.save(EXPORTS / "TailrCV-HopeWhite-preview-1024.png")
    opaque_preview.save(SOURCE / "TailrCV-HopeWhite-IconComposer-iOS-macOS-Default-1024.png")
    opaque_preview.save(SOURCE / "TailrCV-HopeWhite-AppStore-1024-opaque.png")
    watch_master(preview).save(SOURCE / "TailrCV-HopeWhite-IconComposer-watchOS-Default-1088.png")

    save_sizes(opaque_preview, "TailrCV-HopeWhite-IconComposer", ICON_SIZED)
    save_sizes(opaque_preview, "TailrCV-HopeWhite-Raw", RAW_SIZED)
    contact_sheet(opaque_preview, EXPORTS / "TailrCV-HopeWhite-contact-sheet.png")


if __name__ == "__main__":
    main()
