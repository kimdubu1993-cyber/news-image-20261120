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
    missile(draw, x0 + 375, y0 + 95, -38, 0.8)
    missile(draw, x0 + 180, y0 + 120, -25, 0.7)
    skyline(draw, x0, y0 + 150, x1, y1 - 52, (16, 20, 34))
    # river + bridge
    draw.rectangle([x0, y1 - 52, x1, y1], fill=(30, 80, 120))
    draw.line([x0, y1 - 52, x1, y1 - 52], fill=INK, width=3)
    for bx in range(x0 + 30, x1 - 120, 110):
        draw.arc([bx, y1 - 96, bx + 90, y1 - 20], 180, 360,
                 fill=(255, 214, 90), width=4)
    draw.rectangle([x0, y1 - 46, x1, y1 - 40], fill=(200, 200, 200))


def scene_markets(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(250, 240, 225))
    draw.text((x0 + 16, y0 + 8), "AI SELLOFF", font=font(BOLD, 20), fill=RED)
    for gy in range(y0 + 40, y1 - 30, 26):
        draw.line([x0 + 14, gy, x1 - 14, gy], fill=(220, 210, 190), width=1)
    pts = [(x0 + 24, y0 + 48), (x0 + 70, y0 + 62), (x0 + 110, y0 + 56),
           (x0 + 155, y0 + 82), (x0 + 200, y0 + 78), (x0 + 245, y0 + 104),
           (x0 + 274, y0 + 116)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey + 12), (ex - 16, ey - 6), (ex + 2, ey - 12)],
                 fill=RED)
    for i, bh in enumerate([16, 28, 20, 36]):
        bx = x0 + 40 + i * 62
        draw.rectangle([bx, y1 - 26 - bh, bx + 34, y1 - 26],
                       fill=(178, 34, 34), outline=INK, width=2)


def scene_estonia(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(200, 220, 235))
    # Estonian flag (blue-black-white) on a pole
    draw.line([x0 + 34, y0 + 16, x0 + 34, y1 - 28], fill=INK, width=4)
    for i, c in enumerate([(0, 114, 206), (0, 0, 0), (255, 255, 255)]):
        draw.rectangle([x0 + 34, y0 + 16 + i * 14, x0 + 96, y0 + 30 + i * 14],
                       fill=c, outline=INK, width=1)
    draw.text((x0 + 140, y0 + 24), "CLOSED", font=font(BOLD, 26), fill=RED)
    # road + closed barrier arm (red/white stripes)
    draw.rectangle([x0, y1 - 28, x1, y1], fill=(90, 90, 90))
    for px in (x0 + 130, x1 - 30):
        draw.rectangle([px - 5, y0 + 66, px + 5, y1 - 28], fill=(240, 240, 240),
                       outline=INK, width=2)
    for i in range(6):
        sx = x0 + 130 + i * 24
        draw.polygon([(sx, y0 + 66), (sx + 24, y0 + 66),
                      (sx + 12, y0 + 86), (sx - 12, y0 + 86)],
                     fill=RED if i % 2 == 0 else (255, 255, 255), outline=INK)
    for wx in range(x0 + 12, x1 - 12, 34):
        draw.line([wx, y1 - 14, wx + 16, y1 - 14], fill=(255, 255, 255), width=3)


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


def scene_trump_putin(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(235, 228, 210))
    # speech bubble
    draw.rounded_rectangle([x0 + 30, y0 + 12, x1 - 30, y0 + 52], radius=12,
                           fill=(255, 255, 255), outline=INK, width=2)
    draw.polygon([(x0 + 90, y0 + 52), (x0 + 110, y0 + 52), (x0 + 96, y0 + 68)],
                 fill=(255, 255, 255), outline=INK)
    draw.text((x0 + 52, y0 + 22), "\u201cTIRED\u201d \u2014 TRUMP",
              font=font(BOLD, 20), fill=RED)
    # two figures shaking hands
    for cx, suit in [(x0 + 95, (18, 42, 78)), (x0 + 205, (90, 20, 20))]:
        draw.ellipse([cx - 22, y0 + 76, cx + 22, y0 + 118], fill=(232, 200, 160),
                     outline=INK, width=2)
        draw.polygon([(cx - 28, y1 - 6), (cx + 28, y1 - 6),
                      (cx + 20, y0 + 118), (cx - 20, y0 + 118)],
                     fill=suit, outline=INK)
    draw.line([x0 + 122, y0 + 126, x0 + 178, y0 + 126],
              fill=(232, 200, 160), width=8)


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


def scene_harris_macron(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(215, 228, 240))
    # French flag
    for i, c in enumerate([(0, 85, 164), (255, 255, 255), (239, 65, 53)]):
        draw.rectangle([x0 + 18 + i * 16, y0 + 14, x0 + 34 + i * 16, y0 + 40],
                       fill=c, outline=INK, width=1)
    # Eiffel Tower silhouette with arched legs
    cx = x0 + 150
    draw.polygon([(cx - 62, y1 - 6), (cx - 14, y0 + 14), (cx + 14, y0 + 14),
                  (cx + 62, y1 - 6)], fill=(70, 70, 90), outline=INK)
    draw.polygon([(cx - 30, y1 - 6), (cx + 30, y1 - 6), (cx, y0 + 66)],
                 fill=(215, 228, 240))
    draw.rectangle([cx - 34, y0 + 78, cx + 34, y0 + 88], fill=(247, 243, 234),
                   outline=INK, width=2)
    draw.rectangle([cx - 18, y0 + 44, cx + 18, y0 + 52], fill=(247, 243, 234),
                   outline=INK, width=2)

TILES = [
    ("ASIAN MARKETS", "Equities tumble as AI selloff deepens",
     scene_markets, (250, 240, 225)),
    ("ESTONIA", "Closes Russia border for 6 months",
     scene_estonia, (200, 220, 235)),
    ("POLAND", "Probes unknown objects at border",
     scene_poland, (210, 225, 200)),
    ("TRUMP ON PUTIN", "\u201cTired\u201d Putin ready for a deal, Trump says",
     scene_trump_putin, (235, 228, 210)),
    ("COP31, ANTALYA", "Final day: draft deal drops all fossil fuels",
     scene_cop, (206, 232, 210)),
    ("PARIS", "Macron receives Harris in courtesy visit",
     scene_harris_macron, (215, 228, 240)),
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
