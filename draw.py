#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

Fresh artwork: every scene is drawn from simple PIL shapes -- no photos,
no downloaded images. Layout: masthead, one lead story, six tiles, footer.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (24, 28, 38)
NAVY = (18, 42, 78)
RED = (178, 34, 34)
GOLD = (212, 160, 32)
TEAL = (16, 110, 110)
SKY = (140, 185, 220)
DUSK = (52, 68, 110)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, box, fill, outline=INK, width=3):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


def skyline(draw, x0, y0, x1, y1, color):
    """Simple city silhouette with lit windows."""
    import random
    rnd = random.Random(7)
    x = x0
    while x < x1:
        bw = rnd.randint(26, 52)
        bh = rnd.randint(30, int((y1 - y0) * 0.75))
        draw.rectangle([x, y1 - bh, min(x + bw, x1), y1], fill=color)
        for wy in range(y1 - bh + 8, y1 - 6, 14):
            for wx in range(x + 6, min(x + bw, x1) - 6, 12):
                if rnd.random() < 0.35:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 214, 90))
        x += bw + 4


def missile(draw, x, y, angle_deg, scale, body=(200, 210, 220)):
    """A small missile with flame, pointing along angle_deg (0 = right)."""
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)
    px, py = -dy, dx
    L, R = 46 * scale, 7 * scale
    nose = (x + dx * L, y + dy * L)
    tail = (x - dx * L * 0.7, y - dy * L * 0.7)
    pts = [
        nose,
        (tail[0] + px * R, tail[1] + py * R),
        (tail[0] - px * R, tail[1] - py * R),
    ]
    draw.polygon(pts, fill=body, outline=INK)
    # fins
    draw.polygon(
        [(tail[0], tail[1]),
         (tail[0] - dx * 16 * scale + px * 14 * scale,
          tail[1] - dy * 16 * scale + py * 14 * scale),
         (tail[0] - dx * 4 * scale + px * 8 * scale,
          tail[1] - dy * 4 * scale + py * 8 * scale)],
        fill=RED, outline=INK)
    draw.polygon(
        [(tail[0], tail[1]),
         (tail[0] - dx * 16 * scale - px * 14 * scale,
          tail[1] - dy * 16 * scale - py * 14 * scale),
         (tail[0] - dx * 4 * scale - px * 8 * scale,
          tail[1] - dy * 4 * scale - py * 8 * scale)],
        fill=RED, outline=INK)
    # flame
    fx, fy = tail[0] - dx * 10 * scale, tail[1] - dy * 10 * scale
    draw.polygon(
        [(fx, fy),
         (fx - dx * 30 * scale + px * 9 * scale,
          fy - dy * 30 * scale + py * 9 * scale),
         (fx - dx * 30 * scale - px * 9 * scale,
          fy - dy * 30 * scale - py * 9 * scale)],
        fill=(255, 170, 40), outline=(200, 90, 0))

