#!/usr/bin/env python3
"""Draw the front page of THE DAILY PICTURE for Monday, 23 November 2026.

A newspaper front page, 1024x1024 PNG, drawn entirely in code with Pillow.
No network, no external assets, no photographs. Deterministic: the same
code always produces the same bytes.
"""

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants

W, H = 1024, 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN  # 952

PAPER = (247, 243, 234)
PANEL_BG = (239, 234, 222)
SKY = (216, 226, 233)
INK = (26, 26, 26)
GRAY = (96, 91, 82)
ACCENT = (139, 30, 30)
BLUE = (38, 70, 110)
GOLD = (176, 141, 60)
GREEN = (46, 110, 60)
ORANGE = (214, 110, 30)
YELLOW = (232, 178, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, path, text, size, max_width):
    """Largest font size <= `size` for which `text` fits in `max_width`."""
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, 8)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit in max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def rule(draw, x0, x1, y, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ------------------------------------------------------------------- panels

def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=PANEL_BG,
                   outline=(150, 143, 128), width=1)


def draw_cop_big(draw, x, y, w, h):
    """Globe beside factory smokestacks, and a torn deal document."""
    panel(draw, x, y, w, h)
    # Globe, left.
    gx, gy, gr = x + 74, y + h // 2, 52
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(196, 214, 226),
                 outline=BLUE, width=3)
    draw.ellipse([gx - 21, gy - gr, gx + 21, gy + gr], outline=BLUE, width=2)
    draw.line([(gx - gr, gy), (gx + gr, gy)], fill=BLUE, width=2)
    draw.arc([gx - gr + 8, gy - 25, gx + gr - 8, gy + 25], start=180,
             end=360, fill=BLUE, width=2)
    draw.arc([gx - gr + 8, gy - 25, gx + gr - 8, gy + 25], start=0,
             end=180, fill=BLUE, width=2)
    # Continent blobs.
    draw.ellipse([gx - 34, gy - 30, gx - 12, gy - 12], fill=GREEN)
    draw.ellipse([gx + 6, gy + 8, gx + 30, gy + 28], fill=GREEN)
    draw.ellipse([gx - 8, gy - 38, gx + 12, gy - 24], fill=GREEN)
    # Factory with two stacks, right.
    fx = x + w - 128
    base = y + h - 14
    draw.rectangle([fx + 16, base - 34, fx + 116, base], fill=INK)
    draw.polygon([(fx + 30, base - 34), (fx + 38, base - 62),
                  (fx + 52, base - 62), (fx + 60, base - 34)], fill=INK)
    draw.polygon([(fx + 70, base - 34), (fx + 78, base - 84),
                  (fx + 92, base - 84), (fx + 100, base - 34)], fill=INK)
    draw.rectangle([fx + 78, base - 84, fx + 92, base - 78], fill=ACCENT)
    for wx in (fx + 28, fx + 52, fx + 76, fx + 96):
        draw.rectangle([wx, base - 20, wx + 10, base - 8], fill=YELLOW)
    # Smoke puffs drifting up-left.
    for cx, cy, r in [(fx + 84, base - 96, 8), (fx + 64, base - 106, 11),
                      (fx + 38, base - 112, 9), (fx + 46, base - 70, 7)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GRAY)
    # Torn document in front of the factory base: two halves, jagged split.
    dx, dy = fx - 6, base - 40
    draw.polygon([(dx, dy), (dx + 22, dy), (dx + 14, dy + 14),
                  (dx + 24, dy + 26), (dx, dy + 30)], fill=PAPER,
                 outline=INK)
    draw.polygon([(dx + 30, dy + 2), (dx + 52, dy + 6), (dx + 50, dy + 32),
                  (dx + 28, dy + 28), (dx + 36, dy + 14)], fill=PAPER,
                 outline=INK)
    for ly in (dy + 8, dy + 16, dy + 24):
        draw.line([(dx + 4, ly), (dx + 14, ly)], fill=GRAY, width=2)
        draw.line([(dx + 36, ly + 2), (dx + 47, ly + 3)], fill=GRAY,
                  width=2)


