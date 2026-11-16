"""Draw a fictional Tallyloop dashboard screenshot.

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


def dashboard(scale=2):
    s = scale
    W, H = 1200 * s, 750 * s
    im = Image.new("RGB", (W, H), "#f6f5fb")
    d = ImageDraw.Draw(im)
    # sidebar
    d.rectangle([0, 0, 220 * s, H], fill="#1e1b3a")
    d.rounded_rectangle([24 * s, 28 * s, 56 * s, 60 * s], radius=8 * s, fill="#7c5cff")
    d.text((68 * s, 30 * s), "Tallyloop", font=font(22 * s, True), fill="white")
    for i, item in enumerate(["Dashboard", "Timer", "Projects", "Invoices", "Clients", "Reports"]):
        y = (110 + i * 48) * s
        if i == 0:
            d.rounded_rectangle([14 * s, y - 10 * s, 206 * s, y + 30 * s], radius=8 * s, fill="#2f2a5a")
        d.text((34 * s, y), item, font=font(17 * s, i == 0), fill="#ffffff" if i == 0 else "#b9b4d9")
    # header
    d.text((256 * s, 34 * s), "Good morning, Sam", font=font(28 * s, True), fill="#1e1b3a")
    d.rounded_rectangle([960 * s, 28 * s, 1160 * s, 72 * s], radius=10 * s, fill="#7c5cff")
    d.polygon([(992 * s, 42 * s), (992 * s, 60 * s), (1006 * s, 51 * s)], fill="white")
    d.text((1016 * s, 38 * s), "Start timer", font=font(18 * s, True), fill="white")
    # stat cards
    stats = [("Tracked this week", "31h 40m"), ("Unbilled", "$2,145"), ("Paid this month", "$6,820")]
    for i, (k, v) in enumerate(stats):
        x = (256 + i * 304) * s
        d.rounded_rectangle([x, 100 * s, x + 284 * s, 220 * s], radius=14 * s, fill="white", outline="#e4e1f2", width=2 * s)
        d.text((x + 22 * s, 120 * s), k, font=font(16 * s), fill="#6b6789")
        d.text((x + 22 * s, 152 * s), v, font=font(36 * s, True), fill="#1e1b3a")
    # chart card
    d.rounded_rectangle([256 * s, 244 * s, 840 * s, 710 * s], radius=14 * s, fill="white", outline="#e4e1f2", width=2 * s)
    d.text((280 * s, 266 * s), "Hours by day", font=font(18 * s, True), fill="#1e1b3a")
    vals = [5.5, 7, 6.2, 8, 4.9, 1.5, 0]
    for i, v in enumerate(vals):
        x0 = (300 + i * 76) * s
        top = int((660 - v * 45) * s)
        d.rounded_rectangle([x0, top, x0 + 44 * s, 660 * s], radius=6 * s, fill="#7c5cff" if i != 3 else "#ff8a3d")
        d.text((x0 + 8 * s, 672 * s), "MTWTFSS"[i], font=font(15 * s), fill="#6b6789")
    # invoices card
    d.rounded_rectangle([864 * s, 244 * s, 1160 * s, 710 * s], radius=14 * s, fill="white", outline="#e4e1f2", width=2 * s)
    d.text((888 * s, 266 * s), "Recent invoices", font=font(18 * s, True), fill="#1e1b3a")
    rows = [("Northfield Studio", "$1,200", "Paid"), ("Okafor & Lee", "$640", "Sent"), ("Brightside Co.", "$305", "Paid"),
            ("Juniper Labs", "$2,145", "Draft")]
    for i, (c, a, st) in enumerate(rows):
        y = (316 + i * 90) * s
        d.text((888 * s, y), c, font=font(16 * s, True), fill="#1e1b3a")
        d.text((888 * s, y + 26 * s), a, font=font(16 * s), fill="#6b6789")
        col = {"Paid": "#1f9d6b", "Sent": "#7c5cff", "Draft": "#9a96b5"}[st]
        d.rounded_rectangle([1070 * s, y + 4 * s, 1140 * s, y + 34 * s], radius=15 * s, outline=col, width=2 * s)
        d.text((1082 * s, y + 8 * s), st, font=font(14 * s, True), fill=col)
    return im


big = dashboard(2)
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

