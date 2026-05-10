from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


W, H = 1280, 720
FPS = 24
DURATION = 7.2
FRAMES = int(FPS * DURATION)

TRIPTYCH = Path(r"C:\Users\pc105\Downloads\ChatGPT Image 10. Mai 2026, 10_05_30.png")
HERO = Path(r"C:\Users\pc105\Downloads\ChatGPT Image 10. Mai 2026, 10_05_04.png")
OUT_DIR = Path(r"C:\Users\pc105\Obsidian\Phonbot\assets\video")
FRAME_DIR = Path(r"C:\Users\pc105\AppData\Local\Temp\chipy-reference-reveal-frames")
OUT_FILE = OUT_DIR / "chipy-reference-reveal-v8.mp4"

ORANGE = (249, 115, 22)
CYAN = (6, 182, 212)
ICE = (190, 250, 255)


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def smooth(v: float) -> float:
    v = clamp(v)
    return v * v * (3 - 2 * v)


def expo(v: float) -> float:
    v = clamp(v)
    return 1 if v == 1 else 1 - pow(2, -8 * v)


def back(v: float) -> float:
    v = clamp(v)
    c1 = 1.25
    c3 = c1 + 1
    return 1 + c3 * (v - 1) ** 3 + c1 * (v - 1) ** 2


def mix(a: float, b: float, p: float) -> float:
    return a + (b - a) * p


def alpha_from_luma(img: Image.Image, low: int = 7, high: int = 90) -> Image.Image:
    rgb = img.convert("RGB")
    alpha = Image.new("L", img.size, 0)
    ap = alpha.load()
    px = rgb.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            m = max(r, g, b)
            a = int(clamp((m - low) / max(1, high - low)) * 255)
            ap[x, y] = a
    return alpha


def make_sprite(
    src: Image.Image,
    box: tuple[int, int, int, int],
    *,
    polygon: list[tuple[int, int]] | None = None,
    luma_low: int = 7,
    luma_high: int = 88,
    contrast: float = 1.05,
    brightness: float = 1.0,
) -> Image.Image:
    crop = src.crop(box).convert("RGBA")
    crop = ImageEnhance.Contrast(crop).enhance(contrast)
    crop = ImageEnhance.Brightness(crop).enhance(brightness)
    alpha = alpha_from_luma(crop, luma_low, luma_high)
    if polygon:
        body = Image.new("L", crop.size, 0)
        ImageDraw.Draw(body).polygon(polygon, fill=245)
        alpha = Image.composite(Image.new("L", crop.size, 245), alpha, body)
    crop.putalpha(alpha)
    return crop


def resize_sprite(sprite: Image.Image, scale: float, sx: float = 1.0) -> Image.Image:
    w = max(2, int(sprite.width * scale * sx))
    h = max(2, int(sprite.height * scale))
    return sprite.resize((w, h), Image.Resampling.LANCZOS)


def intersect_alpha(sprite: Image.Image, polygons: list[list[tuple[int, int]]], feather: int = 2) -> Image.Image:
    mask = Image.new("L", sprite.size, 0)
    d = ImageDraw.Draw(mask)
    for polygon in polygons:
        d.polygon(polygon, fill=255)
    if feather > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(feather))
    alpha = Image.composite(sprite.getchannel("A"), Image.new("L", sprite.size, 0), mask)
    out = sprite.copy()
    out.putalpha(alpha)
    return out


def paste_center(base: Image.Image, sprite: Image.Image, cx: float, cy: float, opacity: float = 1.0, glow: bool = True) -> None:
    if opacity <= 0:
        return
    s = sprite.copy()
    if opacity < 0.999:
        a = s.getchannel("A").point(lambda p: int(p * opacity))
        s.putalpha(a)
    x = int(cx - s.width / 2)
    y = int(cy - s.height / 2)
    if glow:
        g = s.filter(ImageFilter.GaussianBlur(14))
        ga = g.getchannel("A").point(lambda p: int(p * 0.72))
        g.putalpha(ga)
        base.alpha_composite(g, (x, y))
    base.alpha_composite(s, (x, y))


def make_background() -> Image.Image:
    bg = Image.new("RGBA", (W, H), (1, 2, 4, 255))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay, "RGBA")
    for r in range(850, 80, -55):
        d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), outline=(13, 31, 35, 12), width=2)
    d.ellipse((260, 590, 655, 760), fill=(249, 115, 22, 30))
    d.ellipse((625, 590, 1020, 760), fill=(6, 182, 212, 28))
    overlay = overlay.filter(ImageFilter.GaussianBlur(16))
    bg.alpha_composite(overlay)
    bg.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 35)))
    bg.putalpha(255)
    return bg