def draw_hormuz_wide(draw, x, y, w, h):
    """Two tankers on a wide sea, fire on the nearer one, drone above."""
    panel(draw, x, y, w, h)
    sea_y = y + int(h * 0.52)
    draw.rectangle([x + 1, sea_y, x + w - 2, y + h - 2], fill=(196, 214, 226))
    for wx in range(x + 10, x + w - 10, 30):
        draw.arc([wx, sea_y + 14, wx + 24, sea_y + 28], start=180,
                 end=360, fill=BLUE, width=2)
    # Far tanker, right.
    hx2, hy2 = x + int(w * 0.66), sea_y - 10
    draw.polygon([(hx2, hy2), (hx2 + 210, hy2), (hx2 + 228, hy2 + 13),
                  (hx2, hy2 + 13)], fill=GRAY)
    draw.rectangle([hx2 + 14, hy2 - 15, hx2 + 44, hy2], fill=GRAY)
    for wx in range(hx2 + 58, hx2 + 200, 20):
        draw.rectangle([wx, hy2 - 6, wx + 9, hy2 - 1], fill=INK)
    # Near tanker, left, with fire on deck.
    hx, hy = x + 26, sea_y - 4
    draw.polygon([(hx, hy), (hx + int(w * 0.44), hy),
                  (hx + int(w * 0.50), hy + 17), (hx, hy + 17)], fill=INK)
    draw.rectangle([hx + 10, hy - 22, hx + 52, hy], fill=INK)
    draw.rectangle([hx + 58, hy - 15, hx + 66, hy], fill=INK)
    for wx in range(hx + 76, hx + int(w * 0.42), 20):
        draw.rectangle([wx, hy - 9, wx + 10, hy - 3], fill=GOLD)
    fx, fy = hx + int(w * 0.26), hy - 6
    draw.polygon([(fx - 16, fy), (fx - 6, fy - 26), (fx + 2, fy - 10),
                  (fx + 10, fy - 30), (fx + 19, fy)], fill=ORANGE)
    draw.polygon([(fx - 7, fy), (fx, fy - 14), (fx + 8, fy)], fill=YELLOW)
    # Smoke from the fire, kept inside the panel.
    for cx, cy, r in [(fx + 12, fy - 36, 6), (fx + 28, fy - 40, 8),
                      (fx + 48, fy - 42, 7)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GRAY)
    # Drone in the sky, centre.
    dx, dy = x + int(w * 0.55), y + 22
    draw.ellipse([dx - 10, dy - 6, dx + 10, dy + 6], fill=INK)
    draw.line([(dx - 20, dy - 10), (dx + 20, dy - 10)], fill=INK, width=2)
    draw.line([(dx - 20, dy + 10), (dx + 20, dy + 10)], fill=INK, width=2)
    draw.line([(dx, dy + 6), (dx, dy + 16)], fill=INK, width=2)
    draw.ellipse([dx - 3, dy + 16, dx + 3, dy + 22], fill=ACCENT)
    # Distant shoreline hills, far right top.
    draw.polygon([(x + w - 190, sea_y), (x + w - 110, y + 26),
                  (x + w - 30, sea_y)], fill=(170, 164, 150))


def draw_warship(draw, x, y, w, h):
    """Grey warship listing at sea, a naval drone above it."""
    panel(draw, x, y, w, h)
    sea_y = y + int(h * 0.60)
    draw.rectangle([x + 1, sea_y, x + w - 2, y + h - 2], fill=(196, 214, 226))
    for wx in range(x + 6, x + w - 6, 22):
        draw.arc([wx, sea_y + 6, wx + 18, sea_y + 16], start=180,
                 end=360, fill=BLUE, width=2)
    # Hull, tilted: bow down to the right.
    hx, hy = x + 18, sea_y - 12
    draw.polygon([(hx, hy), (hx + w - 52, hy + 8), (hx + w - 66, hy + 20),
                  (hx + 8, hy + 15)], fill=GRAY)
    draw.rectangle([hx + 26, hy - 12, hx + 66, hy + 2], fill=GRAY)
    draw.rectangle([hx + 70, hy - 7, hx + 96, hy + 4], fill=GRAY)
    draw.line([(hx + 46, hy - 12), (hx + 46, hy - 24)], fill=INK, width=2)
    draw.line([(hx + 46, hy - 24), (hx + 60, hy - 20)], fill=INK, width=2)
    # Gun barrel forward.
    draw.line([(hx + 96, hy), (hx + 118, hy - 4)], fill=INK, width=3)
    # Splash and smoke at the stern.
    for cx, cy, r in [(hx + 14, hy - 6, 5), (hx + 4, hy - 12, 4),
                      (hx + 24, hy - 14, 6)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 250),
                     outline=BLUE)
    # Naval drone above.
    dx, dy = x + w - 52, y + 14
    draw.ellipse([dx - 8, dy - 5, dx + 8, dy + 5], fill=INK)
    draw.line([(dx - 16, dy - 8), (dx + 16, dy - 8)], fill=INK, width=2)
    draw.line([(dx - 16, dy + 8), (dx + 16, dy + 8)], fill=INK, width=2)
    draw.line([(dx - 26, dy + 14), (dx - 6, dy + 6)], fill=ACCENT, width=2)


