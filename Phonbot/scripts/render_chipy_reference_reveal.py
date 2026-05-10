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
OUT_FILE = OUT_DIR / "chipy-reference-reveal-v3.mp4"

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
    d = ImageDraw.Draw(bg, "RGBA")
    for r in range(850, 80, -55):
        d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), outline=(13, 31, 35, 12), width=2)
    d.ellipse((230, 565, 705, 760), fill=(249, 115, 22, 58))
    d.ellipse((585, 565, 1060, 760), fill=(6, 182, 212, 55))
    d.rectangle((0, 0, W, H), fill=(0, 0, 0, 35))
    return bg


def prep_sprites() -> dict[str, Image.Image]:
    trip = Image.open(TRIPTYCH).convert("RGB")
    hero = Image.open(HERO).convert("RGB")

    # Left panel of the triptych is the cleanest no-props body reference.
    body = make_sprite(
        trip,
        (42, 288, 345, 982),
        polygon=[(153, 40), (32, 140), (20, 360), (140, 512), (30, 650), (154, 690), (276, 650), (164, 512), (287, 360), (274, 140)],
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
        hero,
        (210, 500, 455, 935),
        luma_low=6,
        luma_high=82,
        contrast=1.12,
        brightness=1.04,
    )
    calendar = make_sprite(
        hero,
        (720, 505, 1068, 902),
        luma_low=6,
        luma_high=82,
        contrast=1.1,
        brightness=1.04,
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
    body_scale = 0.83 + 0.025 * math.sin(t * 1.7)
    body = resize_sprite(SPRITES["body"], body_scale, sx)
    body_x = W * 0.5 + yrot_shift
    body_y = H * 0.535
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
        s = resize_sprite(SPRITES["phone"], mix(0.43, 0.53, clamp(phone_p)))
        x = mix(-100, W * 0.335, clamp(phone_p))
        y = mix(H * 0.70, H * 0.535, clamp(phone_p))
        paste_center(frame, s, x, y, clamp(phone_p), glow=True)

    cal_p = back((t - 3.28) / 0.82)
    if cal_p > 0:
        s = resize_sprite(SPRITES["calendar"], mix(0.37, 0.49, clamp(cal_p)))
        x = mix(W + 140, W * 0.715, clamp(cal_p))
        y = mix(H * 0.73, H * 0.535, clamp(cal_p))
        paste_center(frame, s, x, y, clamp(cal_p), glow=True)

    hair_p = expo((t - 4.75) / 0.72)
    if hair_p > 0:
        s = resize_sprite(SPRITES["hair"], 0.93 * clamp(hair_p))
        x = W * 0.505
        y = mix(H * 0.24, H * 0.172, clamp(hair_p))
        paste_center(frame, s, x, y, clamp(hair_p), glow=True)

    draw_light_sweep(frame, t)

    d = ImageDraw.Draw(frame, "RGBA")
    d.rectangle((0, 0, W, H), fill=(0, 0, 0, int(90 * (1 - intro))))
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
