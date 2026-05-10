from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


W, H = 1920, 1080
FPS = 30
DURATION = 8.0
FRAMES = int(FPS * DURATION)
OUT_DIR = Path(r"C:\Users\pc105\Obsidian\Phonbot\assets\video")
FRAME_DIR = Path(r"C:\Users\pc105\AppData\Local\Temp\chipy-crystal-reveal-frames")
OUT_FILE = OUT_DIR / "chipy-crystal-reveal-v1.mp4"

ORANGE = (249, 115, 22)
CYAN = (6, 182, 212)
ICE = (180, 245, 255)
INK = (0, 0, 0)


def clamp(x: float, a = 0.0, b = 1.0) -> float:
    return max(a, min(b, x))


def smoothstep(x: float) -> float:
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out_back(x: float) -> float:
    x = clamp(x)
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def mix(a: float, b: float, p: float) -> float:
    return a + (b - a) * p


def rgba(c: tuple[int, int, int], a: int) -> tuple[int, int, int, int]:
    return (c[0], c[1], c[2], a)


def add_glow(base: Image.Image, draw_fn, blur: int = 20, repeats: int = 1) -> None:
    for _ in range(repeats):
        layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        draw_fn(d)
        base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def line_glow(base: Image.Image, pts, color, width: int, alpha: int = 230, blur: int = 18) -> None:
    pts = [(int(x), int(y)) for x, y in pts]

    def glow(d: ImageDraw.ImageDraw) -> None:
        d.line(pts, fill=rgba(color, min(180, alpha)), width=width * 2, joint="curve")

    add_glow(base, glow, blur=blur, repeats=1)
    d = ImageDraw.Draw(base)
    d.line(pts, fill=rgba(color, alpha), width=width, joint="curve")


def poly_glow(base: Image.Image, pts, fill, outline = None, width: int = 3, blur: int = 18) -> None:
    pts = [(int(x), int(y)) for x, y in pts]
    if outline:
        def glow(d: ImageDraw.ImageDraw) -> None:
            d.line(pts + [pts[0]], fill=rgba(outline, 160), width=width * 3, joint="curve")

        add_glow(base, glow, blur=blur, repeats=1)
    d = ImageDraw.Draw(base, "RGBA")
    d.polygon(pts, fill=fill)
    if outline:
        d.line(pts + [pts[0]], fill=rgba(outline, 235), width=width, joint="curve")


def make_background() -> Image.Image:
    bg = Image.new("RGBA", (W, H), (2, 3, 4, 255))
    d = ImageDraw.Draw(bg, "RGBA")
    for r in range(960, 60, -35):
        a = int(16 * (1 - r / 980))
        d.ellipse((W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r), outline=(20, 35, 38, a), width=3)
    for i in range(18):
        x = int((i * 317) % W)
        y = int(70 + ((i * 149) % 660))
        d.ellipse((x, y, x + 2, y + 2), fill=(180, 245, 255, 18))
    d.ellipse((370, 885, 1040, 1165), fill=(249, 115, 22, 62))
    d.ellipse((880, 885, 1550, 1165), fill=(6, 182, 212, 58))
    return bg.filter(ImageFilter.GaussianBlur(1))


BACKGROUND = make_background()


def tx(points, cx: float, sx: float, ox = 0.0, oy = 0.0):
    return [(cx + (x - cx) * sx + ox, y + oy) for x, y in points]


