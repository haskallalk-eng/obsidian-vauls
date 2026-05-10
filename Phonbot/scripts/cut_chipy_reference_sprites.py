from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


TRIPTYCH = Path(r"C:\Users\pc105\Downloads\ChatGPT Image 10. Mai 2026, 10_05_30.png")
OUT = Path(r"C:\Users\pc105\Obsidian\Phonbot\assets\mascot\sprites")


def alpha_from_luma(img: Image.Image, low: int = 5, high: int = 85) -> Image.Image:
    rgb = img.convert("RGB")
    alpha = Image.new("L", img.size, 0)
    ap = alpha.load()
    px = rgb.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            m = max(r, g, b)
            ap[x, y] = int(max(0, min(255, (m - low) / max(1, high - low) * 255)))
    return alpha


def make_cut(
    name: str,
    source: Image.Image,
    box: tuple[int, int, int, int],
    polygons: list[list[tuple[int, int]]],
    *,
    subtract: list[list[tuple[int, int]]] | None = None,
    low: int = 5,
    high: int = 85,
    feather: float = 1.2,
    inner_fill: bool = False,
) -> Image.Image:
    crop = source.crop(box).convert("RGBA")
    source_alpha = alpha_from_luma(crop, low, high)
    mask = Image.new("L", crop.size, 0)
    d = ImageDraw.Draw(mask)
    for polygon in polygons:
        d.polygon(polygon, fill=255)
    if subtract:
        for polygon in subtract:
            d.polygon(polygon, fill=0)
    if feather:
        mask = mask.filter(ImageFilter.GaussianBlur(feather))
    if inner_fill:
        alpha = Image.composite(Image.new("L", crop.size, 250), Image.new("L", crop.size, 0), mask)
    else:
        alpha = Image.composite(source_alpha, Image.new("L", crop.size, 0), mask)
    crop.putalpha(alpha)
    crop.save(OUT / f"{name}.png")
    checker = Image.new("RGBA", crop.size, (14, 18, 22, 255))
    cd = ImageDraw.Draw(checker)
    step = 20
    for y in range(0, crop.height, step):
        for x in range(0, crop.width, step):
            if (x // step + y // step) % 2 == 0:
                cd.rectangle((x, y, x + step - 1, y + step - 1), fill=(42, 50, 56, 255))
    checker.alpha_composite(crop)
    checker.convert("RGB").save(OUT / f"{name}-check.jpg", quality=95)
    return crop


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    trip = Image.open(TRIPTYCH).convert("RGB")

    make_cut(
        "chipy-body-clean",
        trip,
        (42, 315, 345, 900),
        [
            [
                (153, 12),
                (34, 112),
                (16, 330),
                (142, 484),
                (60, 575),
                (246, 575),
                (164, 484),
                (288, 330),
                (276, 112),
            ]
        ],
        inner_fill=True,
        feather=1.6,
    )

    make_cut(
        "chipy-logo-hair",
        trip,
        (118, 160, 305, 330),
        [[(4, 165), (22, 64), (83, 0), (183, 27), (183, 166)]],
        low=4,
        high=68,
        feather=1.2,
    )

    make_cut(
        "chipy-phone-hand-clean",
        trip,
        (820, 410, 1010, 835),
        [
            # Upper receiver cap and outer curve.
            [(13, 106), (43, 84), (94, 87), (126, 121), (121, 166), (60, 168), (21, 146)],
            # Main curved receiver body, kept away from the mascot body on the right.
            [(20, 143), (63, 150), (96, 196), (105, 270), (137, 343), (129, 414), (71, 416), (31, 319), (8, 225)],
            # Hand/fingers wrapped around receiver.
            [(28, 172), (116, 157), (151, 206), (143, 292), (62, 312), (8, 255)],
            # Lower receiver cap.
            [(80, 333), (154, 328), (184, 363), (168, 422), (100, 424), (68, 390)],
        ],
        subtract=[
            # Mascot body/face on the right side of the crop.
            [(129, 0), (190, 0), (190, 424), (152, 424), (149, 330), (119, 264), (118, 170), (128, 118)],
            # Eye and head remnant above the hand.
            [(112, 0), (190, 0), (190, 108), (126, 108)],
            # Lower orange body sliver.
            [(156, 285), (190, 285), (190, 424), (170, 424)],
            # Two remaining body shards near the phone, kept separate so the receiver is not clipped.
            [(121, 68), (152, 72), (147, 118), (126, 118)],
            [(144, 304), (180, 316), (180, 370), (158, 356)],
        ],
        low=4,
        high=78,
        feather=0.9,
    )

    make_cut(
        "chipy-calendar-hand-clean",
        trip,
        (1032, 500, 1248, 825),
        [
            # Calendar card and rings. Left edge starts after mascot body fragments.
            [(36, 37), (176, 54), (214, 104), (196, 252), (49, 253), (24, 204), (27, 87)],
            # Hand at lower right.
            [(124, 166), (216, 156), (216, 278), (158, 320), (80, 260)],
        ],
        subtract=[
            # Left mascot body/eye remnants.
            [(0, 0), (38, 0), (34, 325), (0, 325)],
            [(0, 0), (85, 0), (74, 38), (0, 42)],
            [(0, 248), (52, 250), (34, 325), (0, 325)],
        ],
        low=4,
        high=78,
        feather=0.9,
    )

    for p in OUT.glob("chipy-*.png"):
        print(p)


if __name__ == "__main__":
    main()