def draw_chip(draw, x, y, w, h):
    """AI chip with pins and a circular 'return' arrow around it."""
    panel(draw, x, y, w, h)
    cx, cy = x + w // 2, y + h // 2
    s = 30
    # Pins.
    for i in range(-2, 3):
        off = i * 13
        draw.line([(cx + off, cy - s - 8), (cx + off, cy - s)], fill=INK,
                  width=3)
        draw.line([(cx + off, cy + s), (cx + off, cy + s + 8)], fill=INK,
                  width=3)
        draw.line([(cx - s - 8, cy + off), (cx - s, cy + off)], fill=INK,
                  width=3)
        draw.line([(cx + s, cy + off), (cx + s + 8, cy + off)], fill=INK,
                  width=3)
    # Body and core.
    draw.rectangle([cx - s, cy - s, cx + s, cy + s], fill=INK)
    draw.rectangle([cx - 15, cy - 15, cx + 15, cy + 15], fill=GOLD)
    draw.rectangle([cx - 7, cy - 7, cx + 7, cy + 7], fill=INK)
    # Small return arrow in the panel's top-left corner (the CEO returns).
    draw.arc([x + 8, y + 6, x + 46, y + 44], start=60, end=300,
             fill=ACCENT, width=4)
    draw.polygon([(x + 10, y + 22), (x + 20, y + 18), (x + 16, y + 28)],
                 fill=ACCENT)


