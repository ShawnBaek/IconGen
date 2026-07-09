from pathlib import Path
from io import BytesIO
import json
import shutil
import subprocess

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
VARIANT = ROOT / "HopeWhite"
SOURCE = VARIANT / "SourceLayers"
EXPORTS = VARIANT / "Exports"
ICON_SIZED = EXPORTS / "IconComposerSized"
RAW_SIZED = EXPORTS / "RawSized"
APPEARANCE = EXPORTS / "AppearanceVariants"
MACOS_APPICON = EXPORTS / "MacOSAppIcon.appiconset"
ICON_PACKAGE = SOURCE / "TailrCV-HopeWhite.icon"

for directory in (SOURCE, EXPORTS, ICON_SIZED, RAW_SIZED, APPEARANCE, MACOS_APPICON):
    directory.mkdir(parents=True, exist_ok=True)

SIZE = 1024
WATCH_SIZE = 1088
SIZES = [16, 20, 29, 32, 40, 58, 60, 64, 76, 80, 87, 120, 128, 152, 167, 180, 256, 512, 1024]
MACOS_ICON_SLOTS = [16, 32, 128, 256, 512]

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
    "dark_bg": (6, 15, 30, 255),
    "dark_ink": (242, 247, 255, 255),
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


def background_layer(mode="default"):
    if mode == "dark":
        img = Image.new("RGBA", (SIZE, SIZE), COLORS["dark_bg"])
        pix = img.load()
        for y in range(SIZE):
            for x in range(SIZE):
                nx = x / (SIZE - 1)
                ny = y / (SIZE - 1)
                blue_lift = max(0, 1 - (((nx - 0.54) ** 2 + (ny - 0.36) ** 2) ** 0.5) * 1.65)
                amber_lift = max(0, 1 - (((nx - 0.36) ** 2 + (ny - 0.80) ** 2) ** 0.5) * 2.2)
                r = int(6 + 18 * blue_lift + 18 * amber_lift)
                g = int(15 + 32 * blue_lift + 15 * amber_lift)
                b = int(30 + 64 * blue_lift + 4 * amber_lift)
                pix[x, y] = (r, g, b, 255)

        draw = ImageDraw.Draw(img, "RGBA")
        draw.rounded_rectangle((18, 18, SIZE - 18, SIZE - 18), radius=242, outline=(114, 168, 255, 82), width=8)
        draw.rounded_rectangle((46, 46, SIZE - 46, SIZE - 46), radius=218, outline=(255, 181, 64, 58), width=4)
        return img

    img = Image.new("RGBA", (SIZE, SIZE), COLORS["paper"])
    pix = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            nx = x / (SIZE - 1)
            ny = y / (SIZE - 1)
            blue_lift = max(0, 1 - (((nx - 0.52) ** 2 + (ny - 0.35) ** 2) ** 0.5) * 1.62)
            amber_lift = max(0, 1 - (((nx - 0.36) ** 2 + (ny - 0.78) ** 2) ** 0.5) * 1.9)
            edge_lift = max(0, min(nx, ny, 1 - nx, 1 - ny))
            edge_lift = 1 - min(1, edge_lift / 0.18)
            r = int(255 - 18 * blue_lift - 2 * edge_lift)
            g = int(255 - 10 * blue_lift - 12 * amber_lift - 4 * edge_lift)
            b = int(255 - 2 * amber_lift - 9 * edge_lift)
            pix[x, y] = (r, g, b, 255)

    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((18, 18, SIZE - 18, SIZE - 18), radius=242, outline=(36, 107, 254, 72), width=8)
    draw.rounded_rectangle((46, 46, SIZE - 46, SIZE - 46), radius=218, outline=(255, 181, 64, 50), width=4)
    draw.rounded_rectangle((72, 72, SIZE - 72, SIZE - 72), radius=194, outline=(36, 107, 254, 22), width=2)
    return img