def draw_crystal(base: Image.Image, t: float) -> tuple[float, float]:
    cx = W / 2
    reveal = smoothstep(t / 0.7)
    spin_t = clamp(t / 3.05)
    theta = 2 * math.pi * (1.18 * smoothstep(spin_t)) + 0.12 * math.sin(t * 3)
    spin_width = 0.22 + 0.78 * abs(math.cos(theta))
    front_lock = smoothstep((t - 2.55) / 0.55)
    sx = mix(spin_width, 1.0, front_lock)
    bob = math.sin(t * 2.2) * 5 * (1 - front_lock)

    top = (cx, 260)
    left_shoulder = (cx - 250, 375)
    right_shoulder = (cx + 250, 375)
    left_mid = (cx - 205, 620)
    right_mid = (cx + 205, 620)
    waist = (cx, 745)
    left_foot = (cx - 165, 900)
    right_foot = (cx + 165, 900)
    bottom = (cx, 960)

    outer = tx([top, right_shoulder, right_mid, right_foot, bottom, left_foot, left_mid, left_shoulder], cx, sx, 0, bob)
    alpha = int(255 * reveal)
    poly_glow(base, outer, fill=(0, 0, 0, int(170 * reveal)), outline=ICE, width=3, blur=24)

    facets = [
        ([top, left_shoulder, left_mid, waist], ORANGE, 90),
        ([top, right_shoulder, right_mid, waist], CYAN, 90),
        ([left_mid, waist, left_foot], ORANGE, 80),
        ([right_mid, right_foot, waist], CYAN, 80),
        ([waist, left_foot, bottom], ORANGE, 65),
        ([waist, bottom, right_foot], CYAN, 65),
        ([top, left_shoulder, (cx - 35, 430)], ORANGE, 70),
        ([top, right_shoulder, (cx + 35, 430)], CYAN, 70),
    ]
    for pts, color, a in facets:
        poly_glow(base, tx(pts, cx, sx, 0, bob), fill=rgba(color, int(a * reveal)), outline=color, width=2, blur=18)

    for pts, color in [
        ([top, waist, bottom], ICE),
        ([left_shoulder, right_shoulder], ICE),
        ([left_mid, waist, right_mid], ICE),
        ([left_foot, waist, right_foot], ICE),
        ([left_shoulder, waist], ORANGE),
        ([right_shoulder, waist], CYAN),
    ]:
        line_glow(base, tx(pts, cx, sx, 0, bob), color, width=2, alpha=int(180 * reveal), blur=13)

    eye_p = smoothstep((t - 2.35) / 0.65)
    if eye_p > 0:
        d = ImageDraw.Draw(base, "RGBA")
        left_eye = tx([(cx - 90, 470), (cx - 55, 455), (cx - 20, 470)], cx, sx, 0, bob)
        right_eye = tx([(cx + 20, 470), (cx + 55, 455), (cx + 90, 470)], cx, sx, 0, bob)
        line_glow(base, left_eye, ORANGE, width=max(2, int(8 * eye_p)), alpha=int(235 * eye_p), blur=16)
        line_glow(base, right_eye, CYAN, width=max(2, int(8 * eye_p)), alpha=int(235 * eye_p), blur=16)
        d.arc((int(cx - 105 * sx), int(452 + bob), int(cx - 5 * sx), int(504 + bob)), 200, 340, fill=rgba(ORANGE, int(255 * eye_p)), width=max(2, int(5 * eye_p)))
        d.arc((int(cx + 5 * sx), int(452 + bob), int(cx + 105 * sx), int(504 + bob)), 200, 340, fill=rgba(CYAN, int(255 * eye_p)), width=max(2, int(5 * eye_p)))

    d = ImageDraw.Draw(base, "RGBA")
    d.ellipse((cx - 230 * sx, 930, cx + 230 * sx, 1015), fill=(0, 0, 0, 110))
    d.ellipse((cx - 220 * sx, 945, cx + 20, 990), fill=(249, 115, 22, int(70 * reveal)))
    d.ellipse((cx - 20, 945, cx + 220 * sx, 990), fill=(6, 182, 212, int(70 * reveal)))
    return cx, bob


def draw_calendar(base: Image.Image, t: float) -> None:
    p = ease_out_back((t - 3.1) / 0.9)
    if p <= 0:
        return
    alpha = int(235 * clamp(p))
    x = mix(W + 260, 1240, clamp(p))
    y = mix(650, 535, clamp(p))
    w, h = 285, 245
    d = ImageDraw.Draw(base, "RGBA")
    rect = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)]
    poly_glow(base, rect, fill=(2, 20, 24, int(170 * clamp(p))), outline=CYAN, width=4, blur=24)
    d.rectangle((x - w / 2 + 20, y - h / 2 + 38, x + w / 2 - 20, y + h / 2 - 24), outline=rgba(ICE, alpha), width=3)
    d.line((x - w / 2 + 20, y - h / 2 + 82, x + w / 2 - 20, y - h / 2 + 82), fill=rgba(CYAN, alpha), width=3)
    for i in range(4):
        rx = x - 95 + i * 55
        d.arc((rx, y - h / 2 - 38, rx + 42, y - h / 2 + 32), 0, 180, fill=rgba(ICE, alpha), width=6)
    for row in range(4):
        for col in range(5):
            gx = x - 88 + col * 44
            gy = y - 24 + row * 34
            fill = rgba(CYAN if (row == 2 and col == 2) else ICE, int((95 if row == 2 and col == 2 else 28) * clamp(p)))
            d.rectangle((gx, gy, gx + 20, gy + 20), outline=rgba(ICE, int(190 * clamp(p))), fill=fill, width=2)