def draw_spain(draw, x, y, w, h):
    """Spanish flag on a pole beside a small courthouse front."""
    panel(draw, x, y, w, h)
    base = y + h - 8
    # Courthouse, right.
    bx = x + w - 104
    draw.polygon([(bx, y + 30), (bx + 46, y + 12), (bx + 92, y + 30)],
                 fill=INK)
    draw.rectangle([bx + 4, y + 30, bx + 88, y + 38], fill=INK)
    for i in range(4):
        cxp = bx + 14 + i * 22
        draw.rectangle([cxp, y + 38, cxp + 8, base - 8], fill=INK)
    draw.rectangle([bx, base - 8, bx + 92, base], fill=INK)
    # Flag pole, left.
    px = x + 22
    draw.line([(px, y + 10), (px, base)], fill=INK, width=3)
    draw.ellipse([px - 3, y + 6, px + 3, y + 12], fill=GOLD)
    # Flag: red-yellow-red horizontal bands, waving.
    fw, fh = 74, 44
    fy = y + 12
    draw.rectangle([px + 2, fy, px + 2 + fw, fy + fh // 4], fill=ACCENT)
    draw.rectangle([px + 2, fy + fh // 4, px + 2 + fw, fy + 3 * fh // 4],
                   fill=YELLOW)
    draw.rectangle([px + 2, fy + 3 * fh // 4, px + 2 + fw, fy + fh],
                   fill=ACCENT)
    draw.rectangle([px + 12, fy + fh // 4 + 4, px + 24, fy + 3 * fh // 4 - 4],
                   outline=INK, width=1)


def draw_warrant(draw, x, y, w, h):
    """Arrest warrant sheet with a red seal, and handcuffs."""
    panel(draw, x, y, w, h)
    # Paper sheet, left.
    px, py, pw, ph = x + 18, y + 8, 74, h - 16
    draw.rectangle([px, py, px + pw, py + ph], fill=(252, 250, 244),
                   outline=INK, width=2)
    title_f = font(SANS_B, 10)
    draw.text((px + 8, py + 6), "WARRANT", font=title_f, fill=ACCENT)
    for i, lw in enumerate((58, 58, 44, 58, 36)):
        ly = py + 24 + i * 8
        draw.line([(px + 8, ly), (px + 8 + lw, ly)], fill=GRAY, width=2)
    # Red seal.
    sx, sy = px + pw - 18, py + ph - 16
    draw.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], outline=ACCENT, width=3)
    draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=ACCENT)
    # Handcuffs, right: two rings and a chain.
    c1 = (x + w - 62, y + h // 2 - 8)
    c2 = (x + w - 30, y + h // 2 + 12)
    for cx, cy in (c1, c2):
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=INK,
                     width=4)
        draw.rectangle([cx - 4, cy - 19, cx + 4, cy - 11], fill=INK)
    draw.line([c1[0] + 8, c1[1] + 8, c2[0] - 8, c2[1] - 8], fill=INK,
              width=3)


def draw_cobalt(draw, x, y, w, h):
    """Mine cart of cobalt-blue ore behind a striped halt barrier."""
    panel(draw, x, y, w, h)
    base = y + h - 10
    # Rail track.
    draw.line([(x + 10, base), (x + w - 10, base)], fill=INK, width=3)
    for tx in range(x + 18, x + w - 12, 18):
        draw.line([(tx, base), (tx, base + 4)], fill=INK, width=2)
    # Cart.
    cx0, cy0 = x + 26, base - 26
    draw.polygon([(cx0, cy0), (cx0 + 84, cy0), (cx0 + 74, base - 4),
                  (cx0 + 10, base - 4)], fill=INK)
    for wx in (cx0 + 22, cx0 + 62):
        draw.ellipse([wx - 7, base - 8, wx + 7, base + 6], fill=INK)
        draw.ellipse([wx - 3, base - 4, wx + 3, base + 2], fill=GRAY)
    # Cobalt-blue ore lumps in the cart.
    for ox, oy, r in [(cx0 + 18, cy0 - 6, 9), (cx0 + 38, cy0 - 10, 11),
                      (cx0 + 60, cy0 - 6, 9), (cx0 + 48, cy0 - 2, 8)]:
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=BLUE)
    # Halt barrier across the track, right.
    bx = x + w - 66
    draw.rectangle([bx, y + 14, bx + 7, base], fill=INK)
    bar_y = y + 22
    draw.rectangle([bx - 44, bar_y, bx + 4, bar_y + 10], fill=(250, 250, 250),
                   outline=INK, width=2)
    for i in range(3):
        sx = bx - 44 + i * 16
        draw.polygon([(sx, bar_y + 10), (sx + 8, bar_y), (sx + 16, bar_y),
                      (sx + 8, bar_y + 10)], fill=ACCENT)


def draw_school(draw, x, y, w, h):
    """Schoolhouse with a bell, and an alert envelope."""
    panel(draw, x, y, w, h)
    base = y + h - 8
    # Building.
    bx, bw = x + 16, 96
    draw.rectangle([bx, y + 24, bx + bw, base], fill=INK)
    draw.polygon([(bx - 6, y + 24), (bx + bw // 2, y + 6),
                  (bx + bw + 6, y + 24)], fill=ACCENT)
    # Bell tower.
    draw.rectangle([bx + bw // 2 - 8, y + 0, bx + bw // 2 + 8, y + 10],
                   fill=INK)
    draw.ellipse([bx + bw // 2 - 5, y + 2, bx + bw // 2 + 5, y + 12],
                 fill=GOLD)
    # Door and windows.
    draw.rectangle([bx + bw // 2 - 9, base - 24, bx + bw // 2 + 9, base],
                   fill=PAPER)
    for wx in (bx + 12, bx + bw - 24):
        for wy in (y + 34, y + 50):
            draw.rectangle([wx, wy, wx + 12, wy + 12], fill=YELLOW)
    # Alert envelope, right.
    ex, ey, ew, eh = x + w - 92, y + 18, 76, 48
    draw.rectangle([ex, ey, ex + ew, ey + eh], fill=(252, 250, 244),
                   outline=INK, width=2)
    draw.line([(ex, ey), (ex + ew // 2, ey + 22)], fill=INK, width=2)
    draw.line([(ex + ew, ey), (ex + ew // 2, ey + 22)], fill=INK, width=2)
    # Warning triangle on the envelope.
    tx, ty = ex + ew // 2, ey + eh - 8
    draw.polygon([(tx, ty - 16), (tx - 9, ty), (tx + 9, ty)], fill=YELLOW,
                 outline=INK)
    draw.line([(tx, ty - 12), (tx, ty - 5)], fill=INK, width=2)
    draw.ellipse([tx - 1, ty - 3, tx + 1, ty - 1], fill=INK)


def draw_capitol(draw, x, y, w, h):
    """US Capitol: dome, wings and steps."""
    panel(draw, x, y, w, h)
    base = y + h - 8
    cx = x + w // 2
    # Wings.
    draw.rectangle([cx - 92, base - 22, cx - 18, base - 6], fill=INK)
    draw.rectangle([cx + 18, base - 22, cx + 92, base - 6], fill=INK)
    for wx in range(cx - 86, cx - 24, 14):
        draw.rectangle([wx, base - 17, wx + 6, base - 10], fill=YELLOW)
    for wx in range(cx + 26, cx + 84, 14):
        draw.rectangle([wx, base - 17, wx + 6, base - 10], fill=YELLOW)
    # Central block and columns.
    draw.rectangle([cx - 26, base - 30, cx + 26, base - 6], fill=INK)
    for i in range(4):
        cxp = cx - 19 + i * 13
        draw.rectangle([cxp, base - 26, cxp + 5, base - 8], fill=PAPER)
    # Dome.
    draw.arc([cx - 24, base - 62, cx + 24, base - 14], start=180, end=360,
             fill=INK, width=5)
    draw.rectangle([cx - 26, base - 32, cx + 26, base - 28], fill=INK)
    draw.line([(cx, base - 62), (cx, base - 72)], fill=INK, width=3)
    draw.ellipse([cx - 3, base - 76, cx + 3, base - 70], fill=GOLD)
    # Steps.
    draw.rectangle([cx - 34, base - 6, cx + 34, base - 2], fill=INK)
    draw.rectangle([cx - 44, base - 2, cx + 44, base], fill=INK)


# -------------------------------------------------------------------- page

def build():
    """Draw the front page and write entry.png next to this file."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ------------------------------------------------------
    rule(d, MARGIN, W - MARGIN, 24, width=2)
    title_f = fit_font(d, SERIF_B, "THE DAILY PICTURE", 64, CONTENT_W)
    centered(d, W // 2, 34, "THE DAILY PICTURE", title_f)
    date_f = font(SANS_B, 20)
    centered(d, W // 2, 104, "MONDAY, 23 NOVEMBER 2026", date_f, fill=ACCENT)
    small_f = font(SANS, 13)
    d.text((MARGIN, 106), "EST. 2026", font=small_f, fill=GRAY)
    d.text((W - MARGIN - d.textlength("NO. 327", font=small_f), 106),
           "NO. 327", font=small_f, fill=GRAY)
    rule(d, MARGIN, W - MARGIN, 132, width=4)
    rule(d, MARGIN, W - MARGIN, 138, width=1)

    # ---- Lead story: COP31 ends without a deal --------------------------
    lead_x, lead_w = MARGIN, 628
    y = 152
    kick_f = font(SANS_B, 15)
    d.text((lead_x, y), "ANTALYA  ·  COP31 CLIMATE SUMMIT", font=kick_f,
           fill=ACCENT)
    y = 176
    head_f = fit_font(d, SERIF_B, "CLIMATE TALKS END", 36, lead_w)
    line_h = int(head_f.size * 1.24)
    for line in ["CLIMATE TALKS END",
                 "WITHOUT A DEAL"]:
        d.text((lead_x, y), line, font=head_f, fill=INK)
        y += line_h
    y += 6
    stand_f = font(SERIF, 17)
    y = text_block(d, lead_x, y,
                   "The UN's COP31 summit in Turkey closes as the longest "
                   "climate conference in history, after the EU and others "
                   "reject the final draft over fossil fuels and money.",
                   stand_f, lead_w, leading=21)
    # COP illustration, right of the lead headline.
    cop_x, cop_w = 680, W - MARGIN - 680  # 308
    draw_cop_big(d, cop_x, 152, cop_w, 150)
    cap_f = font(SERIF, 13)
    text_block(d, cop_x, 308,
               "Two weeks of talks in Antalya end with the draft deal "
               "torn up.",
               cap_f, cop_w, fill=GRAY, leading=16)

    rule(d, MARGIN, W - MARGIN, 360, width=2)

    # ---- Second lead: Hormuz -------------------------------------------
    y = 374
    d.text((MARGIN, y), "STRAIT OF HORMUZ  ·  IRAN", font=kick_f,
           fill=ACCENT)
    y = 398
    hor_head_f = font(SERIF_B, 28)
    d.text((MARGIN, y), "TANKERS ATTACKED IN HORMUZ AS IRAN STRIKES WIDEN",
           font=hor_head_f, fill=INK)
    y = 436
    sub_f = font(SERIF, 17)
    y = text_block(d, MARGIN, y,
                   "At least three oil tankers are attacked in the strait "
                   "and an Iranian strike hits an industrial site in "
                   "Bahrain, as Tehran vows to confront the US naval "
                   "blockade with all available tools.",
                   sub_f, CONTENT_W, leading=21)
    y += 4
    draw_hormuz_wide(d, MARGIN, y, CONTENT_W, 116)
    y += 116 + 6
    text_block(d, MARGIN, y,
               "A tanker burns in the Strait of Hormuz as regional "
               "strikes escalate.",
               cap_f, CONTENT_W, fill=GRAY, leading=16)
    y += 22
    rule(d, MARGIN, W - MARGIN, y, width=2)
    y += 10

    # ---- Around the world ----------------------------------------------
    sec_f = font(SANS_B, 14)
    sec_label = "—  AROUND THE WORLD  —"
    centered(d, W // 2, y, sec_label, sec_f)
    y += 26

    def item(x, iy, w, draw_fn, headline, caption, icon_h=64):
        draw_fn(d, x, iy, w, icon_h)
        hy = iy + icon_h + 6
        hf = font(SANS_B, 15)
        hy = text_block(d, x, hy, headline, hf, w, leading=18)
        cf = font(SERIF, 12)
        text_block(d, x, hy + 2, caption, cf, w, fill=GRAY, leading=15)

    gap = 16
    col_w4 = (CONTENT_W - 3 * gap) // 4  # 226
    row_a_y = y
    x4 = [MARGIN + i * (col_w4 + gap) for i in range(4)]
    item(x4[0], row_a_y, col_w4, draw_warship,
         "Ukraine sinks Russian warship off Libya",
         "Kyiv says naval drones sank the corvette Mercury at "
         "Benghazi; Russian strikes kill 15 near Kyiv.")
    item(x4[1], row_a_y, col_w4, draw_chip,
         "Nvidia reinstates Huang as CEO",
         "Jensen Huang returns weeks after his abrupt exit, in a "
         "reversal pressed by President Trump.")
    item(x4[2], row_a_y, col_w4, draw_spain,
         "Court clears Catalan leader's return",
         "Spain's Supreme Court shelves the case against Carles "
         "Puigdemont, ending nearly a decade of exile.")
    item(x4[3], row_a_y, col_w4, draw_warrant,
         "Bangladesh vows to arrest Hasina",
         "Dhaka says the exiled ex-PM will be jailed if she returns "
         "from India.")

    row_b_y = row_a_y + 158
    col_w3 = (CONTENT_W - 2 * gap) // 3  # 306
    x3 = [MARGIN + i * (col_w3 + gap) for i in range(3)]
    item(x3[0], row_b_y, col_w3, draw_cobalt,
         "Congo halts cobalt exports again",
         "The world's top producer suspends exports from 30 November "
         "to tackle oversupply and weak prices.",
         icon_h=56)
    item(x3[1], row_b_y, col_w3, draw_school,
         "Bomb threats hit 450 German schools",
         "Emailed threats disrupt schools across Germany on Monday "
         "morning, Bild reports.",
         icon_h=56)
    item(x3[2], row_b_y, col_w3, draw_capitol,
         "Democrats win biggest House majority since 1992",
         "At least 258 seats in the midterm count, as Trump moves to "
         "curb the new majority's oversight.",
         icon_h=56)

    # ---- Footer ----------------------------------------------------------
    foot_f = font(SANS, 11)
    centered(d, W // 2, H - 22,
             "THE DAILY PICTURE — Monday, 23 November 2026 — "
             "The day's world news, drawn in one page.",
             foot_f, fill=GRAY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG")
    return out


if __name__ == "__main__":
    print(build())