def hope_accent_layer(mode="default"):
    layer = new_layer()
    draw = ImageDraw.Draw(layer, "RGBA")
    boost = 1.28 if mode == "dark" else 1.0

    def alpha(value):
        return min(190, int(value * boost))

    # Sunrise/horizon cue: hope without turning the icon into a landscape.
    draw.pieslice((124, 604, 900, 1380), start=180, end=360, fill=(255, 181, 64, alpha(96)))
    draw.arc((144, 624, 880, 1360), start=181, end=359, fill=(255, 145, 58, alpha(144)), width=30)
    draw.arc((240, 706, 784, 1250), start=181, end=359, fill=(255, 181, 64, alpha(102)), width=15)
    draw.rounded_rectangle((196, 790, 828, 824), radius=17, fill=(255, 181, 64, alpha(92)))
    draw.rounded_rectangle((292, 848, 732, 866), radius=9, fill=(80, 139, 255, alpha(46)))

    glow = layer.filter(ImageFilter.GaussianBlur(18))
    glow.alpha_composite(layer)
    return glow


def sf_symbol_image(symbol_name, size):
    try:
        import AppKit
    except Exception:
        return None

    symbol = AppKit.NSImage.imageWithSystemSymbolName_accessibilityDescription_(symbol_name, None)
    if symbol is None:
        return None

    symbol.setSize_((size, size))
    data = symbol.TIFFRepresentation()
    if data is None:
        return None

    return Image.open(BytesIO(bytes(data))).convert("RGBA")


def tint_symbol(symbol, color):
    alpha = symbol.getchannel("A")
    tinted = Image.new("RGBA", symbol.size, color)
    tinted.putalpha(alpha)
    return tinted


def symbol_document_layer(mode="default"):
    symbol = sf_symbol_image("doc.text.fill", 620)
    if symbol is None:
        return fallback_document_layer()

    bbox = symbol.getbbox()
    if bbox is None:
        return fallback_document_layer()

    symbol = symbol.crop(bbox)
    target_h = 720
    target_w = int(symbol.width * (target_h / symbol.height))
    if target_w > 650:
        target_w = 650
        target_h = int(symbol.height * (target_w / symbol.width))
    symbol = symbol.resize((target_w, target_h), Image.Resampling.LANCZOS)
    symbol_fill = (255, 255, 255, 238) if mode != "dark" else (28, 47, 80, 212)
    symbol = tint_symbol(symbol, symbol_fill)
    symbol_alpha = symbol.getchannel("A")
    outline_alpha = symbol_alpha.filter(ImageFilter.MaxFilter(13))
    outline_alpha = ImageChops.subtract(outline_alpha, symbol_alpha).filter(ImageFilter.GaussianBlur(0.8))
    outline_color = (198, 215, 242, 170) if mode != "dark" else (116, 166, 255, 164)
    outline = Image.new("RGBA", symbol.size, outline_color)
    outline.putalpha(outline_alpha)

    layer = new_layer()
    draw = ImageDraw.Draw(layer, "RGBA")

    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow, "RGBA")
    x = (SIZE - symbol.width) // 2
    y = 112
    shadow_fill = (11, 34, 74, 44) if mode != "dark" else (0, 0, 0, 44)
    shadow_draw.rounded_rectangle((x + 12, y + 18, x + symbol.width - 12, y + symbol.height - 8), radius=58, fill=shadow_fill)
    shadow = ImageChops.offset(shadow, 0, 18).filter(ImageFilter.GaussianBlur(18))
    layer.alpha_composite(shadow)

    layer.alpha_composite(outline, (x, y))
    layer.alpha_composite(symbol, (x, y))

    # Quiet Apple-blue text lines inside the SF Symbol document.
    line_color = (36, 107, 254) if mode != "dark" else (142, 188, 255)
    alpha_scale = 1 if mode != "dark" else 1.45
    for line_y, width, alpha in ((306, 318, 96), (360, 374, 82), (414, 282, 70)):
        draw.rounded_rectangle((326, line_y, 326 + width, line_y + 20), radius=10, fill=(*line_color, min(190, int(alpha * alpha_scale))))

    return layer