def prep_sprites() -> dict[str, Image.Image]:
    trip = Image.open(TRIPTYCH).convert("RGB")
    hero = Image.open(HERO).convert("RGB")

    # Left panel of the triptych is the cleanest no-props body reference.
    body = make_sprite(
        trip,
        (42, 315, 345, 890),
        polygon=[(153, 13), (32, 113), (20, 333), (140, 485), (72, 568), (235, 568), (164, 485), (287, 333), (274, 113)],
        luma_low=5,
        luma_high=82,
        contrast=1.08,
        brightness=1.02,
    )
    hair = make_sprite(
        trip,
        (125, 170, 295, 330),
        luma_low=4,
        luma_high=70,
        contrast=1.15,
        brightness=1.08,
    )
    phone = make_sprite(
        trip,
        (835, 420, 1038, 830),
        luma_low=6,
        luma_high=82,
        contrast=1.12,
        brightness=1.04,
    )
    phone = intersect_alpha(
        phone,
        [
            # Full receiver arc and both handset ends.
            [(0, 82), (35, 70), (88, 72), (122, 112), (130, 175), (120, 238), (157, 318), (156, 406), (42, 406), (0, 275)],
            # Hand around the middle grip; keep the nice crystal fingers, not the body behind it.
            [(20, 145), (118, 130), (151, 184), (144, 266), (56, 285), (4, 236)],
        ],
        feather=3,
    )

    calendar = make_sprite(
        trip,
        (1040, 495, 1248, 820),
        luma_low=6,
        luma_high=82,
        contrast=1.1,
        brightness=1.04,
    )
    calendar = intersect_alpha(
        calendar,
        [
            # Calendar card including rings.
            [(28, 36), (174, 54), (205, 105), (188, 252), (42, 250), (14, 205), (16, 90)],
            # Holding hand on the lower right.
            [(113, 167), (208, 158), (208, 281), (151, 318), (78, 258)],
        ],
        feather=3,
    )

    return {"body": body, "hair": hair, "phone": phone, "calendar": calendar}


SPRITES = prep_sprites()
BACKGROUND = make_background()


def draw_light_sweep(base: Image.Image, t: float) -> None:
    p = smooth((t - 5.85) / 0.65) * (1 - smooth((t - 6.65) / 0.35))
    if p <= 0:
        return
    x = mix(W * 0.18, W * 0.83, p)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    a = int(160 * math.sin(math.pi * p))
    d.line((x - 60, 100, x + 60, 640), fill=(*ICE, a), width=3)
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(10)))
    base.alpha_composite(layer)


def render_frame(i: int) -> Image.Image:
    t = i / FPS
    frame = BACKGROUND.copy()

    intro = smooth(t / 0.5)
    spin = smooth(clamp((t - 0.45) / 2.2))
    lock = smooth((t - 2.35) / 0.5)
    theta = math.pi * 2.05 * spin
    sx = mix(0.22 + 0.78 * abs(math.cos(theta)), 1.0, lock)
    yrot_shift = math.sin(theta) * 28 * (1 - lock)
    body_scale = 0.94 + 0.025 * math.sin(t * 1.7)
    body = resize_sprite(SPRITES["body"], body_scale, sx)
    body_x = W * 0.5 + yrot_shift
    body_y = H * 0.555
    paste_center(frame, body, body_x, body_y, intro, glow=True)

    # Thin side edge during the most compressed turn makes the faux rotation read cleaner.
    if 0.7 < t < 2.35 and sx < 0.38:
        edge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(edge, "RGBA")
        x = body_x
        d.line((x, 150, x, 625), fill=(*CYAN, 190), width=4)
        d.line((x - 6, 175, x - 2, 610), fill=(*ORANGE, 130), width=2)
        frame.alpha_composite(edge.filter(ImageFilter.GaussianBlur(10)))
        frame.alpha_composite(edge)

    phone_p = back((t - 3.05) / 0.78)
    if phone_p > 0:
        s = resize_sprite(SPRITES["phone"], mix(0.55, 0.72, clamp(phone_p)))
        x = mix(-100, W * 0.35, clamp(phone_p))
        y = mix(H * 0.70, H * 0.50, clamp(phone_p))
        paste_center(frame, s, x, y, clamp(phone_p), glow=True)

    cal_p = back((t - 3.28) / 0.82)
    if cal_p > 0:
        s = resize_sprite(SPRITES["calendar"], mix(0.74, 0.96, clamp(cal_p)))
        x = mix(W + 140, W * 0.70, clamp(cal_p))
        y = mix(H * 0.73, H * 0.50, clamp(cal_p))
        paste_center(frame, s, x, y, clamp(cal_p), glow=True)

    hair_p = expo((t - 4.75) / 0.72)
    if hair_p > 0:
        s = resize_sprite(SPRITES["hair"], 0.93 * clamp(hair_p))
        x = W * 0.505
        y = mix(H * 0.24, H * 0.155, clamp(hair_p))
        paste_center(frame, s, x, y, clamp(hair_p), glow=True)

    draw_light_sweep(frame, t)

    fade_alpha = int(90 * (1 - intro))
    if fade_alpha > 0:
        frame.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, fade_alpha)))
    return frame.convert("RGB")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if FRAME_DIR.exists():
        shutil.rmtree(FRAME_DIR)
    FRAME_DIR.mkdir(parents=True)
    for i in range(FRAMES):
        render_frame(i).save(FRAME_DIR / f"frame_{i:04d}.jpg", quality=95, subsampling=0)
        if i % FPS == 0:
            print(f"rendered {i}/{FRAMES}")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(FRAME_DIR / "frame_%04d.jpg"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "16",
            "-movflags",
            "+faststart",
            str(OUT_FILE),
        ],
        check=True,
    )
    print(OUT_FILE)


if __name__ == "__main__":
    main()
