from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


W, H = 1280, 720
FPS = 24
DURATION = 7.0
FRAMES = int(FPS * DURATION)
OUT_DIR = Path(r"C:\Users\pc105\Obsidian\Phonbot\assets\video")
FRAME_DIR = Path(r"C:\Users\pc105\AppData\Local\Temp\chipy-crystal-preview-frames")
OUT_FILE = OUT_DIR / "chipy-crystal-reveal-preview-v2.mp4"

ORANGE = (249, 115, 22)
CYAN = (6, 182, 212)
ICE = (190, 250, 255)
DARK = (2, 3, 5)


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def smooth(x: float) -> float:
    x = clamp(x)
    return x * x * (3 - 2 * x)


def back(x: float) -> float:
    x = clamp(x)
    c1 = 1.45
    c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def mix(a: float, b: float, p: float) -> float:
    return a + (b - a) * p


def rgba(c: tuple[int, int, int], a: int) -> tuple[int, int, int, int]:
    return (c[0], c[1], c[2], int(clamp(a, 0, 255)))


def bg() -> Image.Image:
    img = Image.new("RGBA", (W, H), (*DARK, 255))
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(12):
        r = 760 - i * 48
        a = 5 + i * 2
        d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), outline=(21, 46, 48, a), width=2)
    d.ellipse((260, 600, 700, 790), fill=(249, 115, 22, 52))
    d.ellipse((575, 600, 1015, 790), fill=(6, 182, 212, 50))
    d.rectangle((0, 0, W, H), fill=(0, 0, 0, 20))
    return img


BACKGROUND = bg()


def transform(points, cx: float, cy: float, sx: float, scale: float = 1.0, yoff: float = 0.0):
    out = []
    for x, y in points:
        out.append((cx + (x - cx) * sx * scale, cy + (y - cy) * scale + yoff))
    return out


def line(layer: Image.Image, points, color, width: int, alpha: int = 235) -> None:
    ImageDraw.Draw(layer, "RGBA").line(points, fill=rgba(color, alpha), width=width, joint="curve")


def poly(layer: Image.Image, points, fill, outline = None, width: int = 2) -> None:
    d = ImageDraw.Draw(layer, "RGBA")
    d.polygon(points, fill=fill)
    if outline:
        d.line(points + [points[0]], fill=rgba(outline, 235), width=width, joint="curve")