def fallback_document_layer():
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
    fnt = font(486)
    c_box = draw.textbbox((0, 0), "C", font=fnt)
    v_box = draw.textbbox((0, 0), "V", font=fnt)
    c_w = c_box[2] - c_box[0]
    v_w = v_box[2] - v_box[0]
    kern = -28
    total_w = c_w + v_w + kern
    x = (SIZE - total_w) // 2 - 4
    y = 326
    draw.text((x, y), "C", font=fnt, fill=255)
    draw.text((x + c_w + kern, y), "V", font=fnt, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.12))


def type_shadow_layer(mask, mode="default"):
    long_shadow = Image.new("L", (SIZE, SIZE), 0)
    for i in range(1, 42):
        shifted = ImageChops.offset(mask, i * 2, i * 3)
        opacity = max(0, 0.18 - i * 0.0033)
        long_shadow = ImageChops.lighter(long_shadow, shifted.point(lambda p, o=opacity: int(p * o)))
    long_shadow = long_shadow.filter(ImageFilter.GaussianBlur(7))

    layer = new_layer()
    shadow_color = (12, 29, 62, 138) if mode != "dark" else (0, 0, 0, 190)
    layer.alpha_composite(Image.composite(Image.new("RGBA", (SIZE, SIZE), shadow_color), layer, long_shadow))
    return layer


