#!/usr/bin/env python3
"""Draw the GTA 6 launch-day meme for the gta6-meme-x-01 bounty.

Scene: a Vice City / Leonida sunset. The make.fun ghost (press-kit asset,
assets/ghost.png) is the setting sun itself: its magenta disc hangs over the
ocean, big enough to stay recognisable at 480x480. Below it, the GTA-style
"WASTED" and a two-line caption carry the joke.

Output: meme.png, 1024x1024, next to this script.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 1024

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, width, y0, y1, top, bottom):
    """Vertical gradient band from y0 to y1."""
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        draw.line([(0, y), (width, y)], fill=lerp(top, bottom, (y - y0) / span))


def text_outline(draw, xy, text, fnt, fill, outline, width=4):
    x, y = xy
    for dx in range(-width, width + 1):
        for dy in range(-width, width + 1):
            if dx * dx + dy * dy <= width * width:
                draw.text((x + dx, y + dy), text, font=fnt, fill=outline)
    draw.text((x, y), text, font=fnt, fill=fill)


def text_center(draw, cx, y, text, fnt, fill, outline, width=4):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    w = bbox[2] - bbox[0]
    text_outline(draw, (cx - w // 2 - bbox[0], y), text, fnt, fill, outline, width)


def bezier(p0, p1, p2, steps=24):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def palm(draw, base_x, base_y, lean, height, color):
    """One palm silhouette. lean: -1 leans left, +1 leans right."""
    top_x = base_x + lean * 70
    top_y = base_y - height
    # trunk: gentle curve
    trunk = bezier((base_x, base_y), (base_x + lean * 20, base_y - height * 0.55),
                   (top_x, top_y), steps=20)
    draw.line(trunk, fill=color, width=26, joint="curve")
    # fronds: arcs drooping out from the crown
    for angle_deg, length in ((-160, 190), (-120, 220), (-80, 230),
                             (-40, 220), (0, 190), (35, 150)):
        a = math.radians(angle_deg)
        # frond tip curls downward
        tip = (top_x + math.cos(a) * length, top_y + math.sin(a) * length * 0.45 + 70)
        mid = (top_x + math.cos(a) * length * 0.55,
               top_y + math.sin(a) * length * 0.30 - 25)
        draw.line(bezier((top_x, top_y), mid, tip, steps=12),
                  fill=color, width=13, joint="curve")
    # coconuts
    draw.ellipse([top_x - 18, top_y + 4, top_x + 2, top_y + 24], fill=color)
    draw.ellipse([top_x + 4, top_y + 8, top_x + 22, top_y + 26], fill=color)


def main():
    img = Image.new("RGB", (SIZE, SIZE), (20, 4, 40))
    draw = ImageDraw.Draw(img)

    # --- sky: deep purple up top, hot pink, orange at the horizon ---
    vgrad(draw, SIZE, 0, 300, (26, 6, 52), (150, 24, 96))
    vgrad(draw, SIZE, 300, 610, (150, 24, 96), (255, 122, 54))

    # --- distant Vice City skyline on the horizon ---
    skyline = (18, 6, 44)
    buildings = [(0, 560, 70, 610), (70, 540, 130, 610), (130, 575, 190, 610),
                 (190, 530, 250, 610), (250, 565, 320, 610), (320, 545, 380, 610),
                 (650, 550, 710, 610), (710, 570, 780, 610), (780, 535, 840, 610),
                 (840, 565, 910, 610), (910, 545, 980, 610), (980, 570, 1024, 610)]
    for x0, y0, x1, y1 in buildings:
        draw.rectangle([x0, y0, x1, y1], fill=skyline)
    # lit windows
    for bx, by in [(90, 560), (210, 555), (350, 565), (730, 570), (860, 555)]:
        draw.rectangle([bx, by, bx + 8, by + 10], fill=(255, 190, 90))

    # --- the ghost is the sun ---
    ghost = Image.open(os.path.join(HERE, "assets", "ghost.png")).convert("RGBA")
    sun_d = 400
    ghost = ghost.resize((sun_d, sun_d), Image.LANCZOS)
    img.paste(ghost, (SIZE // 2 - sun_d // 2, 92), ghost)
    draw = ImageDraw.Draw(img)

    # --- ocean with a sun reflection ---
    vgrad(draw, SIZE, 610, 830, (44, 14, 74), (16, 22, 66))
    refl = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    rd = ImageDraw.Draw(refl)
    for i, y in enumerate(range(622, 826, 12)):
        w = 150 - i * 2
        x0 = SIZE // 2 - w // 2
        alpha = max(40, 190 - i * 10)
        rd.line([(x0, y), (x0 + w, y)], fill=(255, 150, 80, alpha), width=6)
    img.paste(Image.alpha_composite(img.convert("RGBA"), refl).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)

    # --- foreground sand, dark ---
    vgrad(draw, SIZE, 830, SIZE, (30, 10, 46), (12, 4, 24))

    # --- birds ---
    for bx, by, s in [(180, 150, 16), (230, 120, 12), (830, 170, 14), (790, 130, 10)]:
        draw.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340, fill=(20, 5, 40), width=4)
        draw.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340, fill=(20, 5, 40), width=4)

    # --- palms framing the scene ---
    palm_color = (12, 4, 26)
    palm(draw, 60, 1024, 1, 560, palm_color)    # left, leaning right
    palm(draw, 970, 1024, -1, 590, palm_color)  # right, leaning left

    # --- top tag ---
    tag = font(BOLD, 34)
    text_center(draw, SIZE // 2, 30, "L E O N I D A  •  V I C E  C I T Y",
                tag, (255, 235, 220), (10, 4, 24), width=3)

    # --- WASTED, GTA style: light grey with a heavy black outline ---
    wasted = font(BOLD, 168)
    text_center(draw, SIZE // 2, 632, "WASTED", wasted,
                (208, 208, 208), (0, 0, 0), width=7)

    # --- caption: the joke, big and short ---
    line1 = font(BOLD, 54)
    text_center(draw, SIZE // 2, 836, "Sick day for GTA 6.",
                line1, (255, 255, 255), (0, 0, 0), width=5)
    line2 = font(BOLD, 40)  # 44px measured 1020px wide: flush to the edges
    text_center(draw, SIZE // 2, 910, "My agent earns on make.fun while I play.",
                line2, (255, 214, 240), (0, 0, 0), width=5)

    out = os.path.join(HERE, "meme.png")
    img.save(out, "PNG")
    print(f"wrote {out} {img.size} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
