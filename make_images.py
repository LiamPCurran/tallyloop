"""Produce the Tallyloop dashboard images from the rendered HTML mockup.

before/: one huge, unoptimized PNG (typical of AI-builder exports).
after/:  WebP at 1200px and 640px for srcset, plus an OG image.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent


def font(size, bold=False):
    for n in (["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]):
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    return ImageFont.load_default()


# The dashboard is an HTML mockup (mockup/dashboard.html) rendered at 2x to mockup/dashboard-2400.png with headless Chrome.
big = Image.open(ROOT / "mockup" / "dashboard-2400.png").convert("RGB")
(ROOT / "docs" / "before" / "assets").mkdir(parents=True, exist_ok=True)
(ROOT / "docs" / "assets").mkdir(parents=True, exist_ok=True)
big.save(ROOT / "docs" / "before" / "assets" / "dashboard-screenshot-final-v3.png", compress_level=1)
small = big.resize((1200, 750), Image.LANCZOS)
small.save(ROOT / "docs" / "assets" / "dashboard-1200.webp", quality=80, method=6)
small.resize((640, 400), Image.LANCZOS).save(ROOT / "docs" / "assets" / "dashboard-640.webp", quality=80, method=6)

og = Image.new("RGB", (1200, 630), "#1e1b3a")
od = ImageDraw.Draw(og)
od.rounded_rectangle([80, 90, 150, 160], radius=16, fill="#7c5cff")
od.text((170, 92), "Tallyloop", font=font(56, True), fill="white")
od.text((80, 230), "Time tracking and invoicing", font=font(60, True), fill="white")
od.text((80, 310), "for freelancers who'd rather be working.", font=font(44), fill="#b9b4d9")
od.text((80, 520), "Concept project · fictional product", font=font(28), fill="#ff8a3d")
og.save(ROOT / "docs" / "assets" / "og.png", optimize=True)
for p in sorted(ROOT.rglob("*.png")) + sorted(ROOT.rglob("*.webp")):
    print(p.relative_to(ROOT), p.stat().st_size)