def scene_strikes(draw, box):
    """Night sky over Kyiv: explosions, missiles, bridge over a river."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=DUSK)
    for cx, cy, r in [(x0 + 90, y0 + 60, 46), (x0 + 300, y0 + 40, 34),
                      (x0 + 340, y0 + 78, 30)]:
        for rr, col in [(r, (255, 190, 60)), (r * 0.6, (255, 120, 30)),
                        (r * 0.3, (255, 230, 150))]:
            draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    missile(draw, x0 + 420, y0 + 95, -38, 0.9)
    missile(draw, x0 + 180, y0 + 120, -25, 0.7)
    skyline(draw, x0, y0 + 150, x1, y1 - 52, (16, 20, 34))
    # river + bridge
    draw.rectangle([x0, y1 - 52, x1, y1], fill=(30, 80, 120))
    draw.line([x0, y1 - 52, x1, y1 - 52], fill=INK, width=3)
    for bx in range(x0 + 30, x1 - 30, 110):
        draw.arc([bx, y1 - 96, bx + 90, y1 - 20], 180, 360,
                 fill=(255, 214, 90), width=4)
    draw.rectangle([x0, y1 - 46, x1, y1 - 40], fill=(200, 200, 200))


def scene_summit(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 222, 196))
    # three flags on poles
    cols = [(178, 34, 34), (255, 255, 255), (200, 30, 30)]
    for i, c in enumerate(cols):
        fx = x0 + 60 + i * 90
        draw.line([fx, y0 + 18, fx, y1 - 30], fill=INK, width=4)
        draw.rectangle([fx, y0 + 18, fx + 62, y0 + 52], fill=c,
                       outline=INK, width=2)
    # table with three leaders (simple figures)
    draw.rectangle([x0 + 30, y1 - 62, x1 - 30, y1 - 34], fill=(120, 70, 40),
                   outline=INK, width=2)
    for i, suit in enumerate([(18, 42, 78), (60, 60, 60), (90, 20, 20)]):
        cx = x0 + 80 + i * 90
        draw.ellipse([cx - 20, y1 - 118, cx + 20, y1 - 78], fill=(232, 200, 160),
                     outline=INK, width=2)
        draw.polygon([(cx - 26, y1 - 62), (cx + 26, y1 - 62),
                      (cx + 18, y1 - 84), (cx - 18, y1 - 84)],
                     fill=suit, outline=INK)


def scene_missile_sea(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(168, 205, 230))
    draw.ellipse([x0 + 210, y0 + 12, x0 + 262, y0 + 64], fill=(255, 240, 160),
                 outline=(220, 180, 60), width=2)
    missile(draw, x0 + 150, y0 + 62, -50, 0.9)
    for k in range(4):
        draw.arc([x0 + 40 + k * 60, y0 + 120 + k * 8,
                  x0 + 120 + k * 60, y0 + 150 + k * 8], 200, 340,
                 fill=(255, 255, 255), width=4)
    draw.rectangle([x0, y1 - 34, x1, y1], fill=(28, 90, 140))
    for wx in range(x0 + 12, x1 - 12, 34):
        draw.line([wx, y1 - 18, wx + 16, y1 - 18], fill=(255, 255, 255), width=3)


def scene_poland(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(210, 225, 200))
    # radar dish
    cx, cy = x0 + 150, y0 + 110
    draw.line([cx, cy, cx - 30, y1 - 30], fill=INK, width=5)
    draw.line([cx, cy, cx + 30, y1 - 30], fill=INK, width=5)
    draw.pieslice([cx - 70, cy - 70, cx + 70, cy + 70], 200, 340,
                  fill=(120, 160, 120), outline=INK, width=3)
    draw.arc([cx - 92, cy - 92, cx + 92, cy + 92], 200, 340,
             fill=(16, 110, 110), width=3)
    draw.line([cx, cy, cx + 78, cy - 52], fill=RED, width=4)
    for qx, qy in [(x0 + 52, y0 + 34), (x0 + 250, y0 + 40)]:
        draw.text((qx, qy), "?", font=font(BOLD, 44), fill=RED)


def scene_drones(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(196, 216, 235))
    for i, (dx, dy) in enumerate([(70, 50), (150, 80), (230, 45),
                                  (110, 120), (200, 125)]):
        cx, cy = x0 + dx, y0 + dy
        draw.ellipse([cx - 26, cy - 8, cx - 8, cy + 8], outline=INK, width=2)
        draw.ellipse([cx + 8, cy - 8, cx + 26, cy + 8], outline=INK, width=2)
        draw.rectangle([cx - 20, cy - 6, cx + 20, cy + 6], fill=(60, 70, 90),
                       outline=INK, width=2)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    draw.rectangle([x0 + 40, y1 - 46, x1 - 40, y1 - 20], fill=(255, 214, 90),
                   outline=INK, width=2)
    draw.text((x0 + 62, y1 - 44), "UK  >  UKRAINE", font=font(BOLD, 20), fill=INK)


def scene_cop(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(206, 232, 210))
    cx, cy = x0 + 150, y0 + 82
    draw.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], fill=(70, 140, 200),
                 outline=INK, width=3)
    draw.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], outline=(255, 255, 255),
                 width=1)
    for gx, gy in [(cx - 30, cy - 20), (cx + 28, cy + 10), (cx - 5, cy + 34)]:
        draw.ellipse([gx - 16, gy - 10, gx + 16, gy + 10], fill=(90, 180, 90),
                     outline=INK, width=2)
    # oil drop crossed out
    ox, oy = x0 + 235, y0 + 118
    draw.polygon([(ox, oy - 26), (ox + 20, oy + 8), (ox, oy + 24),
                  (ox - 20, oy + 8)], fill=(40, 40, 40), outline=INK)
    draw.line([ox - 26, oy - 30, ox + 26, oy + 30], fill=RED, width=6)
    draw.line([ox - 26, oy + 30, ox + 26, oy - 30], fill=RED, width=6)


def scene_rose(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(120, 170, 90))
    draw.polygon([(x0 + 150, y1 - 28), (x0 + 60, y0 + 78),
                  (x0 + 240, y0 + 78)], fill=(210, 180, 130),
                 outline=(255, 255, 255), width=3)
    draw.ellipse([x0 + 128, y0 + 92, x0 + 172, y0 + 136], fill=(255, 255, 255),
                 outline=RED, width=3)
    draw.arc([x0 + 134, y0 + 96, x0 + 150, y0 + 132], 300, 60, fill=RED, width=2)
    draw.arc([x0 + 150, y0 + 96, x0 + 166, y0 + 132], 120, 240, fill=RED, width=2)
    # bat
    draw.line([x0 + 235, y0 + 30, x0 + 195, y0 + 110], fill=(150, 100, 50),
              width=10)
    draw.text((x0 + 12, y0 + 10), "4,256 HITS", font=font(BOLD, 22), fill=(255, 255, 255))

TILES = [
    ("SUMMIT IN SHENZHEN", "Trump, Xi & Putin meet \u2014 no Ukraine deal",
     scene_summit, (232, 222, 196)),
    ("NORTH KOREA", "Fires ballistic missile into the sea, Seoul says",
     scene_missile_sea, (168, 205, 230)),
    ("POLAND", "Probes unknown objects at border",
     scene_poland, (210, 225, 200)),
    ("BRITAIN AIDS KYIV", "UK pledges 1,000+ drones, \u00a3260m",
     scene_drones, (196, 216, 235)),
    ("COP31, ANTALYA", "Final day: draft deal drops all fossil fuels",
     scene_cop, (206, 232, 210)),
    ("BASEBALL", "Trump pardons Pete Rose, posthumously",
     scene_rose, (120, 170, 90)),
]


def build(path="news.png"):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 126], fill=GOLD)
    d.text((36, 14), "THE WORLD IN ONE DAY",
           font=font(BOLD, 46), fill=(255, 255, 255))
    d.text((36, 72), "Friday, 20 November 2026",
           font=font(BOLD, 34), fill=GOLD)
    d.text((700, 30), "WORLD NEWS", font=font(BOLD, 26), fill=(255, 255, 255))
    d.text((700, 66), "7 stories \u00b7 1 day", font=font(REG, 22),
           fill=(200, 210, 230))
    # Lead story
    lx, ly, lw, lh = 28, 144, 968, 330
    panel(d, [lx, ly, lx + lw, ly + lh], (255, 255, 255))
    scene_strikes(d, [lx + 8, ly + 8, lx + 430, ly + lh - 8])
    d.text((lx + 452, ly + 18), "UKRAINE UNDER FIRE",
           font=font(BOLD, 34), fill=RED)
    lines = wrap(d, "Russia launches a huge overnight missile and drone "
                 "attack on Kyiv: 100+ missiles, 400 drones; 8 killed, "
                 "bridges hit, power cut.",
                 font(BOLD, 26), 500)
    y = text_block(d, (lx + 452, ly + 64), lines, font(BOLD, 26), INK, 34)
    d.text((lx + 452, y + 14), "Hours after the Shenzhen summit ends",
           font=font(REG, 22), fill=(90, 90, 90))
    d.text((lx + 452, y + 44), "with no Ukraine breakthrough.",
           font=font(REG, 22), fill=(90, 90, 90))
    # Tiles: 3 columns x 2 rows
    tw, th, gap = 312, 236, 16
    tx0, ty0 = 28, 492
    for i, (kick, head, scene, _bg) in enumerate(TILES):
        col, row = i % 3, i // 3
        x = tx0 + col * (tw + gap)
        y = ty0 + row * (th + gap)
        panel(d, [x, y, x + tw, y + th], (255, 255, 255))
        scene(d, [x + 6, y + 6, x + tw - 6, y + 148])
        d.text((x + 12, y + 156), kick, font=font(BOLD, 19), fill=RED)
        lines = wrap(d, head, font(BOLD, 21), tw - 24)
        text_block(d, (x + 12, y + 180), lines[:2], font(BOLD, 21), INK, 25)
    # Footer
    d.rectangle([0, 992, W, H], fill=NAVY)
    d.text((36, 1000), "All events of Friday 20 November 2026, as reported that day.",
           font=font(REG, 18), fill=(255, 255, 255))
    img.save(path, "PNG", optimize=True)
    print("wrote", path, img.size)


if __name__ == "__main__":
    build()