def type_layer(mask, mode="default"):
    layer = new_layer()

    fill_color = COLORS["ink"] if mode != "dark" else COLORS["dark_ink"]
    fill = Image.new("RGBA", (SIZE, SIZE), fill_color)
    blue_rim = ImageChops.subtract(ImageChops.offset(mask, -5, -4), mask)
    amber_rim = ImageChops.subtract(ImageChops.offset(mask, 5, 4), mask)

    layer.alpha_composite(Image.composite(fill, layer, mask))
    layer.alpha_composite(
        Image.composite(
            Image.new("RGBA", (SIZE, SIZE), (36, 107, 254, 132 if mode == "dark" else 112)),
            Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0)),
            blue_rim.filter(ImageFilter.GaussianBlur(1.1)),
        )
    )
    layer.alpha_composite(
        Image.composite(
            Image.new("RGBA", (SIZE, SIZE), (255, 181, 64, 122 if mode == "dark" else 92)),
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


def flatten_on(img, background):
    flattened = Image.new("RGBA", img.size, background)
    flattened.alpha_composite(img)
    return flattened.convert("RGB")


def save_sizes(master, prefix, out_dir):
    out_dir.mkdir(exist_ok=True)
    for size in SIZES:
        master.resize((size, size), Image.Resampling.LANCZOS).save(out_dir / f"{prefix}-{size}.png")


def write_macos_app_icon_set(master, out_dir):
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    images = []
    for base in MACOS_ICON_SLOTS:
        for scale, suffix in ((1, ""), (2, "@2x")):
            pixel_size = base * scale
            filename = f"icon_{base}x{base}{suffix}.png"
            master.resize((pixel_size, pixel_size), Image.Resampling.LANCZOS).save(out_dir / filename)
            images.append(
                {
                    "filename": filename,
                    "idiom": "mac",
                    "scale": f"{scale}x",
                    "size": f"{base}x{base}",
                }
            )

    contents = {
        "images": images,
        "info": {
            "author": "xcode",
            "version": 1,
        },
    }
    (out_dir / "Contents.json").write_text(json.dumps(contents, indent=2) + "\n")


def write_macos_icns(app_icon_set, output_path):
    iconset = output_path.with_suffix(".iconset")
    if iconset.exists():
        shutil.rmtree(iconset)
    iconset.mkdir(parents=True)

    for source in app_icon_set.glob("icon_*.png"):
        shutil.copy2(source, iconset / source.name)

    subprocess.run(["iconutil", "-c", "icns", str(iconset), "-o", str(output_path)], check=True)
    shutil.rmtree(iconset)


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


def compose(mode="default"):
    mask = text_mask()
    layers = [
        ("01-white-hope-background.png", background_layer(mode)),
        ("02-sunrise-hope-accent.png", hope_accent_layer(mode)),
        ("03-sf-doc-text-symbol.png", symbol_document_layer(mode)),
        ("04-CV-type-shadow.png", type_shadow_layer(mask, mode)),
        ("05-CV-typography.png", type_layer(mask, mode)),
        ("06-glass-highlights.png", glass_highlights_layer(mask)),
    ]

    preview = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    for _, layer in layers:
        preview.alpha_composite(layer)
    return layers, preview


def mono_variant(master):
    gray = master.convert("L")
    return Image.merge("RGB", (gray, gray, gray))


def tinted_grayscale_variant(master):
    gray = master.convert("L")
    toned = Image.new("RGB", master.size)
    pix_in = gray.load()
    pix_out = toned.load()
    for y in range(master.height):
        for x in range(master.width):
            value = pix_in[x, y]
            # Preserve grayscale for Icon Composer tinted/mono input, with slightly lifted contrast.
            lifted = max(0, min(255, int((value - 16) * 1.08 + 16)))
            pix_out[x, y] = (lifted, lifted, lifted)
    return toned


def write_icon_package(layer_names):
    if ICON_PACKAGE.exists():
        shutil.rmtree(ICON_PACKAGE)
    assets = ICON_PACKAGE / "Assets"
    assets.mkdir(parents=True)
    for name in layer_names:
        shutil.copy2(SOURCE / name, assets / name)

    # Icon Composer packages are folders with icon.json and an Assets directory.
    # This baseline package opens in Icon Composer; use the inspector there for
    # per-appearance Liquid Glass tuning, then export with ictool or the GUI.
    data = {
        "groups": [
            {
                "layers": [
                    {"image-name": name, "name": Path(name).stem}
                    for name in reversed(layer_names)
                ],
                "shadow": {"kind": "neutral", "opacity": 0.42},
                "translucency": {"enabled": True, "value": 0.16},
            }
        ],
        "supported-platforms": {
            "circles": ["watchOS"],
            "squares": "shared",
        },
    }
    (ICON_PACKAGE / "icon.json").write_text(json.dumps(data, indent=2) + "\n")


def main():
    layers, preview = compose("default")
    for name, layer in layers:
        layer.save(SOURCE / name)

    opaque_preview = flatten_opaque(preview)
    opaque_preview.save(EXPORTS / "TailrCV-HopeWhite-preview-1024.png")
    opaque_preview.save(SOURCE / "TailrCV-HopeWhite-IconComposer-iOS-macOS-Default-1024.png")
    opaque_preview.save(SOURCE / "TailrCV-HopeWhite-AppStore-1024-opaque.png")
    watch_master(preview).save(SOURCE / "TailrCV-HopeWhite-IconComposer-watchOS-Default-1088.png")

    _, dark_preview = compose("dark")
    dark = flatten_on(dark_preview, COLORS["dark_bg"])
    dark.save(APPEARANCE / "TailrCV-HopeWhite-IconComposer-iOS-macOS-Dark-1024.png")
    mono_variant(opaque_preview).save(APPEARANCE / "TailrCV-HopeWhite-IconComposer-iOS-macOS-Mono-1024.png")
    tinted_grayscale_variant(opaque_preview).save(APPEARANCE / "TailrCV-HopeWhite-IconComposer-iOS-macOS-Tinted-Grayscale-1024.png")

    save_sizes(opaque_preview, "TailrCV-HopeWhite-IconComposer", ICON_SIZED)
    save_sizes(opaque_preview, "TailrCV-HopeWhite-Raw", RAW_SIZED)
    write_macos_app_icon_set(opaque_preview, MACOS_APPICON)
    write_macos_icns(MACOS_APPICON, EXPORTS / "TailrCV-HopeWhite-AppIcon.icns")
    contact_sheet(opaque_preview, EXPORTS / "TailrCV-HopeWhite-contact-sheet.png")
    contact_sheet(dark, APPEARANCE / "TailrCV-HopeWhite-Dark-contact-sheet.png")
    contact_sheet(mono_variant(opaque_preview), APPEARANCE / "TailrCV-HopeWhite-Mono-contact-sheet.png")
    write_icon_package([name for name, _ in layers])


if __name__ == "__main__":
    main()
