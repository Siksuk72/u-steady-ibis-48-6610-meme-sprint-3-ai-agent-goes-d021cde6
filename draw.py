#!/usr/bin/env python3
"""Paint entry.png for the Meme Sprint 3 entry.

Opens hero.png (AI illustration, no text), resizes to 1024x1024, draws
the two caption lines in bold white Impact-style sans with a black
outline, top and bottom, and writes entry.png (PNG, under 1 MiB).

Deterministic, no network. Run: python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SIZE = 1024
MAX_BYTES = 1_048_576

TOP_LINES = ["MY AGENT WENT ROGUE"]
BOTTOM_LINES = ["NOW IT'S ENTERING BOUNTIES", "AGAINST ME"]


def fit_font(draw, lines, max_width, start_size):
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size)
        if all(draw.textlength(line, font=font) <= max_width for line in lines):
            return font
        size -= 2
    return ImageFont.truetype(FONT_PATH, 20)


def draw_caption(draw, lines, y_top, max_width):
    font = fit_font(draw, lines, max_width, 92)
    line_h = int(font.size * 1.08)
    y = y_top
    for line in lines:
        w = draw.textlength(line, font=font)
        x = (SIZE - w) / 2
        draw.text(
            (x, y),
            line,
            font=font,
            fill="white",
            stroke_width=max(4, font.size // 12),
            stroke_fill="black",
        )
        y += line_h
    return y


def main():
    img = Image.open(os.path.join(HERE, "hero.png")).convert("RGB")
    img = img.resize((SIZE, SIZE), Image.LANCZOS)

    # Subtle dark bands so the outlined captions stay readable over the art.
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([0, 0, SIZE, 150], fill=(0, 0, 0, 110))
    od.rectangle([0, SIZE - 210, SIZE, SIZE], fill=(0, 0, 0, 110))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(img)
    margin = 28
    max_width = SIZE - 2 * margin

    draw_caption(draw, TOP_LINES, 30, max_width)

    bottom_font = fit_font(draw, BOTTOM_LINES, max_width, 84)
    total_h = int(bottom_font.size * 1.08) * len(BOTTOM_LINES)
    draw_caption(draw, BOTTOM_LINES, SIZE - 24 - total_h, max_width)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    n = os.path.getsize(out)
    print(f"entry.png: {img.size[0]}x{img.size[1]}, {n} bytes")
    assert n <= MAX_BYTES, f"entry.png too large: {n} > {MAX_BYTES}"


if __name__ == "__main__":
    main()
