#!/usr/bin/env python3
"""Render the 19 November 2026 one-day news image (1024x1024 PNG).

Reads tools/stories.json (researched from AP / AFP / Reuters / The Japan
Times / The Hindu / NDTV / Manila Times / SBS coverage of 19 Nov 2026)
and draws a newspaper front page with PIL. Output: entry.png next to
main.ts. Pure stdlib + Pillow; no network.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

W, H = 1024, 1024
PAPER = (248, 244, 234)
INK = (24, 24, 24)
NAVY = (18, 32, 62)
GOLD = (186, 132, 26)
RED = (178, 34, 22)
TEAL = (12, 110, 104)
GREY = (96, 94, 86)
CARD = (255, 255, 255)
BORDER = (214, 206, 188)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def glyph_summit(d, x, y, s, color):
    # Three leaders' chairs: three circles linked by a table line.
    cy = y + s * 0.42
    for i, cx in enumerate((x + s * 0.2, x + s * 0.5, x + s * 0.8)):
        d.ellipse([cx - s * 0.13, cy - s * 0.13, cx + s * 0.13, cy + s * 0.13],
                  outline=color, width=4)
        d.line([cx, cy + s * 0.13, cx, y + s * 0.86], fill=color, width=4)
    d.line([x + s * 0.08, y + s * 0.86, x + s * 0.92, y + s * 0.86],
           fill=color, width=5)


def glyph_game(d, x, y, s, color):
    # Game controller: rounded body, two sticks, four buttons.
    d.rounded_rectangle([x + s * 0.06, y + s * 0.3, x + s * 0.94, y + s * 0.88],
                        radius=int(s * 0.18), outline=color, width=4)
    d.line([x + s * 0.26, y + s * 0.52, x + s * 0.26, y + s * 0.68],
           fill=color, width=4)
    d.line([x + s * 0.18, y + s * 0.6, x + s * 0.34, y + s * 0.6],
           fill=color, width=4)
    for bx, by in ((0.66, 0.52), (0.76, 0.6), (0.66, 0.68), (0.56, 0.6)):
        d.ellipse([x + s * bx - 4, y + s * by - 4, x + s * bx + 4,
                   y + s * by + 4], fill=color)


def glyph_chart(d, x, y, s, color):
    # Rising bars with an arrowhead.
    for i, h in enumerate((0.3, 0.45, 0.6, 0.78)):
        bx = x + s * (0.12 + i * 0.2)
        d.rectangle([bx, y + s * (0.9 - h), bx + s * 0.12, y + s * 0.9],
                    fill=color)
    d.line([x + s * 0.1, y + s * 0.3, x + s * 0.9, y + s * 0.14], fill=color,
           width=4)
    d.polygon([(x + s * 0.9, y + s * 0.14), (x + s * 0.76, y + s * 0.12),
               (x + s * 0.84, y + s * 0.26)], fill=color)


def glyph_deal(d, x, y, s, color):
    # Handshake as two interlocking arcs meeting in the middle.
    d.arc([x + s * 0.06, y + s * 0.2, x + s * 0.62, y + s * 0.8],
          start=300, end=60, fill=color, width=4)
    d.arc([x + s * 0.38, y + s * 0.2, x + s * 0.94, y + s * 0.8],
          start=120, end=240, fill=color, width=4)
    d.line([x + s * 0.5, y + s * 0.5, x + s * 0.5, y + s * 0.86],
           fill=color, width=4)
    d.line([x + s * 0.34, y + s * 0.86, x + s * 0.66, y + s * 0.86],
           fill=color, width=4)


def glyph_art(d, x, y, s, color):
    # Artist's palette: a disc with thumb hole and three dabs.
    cx, cy = x + s * 0.48, y + s * 0.5
    d.ellipse([x + s * 0.08, y + s * 0.1, x + s * 0.88, y + s * 0.9],
              outline=color, width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=color, width=3)
    for dx, dy in ((-0.22, -0.2), (0.16, -0.24), (-0.24, 0.18)):
        d.ellipse([cx + s * dx - 6, cy + s * dy - 6, cx + s * dx + 6,
                   cy + s * dy + 6], fill=color)


def glyph_clash(d, x, y, s, color):
    # Two crossed blades.
    d.line([x + s * 0.12, y + s * 0.18, x + s * 0.88, y + s * 0.82],
           fill=color, width=5)
    d.line([x + s * 0.88, y + s * 0.18, x + s * 0.12, y + s * 0.82],
           fill=color, width=5)
    d.line([x + s * 0.12, y + s * 0.9, x + s * 0.88, y + s * 0.9],
           fill=color, width=4)


def glyph_ship(d, x, y, s, color):
    # Tanker hull on waves.
    d.polygon([(x + s * 0.08, y + s * 0.42), (x + s * 0.92, y + s * 0.42),
               (x + s * 0.78, y + s * 0.66), (x + s * 0.22, y + s * 0.66)],
              fill=color)
    d.rectangle([x + s * 0.3, y + s * 0.24, x + s * 0.46, y + s * 0.42],
                fill=color)
    for wy in (0.78, 0.9):
        d.line([x + s * 0.06, y + s * wy, x + s * 0.94, y + s * wy],
               fill=color, width=3)


GLYPHS = {"summit": glyph_summit, "game": glyph_game, "chart": glyph_chart,
          "deal": glyph_deal, "art": glyph_art, "clash": glyph_clash,
          "ship": glyph_ship}


def main():
    with open(os.path.join(HERE, "stories.json")) as f:
        data = json.load(f)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W / 2, 44), data["masthead"], font=font(SERIF_B, 58),
           fill=(248, 244, 234), anchor="mm")
    d.line([36, 96, W - 36, 96], fill=GOLD, width=3)
    d.text((W / 2, 106), data["date"].upper(), font=font(SANS_B, 19),
           fill=GOLD, anchor="mm")

    # --- lead story -----------------------------------------------------
    lead = data["lead"]
    d.rectangle([28, 140, W - 28, 424], fill=CARD, outline=BORDER, width=2)
    d.text((52, 158), lead["kicker"], font=font(SANS_B, 17), fill=RED)
    d.line([52, 186, 300, 186], fill=RED, width=3)
    for i, line in enumerate(wrap(d, lead["headline"], font(SERIF_B, 38), 640)):
        d.text((52, 200 + i * 46), line, font=font(SERIF_B, 38), fill=INK)
    n_head = len(wrap(d, lead["headline"], font(SERIF_B, 38), 640))
    body_top = 200 + n_head * 46 + 8
    for i, line in enumerate(wrap(d, lead["body"], font(SERIF, 19), 640)):
        d.text((52, body_top + i * 26), line, font=font(SERIF, 19), fill=INK)
    GLYPHS[lead["glyph"]](d, 742, 168, 210, NAVY)
    d.text((847, 412), "XI  •  PUTIN  •  TRUMP", font=font(SANS_B, 15),
           fill=GREY, anchor="mm")

    # --- story grid -----------------------------------------------------
    gx, gy = 28, 440
    cw, ch = 476, 164
    gap = 14
    accents = [TEAL, NAVY, GOLD, RED, TEAL, NAVY]
    for idx, story in enumerate(data["stories"]):
        col, row = idx % 2, idx // 2
        x0 = gx + col * (cw + gap)
        y0 = gy + row * (ch + gap)
        accent = accents[idx]
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD,
                    outline=BORDER, width=2)
        d.rectangle([x0, y0, x0 + 6, y0 + ch], fill=accent)
        GLYPHS[story["glyph"]](d, x0 + 20, y0 + 18, 64, accent)
        d.text((x0 + 100, y0 + 16), story["kicker"], font=font(SANS_B, 14),
               fill=accent)
        for i, line in enumerate(wrap(d, story["headline"],
                                      font(SERIF_B, 22), cw - 116)):
            d.text((x0 + 100, y0 + 38 + i * 27), line,
                   font=font(SERIF_B, 22), fill=INK)
            if i >= 1:
                break
        n = len(wrap(d, story["headline"], font(SERIF_B, 22), cw - 116))
        btop = y0 + 38 + min(n, 2) * 27 + 4
        for i, line in enumerate(wrap(d, story["body"], font(SANS, 15),
                                      cw - 32)):
            if btop + i * 20 > y0 + ch - 22:
                break
            d.text((x0 + 16, btop + i * 20), line, font=font(SANS, 15),
                   fill=(58, 58, 54))

    # --- footer ---------------------------------------------------------
    fy = 440 + 3 * ch + 2 * gap + 12
    d.line([28, fy, W - 28, fy], fill=BORDER, width=2)
    for i, line in enumerate(wrap(d, data["sources_note"], font(SANS, 14),
                                  W - 56)):
        d.text((28, fy + 10 + i * 19), line, font=font(SANS, 14), fill=GREY)

    out = os.path.join(ROOT, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