def make_phone_layer(alpha: int) -> Image.Image:
    layer = Image.new("RGBA", (360, 430), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    pts = [(245, 80), (180, 100), (155, 170), (168, 245), (225, 300), (287, 326)]

    def glow(g: ImageDraw.ImageDraw) -> None:
        g.line(pts, fill=rgba(ORANGE, min(150, alpha)), width=70, joint="curve")

    add_glow(layer, glow, blur=22, repeats=1)
    d.line(pts, fill=(21, 13, 9, alpha), width=58, joint="curve")
    d.line(pts, fill=rgba(ORANGE, alpha), width=10, joint="curve")
    d.rounded_rectangle((214, 42, 320, 120), radius=35, outline=rgba(ORANGE, alpha), fill=(34, 20, 12, int(alpha * 0.48)), width=5)
    d.rounded_rectangle((246, 288, 350, 370), radius=35, outline=rgba(ORANGE, alpha), fill=(34, 20, 12, int(alpha * 0.48)), width=5)
    d.line((238, 56, 305, 107), fill=rgba(ICE, int(alpha * 0.65)), width=3)
    d.line((268, 305, 337, 354), fill=rgba(ICE, int(alpha * 0.65)), width=3)
    return layer


def draw_phone(base: Image.Image, t: float) -> None:
    p = ease_out_back((t - 3.45) / 0.9)
    if p <= 0:
        return
    p = clamp(p)
    layer = make_phone_layer(int(235 * p))
    angle = mix(-48, -14, p)
    layer = layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    x = int(mix(-310, 570, p))
    y = int(mix(650, 530, p))
    base.alpha_composite(layer, (x - layer.width // 2, y - layer.height // 2))


def draw_hair(base: Image.Image, t: float, cx: float, bob: float) -> None:
    p = ease_out_back((t - 5.05) / 1.0)
    if p <= 0:
        return
    p = clamp(p)
    anchor_y = 246 + bob
    paths = [
        ([(cx - 70, anchor_y + 18), (cx - 120, anchor_y - 35), (cx - 80, anchor_y - 105), (cx - 40, anchor_y - 190), (cx - 22, anchor_y - 84), (cx + 8, anchor_y - 8)], ORANGE, CYAN),
        ([(cx - 12, anchor_y + 8), (cx - 5, anchor_y - 62), (cx + 42, anchor_y - 142), (cx + 37, anchor_y - 220), (cx + 100, anchor_y - 122), (cx + 92, anchor_y - 20)], CYAN, ORANGE),
        ([(cx - 30, anchor_y + 28), (cx - 20, anchor_y - 18), (cx + 10, anchor_y - 88), (cx + 2, anchor_y - 170), (cx + 52, anchor_y - 80), (cx + 54, anchor_y - 8)], ICE, CYAN),
    ]
    for points, primary, secondary in paths:
        scaled = [(cx + (x - cx) * p, anchor_y + (y - anchor_y) * p) for x, y in points]
        line_glow(base, scaled, primary, width=max(2, int(16 * p)), alpha=int(235 * p), blur=22)
        inner = [(x + 12 * p, y + 4 * p) for x, y in scaled]
        line_glow(base, inner, secondary, width=max(1, int(6 * p)), alpha=int(210 * p), blur=12)


def draw_final_sheen(base: Image.Image, t: float) -> None:
    p = smoothstep((t - 6.35) / 0.9) * (1 - smoothstep((t - 7.35) / 0.5))
    if p <= 0:
        return
    x = mix(360, 1500, p)
    line_glow(base, [(x - 80, 230), (x + 80, 900)], ICE, width=3, alpha=int(160 * math.sin(p * math.pi)), blur=16)


def render_frame(i: int) -> Image.Image:
    t = i / FPS
    frame = BACKGROUND.copy()
    d = ImageDraw.Draw(frame, "RGBA")
    d.rectangle((0, 0, W, H), fill=(0, 0, 0, int(45 * (1 - smoothstep(t / 0.8)))))
    cx, bob = draw_crystal(frame, t)
    draw_calendar(frame, t)
    draw_phone(frame, t)
    draw_hair(frame, t, cx, bob)
    draw_final_sheen(frame, t)
    return frame.convert("RGB")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if FRAME_DIR.exists():
        shutil.rmtree(FRAME_DIR)
    FRAME_DIR.mkdir(parents=True)

    for i in range(FRAMES):
        frame = render_frame(i)
        frame.save(FRAME_DIR / f"frame_{i:04d}.png", optimize=False)
        if i % 30 == 0:
            print(f"rendered {i}/{FRAMES}")

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(FPS),
        "-i",
        str(FRAME_DIR / "frame_%04d.png"),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "18",
        "-movflags",
        "+faststart",
        str(OUT_FILE),
    ]
    subprocess.run(cmd, check=True)
    print(OUT_FILE)


if __name__ == "__main__":
    main()