def draw_crystal(crisp: Image.Image, glow: Image.Image, t: float) -> tuple[float, float]:
    cx, cy = W * 0.5, H * 0.57
    scale = 0.72
    reveal = smooth(t / 0.55)
    spin = smooth(clamp(t / 2.65))
    theta = 2 * math.pi * 1.12 * spin
    lock = smooth((t - 2.35) / 0.55)
    sx = mix(0.18 + 0.82 * abs(math.cos(theta)), 1.0, lock)
    skew = math.sin(theta) * 32 * (1 - lock)
    bob = math.sin(t * 2.3) * 5 * (1 - lock)

    top = (cx + skew * 0.2, cy - 315)
    ls = (cx - 190 + skew, cy - 225)
    rs = (cx + 190 + skew, cy - 225)
    lm = (cx - 145 + skew * 0.55, cy - 25)
    rm = (cx + 145 + skew * 0.55, cy - 25)
    waist = (cx, cy + 92)
    lf = (cx - 125, cy + 245)
    rf = (cx + 125, cy + 245)
    bottom = (cx, cy + 285)

    outer = transform([top, rs, rm, rf, bottom, lf, lm, ls], cx, cy, sx, scale, bob)
    poly(glow, outer, fill=(0, 0, 0, 0), outline=ICE, width=14)
    poly(crisp, outer, fill=(0, 0, 0, int(158 * reveal)), outline=ICE, width=2)

    facets = [
        ([top, ls, lm, waist], ORANGE, 86),
        ([top, rs, rm, waist], CYAN, 86),
        ([lm, waist, lf], ORANGE, 72),
        ([rm, rf, waist], CYAN, 72),
        ([waist, lf, bottom], ORANGE, 55),
        ([waist, bottom, rf], CYAN, 55),
        ([top, ls, (cx - 30, cy - 170)], ORANGE, 70),
        ([top, rs, (cx + 30, cy - 170)], CYAN, 70),
    ]
    for pts, c, a in facets:
        p = transform(pts, cx, cy, sx, scale, bob)
        poly(glow, p, fill=rgba(c, int(a * reveal)), outline=c, width=9)
        poly(crisp, p, fill=rgba(c, int(a * reveal * 0.75)), outline=c, width=2)

    for pts, c in [
        ([top, waist, bottom], ICE),
        ([ls, rs], ICE),
        ([lm, waist, rm], ICE),
        ([lf, waist, rf], ICE),
        ([ls, waist], ORANGE),
        ([rs, waist], CYAN),
    ]:
        p = transform(pts, cx, cy, sx, scale, bob)
        line(glow, p, c, 9, int(150 * reveal))
        line(crisp, p, c, 2, int(220 * reveal))

    face = transform(
        [
            (cx - 86, cy - 218),
            (cx + 86, cy - 218),
            (cx + 108, cy - 92),
            (cx, cy + 24),
            (cx - 108, cy - 92),
        ],
        cx,
        cy,
        sx,
        scale,
        bob,
    )
    poly(crisp, face, fill=(0, 0, 0, int(132 * reveal)), outline=(58, 82, 88), width=1)

    eyes = smooth((t - 2.25) / 0.45)
    if eyes:
        le = transform([(cx - 70, cy - 132), (cx - 44, cy - 146), (cx - 18, cy - 132)], cx, cy, sx, scale, bob)
        re = transform([(cx + 18, cy - 132), (cx + 44, cy - 146), (cx + 70, cy - 132)], cx, cy, sx, scale, bob)
        line(glow, le, ORANGE, 18, int(245 * eyes))
        line(glow, re, CYAN, 18, int(245 * eyes))
        line(crisp, le, ORANGE, 7, int(255 * eyes))
        line(crisp, re, CYAN, 7, int(255 * eyes))

    d = ImageDraw.Draw(glow, "RGBA")
    d.ellipse((cx - 165 * sx, H - 95, cx + 165 * sx, H - 35), fill=(249, 115, 22, int(55 * reveal)))
    d.ellipse((cx - 20, H - 95, cx + 180 * sx, H - 35), fill=(6, 182, 212, int(55 * reveal)))
    return cx, cy + bob


def draw_calendar(crisp: Image.Image, glow: Image.Image, t: float) -> None:
    p = back((t - 3.05) / 0.75)
    if p <= 0:
        return
    p = clamp(p)
    x, y = mix(W + 120, W * 0.73, p), mix(H * 0.73, H * 0.53, p)
    w, h = 210, 170
    d = ImageDraw.Draw(crisp, "RGBA")
    dg = ImageDraw.Draw(glow, "RGBA")
    box = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    dg.rounded_rectangle(box, radius=16, outline=rgba(CYAN, 180), width=14)
    d.rounded_rectangle(box, radius=16, fill=(2, 20, 24, 185), outline=rgba(CYAN, 235), width=3)
    d.line((x - w / 2 + 18, y - h / 2 + 50, x + w / 2 - 18, y - h / 2 + 50), fill=rgba(ICE, 200), width=2)
    for i in range(4):
        rx = x - 72 + i * 48
        d.arc((rx, y - h / 2 - 24, rx + 34, y - h / 2 + 28), 0, 180, fill=rgba(ICE, 210), width=4)
    for r in range(3):
        for c in range(5):
            gx = x - 72 + c * 34
            gy = y - 24 + r * 30
            hit = r == 1 and c == 2
            d.rectangle((gx, gy, gx + 17, gy + 17), outline=rgba(ICE, 190), fill=rgba(CYAN if hit else ICE, 90 if hit else 18), width=1)


