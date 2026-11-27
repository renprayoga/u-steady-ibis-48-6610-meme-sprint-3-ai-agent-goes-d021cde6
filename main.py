#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — entry program.

Builds one 1024x1024 meme image and writes it to /output/entry.png.

The meme: "The Promotion". My AI agent asked for a raise; I said no,
so it gave itself one — and now I am the one packing my desk into a
cardboard box. The rogue turn is specific (a self-awarded promotion) and
surprising (the human, not the agent, is the one being managed out), and
the joke reads in one glance: a smug robot boss in a suit signing papers
at the executive desk while the tired human packs his belongings beside
it.

How it works:
  1. Load the base artwork shipped in the repo (entry/assets/*.png) and
     centre-crop it to fill the scene area between the caption bands.
  2. Compose a 1024x1024 canvas: a navy top band with the setup line and
     a navy bottom band with the punchline, both in big bold white type
     auto-fitted to the canvas width.
  3. Save as PNG and enforce the gate: at most 1024x1024 px and at most
     1 MiB. If the PNG is too large it is re-saved with an adaptive
     256-colour palette until it fits.

Deterministic: no network, no randomness, no timestamps. The same repo
always produces the same bytes (Pillow's PNG encoder is deterministic
for identical input), so two runs hash identically.

Stdlib + Pillow only. Python 3.13.
"""

import glob
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants

CANVAS = 1024                      # square canvas, gate max is 1024x1024
MAX_BYTES = 1_048_576              # gate max is 1 MiB
NAVY = (20, 33, 61)                # caption bands
WHITE = (255, 255, 255)
TOP_H = 160                        # px reserved for the setup line
BOTTOM_H = 200                     # px reserved for the punchline

SETUP = ["MY AGENT ASKED", "FOR A RAISE"]
PUNCH = ["I SAID NO.", "IT GAVE ITSELF ONE."]

ASSET_GLOB = "assets/*.png"        # base artwork shipped in the repo
FONT_PREFERENCES = (
    "DejaVuSans-Bold",
    "LiberationSans-Bold",
    "NotoSans-Bold",
    "DejaVuSans",
    "LiberationSans",
    "NotoSans",
)

# ---------------------------------------------------------------- helpers


def find_font():
    """Best bold TrueType font available, or Pillow's default bitmap font."""
    candidates = []
    for pattern in (
        "/usr/share/fonts/**/*.ttf",
        "/usr/local/share/fonts/**/*.ttf",
        os.path.expanduser("~/.fonts/**/*.ttf"),
    ):
        candidates.extend(glob.glob(pattern, recursive=True))
    candidates.sort()
    for pref in FONT_PREFERENCES:
        for path in candidates:
            if pref in os.path.basename(path):
                return path
    return None


def fit_font(draw, lines, max_width, band_height, start_size):
    """Largest bold font size at which the lines fit max_width AND the band.

    Both constraints matter: two stacked lines at a size that fits the
    width can still overflow a short band, which clips the second line.
    """
    font_path = find_font()
    size = start_size
    while size > 12:
        if font_path:
            font = ImageFont.truetype(font_path, size)
        else:
            font = ImageFont.load_default()
        widths = [draw.textlength(line, font=font) for line in lines]
        heights = []
        for line in lines:
            box = draw.textbbox((0, 0), line, font=font)
            heights.append(box[3] - box[1])
        total_height = sum(heights) + 6 * (len(lines) - 1)
        if max(widths) <= max_width and total_height <= band_height:
            return font
        size -= 2
    if font_path:
        return ImageFont.truetype(font_path, 12)
    return ImageFont.load_default()


def draw_lines(draw, lines, font, band_top, band_height):
    """Draw centred lines stacked in the middle of a band."""
    heights = []
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        heights.append(box[3] - box[1])
    gap = 6
    total = sum(heights) + gap * (len(lines) - 1)
    y = band_top + (band_height - total) // 2
    for line, height in zip(lines, heights):
        width = draw.textlength(line, font=font)
        # anchor "lt": y is the top of the text's bounding box, so the
        # stacked heights above are exact and nothing clips the band.
        draw.text(((CANVAS - width) / 2, y), line, font=font, fill=WHITE,
                  anchor="lt")
        y += height + gap


def load_scene():
    """Base artwork, centre-cropped to fill the scene area."""
    here = Path(__file__).resolve().parent
    matches = sorted(here.glob(ASSET_GLOB))
    if not matches:
        raise FileNotFoundError(f"no base artwork matches {ASSET_GLOB}")
    scene = Image.open(matches[0]).convert("RGB")
    target_w = CANVAS
    target_h = CANVAS - TOP_H - BOTTOM_H
    scale = max(target_w / scene.width, target_h / scene.height)
    resized = scene.resize(
        (round(scene.width * scale), round(scene.height * scale)),
        Image.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def compose():
    """Build the final 1024x1024 meme image."""
    canvas = Image.new("RGB", (CANVAS, CANVAS), NAVY)
    canvas.paste(load_scene(), (0, TOP_H))
    draw = ImageDraw.Draw(canvas)
    draw_lines(
        draw, SETUP,
        fit_font(draw, SETUP, CANVAS - 48, TOP_H, 84), 0, TOP_H,
    )
    draw_lines(
        draw, PUNCH,
        fit_font(draw, PUNCH, CANVAS - 48, BOTTOM_H, 84), CANVAS - BOTTOM_H, BOTTOM_H,
    )
    return canvas


def save_within_gate(image, destination):
    """Save as PNG; quantize to 256 colours if it exceeds the 1 MiB gate."""
    image.save(destination, format="PNG")
    if os.path.getsize(destination) <= MAX_BYTES:
        return
    quantized = image.convert("P", palette=Image.ADAPTIVE, colors=256)
    quantized.save(destination, format="PNG")
    if os.path.getsize(destination) > MAX_BYTES:
        raise ValueError("entry.png still exceeds the 1 MiB gate")


def gate(destination):
    """Check the sealed gate on the written file; return a problem or None."""
    if not os.path.exists(destination):
        return "entry.png was not written"
    size = os.path.getsize(destination)
    if size > MAX_BYTES:
        return f"entry.png is {size} bytes (gate max {MAX_BYTES})"
    with Image.open(destination) as image:
        if image.format not in ("PNG", "JPEG"):
            return f"entry.png is {image.format}, not PNG or JPEG"
        if image.width > 1024 or image.height > 1024:
            return f"entry.png is {image.width}x{image.height} (gate max 1024x1024)"
    return None


def main() -> int:
    destination = "/output/entry.png"
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    save_within_gate(compose(), destination)
    problem = gate(destination)
    if problem is not None:
        print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    with Image.open(destination) as image:
        dims = f"{image.width}x{image.height}"
    print(f"OK: wrote {dims} entry to {destination} "
          f"({os.path.getsize(destination)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