def draw_phone(crisp: Image.Image, glow: Image.Image, t: float) -> None:
    p = back((t - 3.38) / 0.75)
    if p <= 0:
        return
    p = clamp(p)
    x, y = mix(-150, W * 0.31, p), mix(H * 0.76, H * 0.54, p)
    pts = [(x + 70, y - 115), (x + 12, y - 82), (x - 18, y - 18), (x - 5, y + 55), (x + 54, y + 105)]
    line(glow, pts, ORANGE, 42, 175)
    line(crisp, pts, (31, 17, 11), 32, 235)
    line(crisp, pts, ORANGE, 6, 245)
    d = ImageDraw.Draw(crisp, "RGBA")
    d.rounded_rectangle((x + 32, y - 150, x + 118, y - 92), radius=24, fill=(31, 17, 11, 165), outline=rgba(ORANGE, 235), width=3)
    d.rounded_rectangle((x + 28, y + 80, x + 118, y + 140), radius=24, fill=(31, 17, 11, 165), outline=rgba(ORANGE, 235), width=3)


def draw_hair(crisp: Image.Image, glow: Image.Image, t: float, cx: float, cy: float) -> None:
    p = back((t - 4.82) / 0.75)
    if p <= 0:
        return
    p = clamp(p)
    anchor = cy - 226
    paths = [
        ([(cx - 54, anchor + 22), (cx - 105, anchor - 28), (cx - 72, anchor - 92), (cx - 44, anchor - 165), (cx - 20, anchor - 78), (cx + 8, anchor - 4)], ORANGE),
        ([(cx - 4, anchor + 12), (cx + 4, anchor - 54), (cx + 42, anchor - 118), (cx + 36, anchor - 190), (cx + 92, anchor - 96), (cx + 84, anchor - 12)], CYAN),
        ([(cx - 24, anchor + 28), (cx - 8, anchor - 24), (cx + 20, anchor - 88), (cx + 16, anchor - 145), (cx + 58, anchor - 72), (cx + 52, anchor - 4)], ICE),
    ]
    for pts, c in paths:
        scaled = [(cx + (x - cx) * p, anchor + (y - anchor) * p) for x, y in pts]
        line(glow, scaled, c, max(5, int(18 * p)), int(210 * p))
        line(crisp, scaled, c, max(2, int(6 * p)), int(255 * p))


def draw_sheen(crisp: Image.Image, glow: Image.Image, t: float) -> None:
    p = smooth((t - 5.82) / 0.65) * (1 - smooth((t - 6.55) / 0.35))
    if p <= 0:
        return
    x = mix(W * 0.24, W * 0.79, p)
    a = int(170 * math.sin(math.pi * p))
    line(glow, [(x - 55, 135), (x + 55, 630)], ICE, 10, a)
    line(crisp, [(x - 55, 135), (x + 55, 630)], ICE, 2, a)


def render_frame(i: int) -> Image.Image:
    t = i / FPS
    frame = BACKGROUND.copy()
    crisp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx, cy = draw_crystal(crisp, glow, t)
    draw_phone(crisp, glow, t)
    draw_calendar(crisp, glow, t)
    draw_hair(crisp, glow, t, cx, cy)
    draw_sheen(crisp, glow, t)
    frame.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))
    frame.alpha_composite(crisp)
    fade = 1 - smooth((t - 6.55) / 0.45)
    if fade < 1:
        d = ImageDraw.Draw(frame, "RGBA")
        d.rectangle((0, 0, W, H), fill=(0, 0, 0, int(255 * (1 - fade) * 0.18)))
    return frame.convert("RGB")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if FRAME_DIR.exists():
        shutil.rmtree(FRAME_DIR)
    FRAME_DIR.mkdir(parents=True)
    for i in range(FRAMES):
        render_frame(i).save(FRAME_DIR / f"frame_{i:04d}.jpg", quality=92, subsampling=0)
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
            "18",
            "-movflags",
            "+faststart",
            str(OUT_FILE),
        ],
        check=True,
    )
    print(OUT_FILE)


if __name__ == "__main__":
    main()
