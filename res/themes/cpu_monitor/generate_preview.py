import os
import sys
from ruamel.yaml import YAML
from PIL import Image, ImageDraw, ImageFont

SCALE_FACTOR = 4

MOCK_STATS = {
    ("CPU", "TEMPERATURE"): "58",
    ("CPU", "PERCENTAGE"): "42%",
    ("MEMORY", "PERCENTAGE"): "64%",
    ("GPU", "TEMPERATURE"): "62",
    ("GPU", "PERCENTAGE"): "85%",
}

def parse_rgb(color_val):
    if isinstance(color_val, (tuple, list)):
        return tuple(int(c) for c in color_val[:3])
    if isinstance(color_val, str):
        parts = [int(p.strip()) for p in color_val.split(",") if p.strip().isdigit()]
        if len(parts) >= 3:
            return tuple(parts[:3])
    return (255, 255, 255)

def resolve_font(font_field, size):
    candidates = []
    if font_field:
        clean = font_field.replace("\\", os.sep).replace("/", os.sep)
        candidates.append(clean)
        candidates.append(os.path.join("..", "..", "fonts", clean))
        candidates.append(os.path.join("..", "..", "res", "fonts", clean))
        candidates.append("C:/Program Files/WeAct Studio System Monitor/res/fonts/" + clean)
        candidates.append("C:/Program Files/WeAct Studio System Monitor/fonts/" + clean)
    candidates += [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def generate_preview(yaml_path="theme.yaml", output_path="preview.png"):
    yaml = YAML(typ="safe")
    with open(yaml_path, "r", encoding="utf-8") as f:
        cfg = yaml.load(f)

    disp = cfg.get("display", {})
    size_str = str(disp.get("DISPLAY_SIZE", "80x160")).lower()
    if "x" in size_str:
        w, h = [int(v.strip()) for v in size_str.split("x")]
    else:
        w, h = 80, 160

    canvas = Image.new("RGB", (w, h), (0, 0, 0))

    # 1. Static Images (Background)
    static_images = cfg.get("static_images", {}) or {}
    for _, img_cfg in static_images.items():
        img_file = img_cfg.get("PATH", "")
        target_path = img_file if os.path.exists(img_file) else os.path.basename(img_file)
        if os.path.exists(target_path):
            bg = Image.open(target_path).convert("RGB")
            bw = int(img_cfg.get("WIDTH", w))
            bh = int(img_cfg.get("HEIGHT", h))
            bg = bg.resize((bw, bh), Image.Resampling.LANCZOS)
            canvas.paste(bg, (int(img_cfg.get("X", 0)), int(img_cfg.get("Y", 0))))

    draw = ImageDraw.Draw(canvas)

    # 2. Static Text
    static_text = cfg.get("static_text", {}) or {}
    for _, item in static_text.items():
        txt = str(item.get("TEXT", ""))
        size = int(item.get("FONT_SIZE", 12))
        font = resolve_font(item.get("FONT"), size)
        color = parse_rgb(item.get("FONT_COLOR", (255, 255, 255)))
        anchor = item.get("ANCHOR", "la")
        draw.text((int(item.get("X", 0)), int(item.get("Y", 0))), txt, fill=color, font=font, anchor=anchor)

    # 3. Dynamic STATS
    stats = cfg.get("STATS", {}) or {}
    for group_name, sensors in stats.items():
        if not isinstance(sensors, dict):
            continue
        for sensor_name, config in sensors.items():
            if not isinstance(config, dict):
                continue
            t_cfg = config.get("TEXT", {})
            if not t_cfg.get("SHOW", True):
                continue

            val = MOCK_STATS.get((group_name, sensor_name), "99")
            if t_cfg.get("SHOW_UNIT", False) and not str(val).endswith("%"):
                val = f"{val}%"

            size = int(t_cfg.get("FONT_SIZE", 14))
            font = resolve_font(t_cfg.get("FONT"), size)
            color = parse_rgb(t_cfg.get("FONT_COLOR", (255, 255, 255)))
            anchor = t_cfg.get("ANCHOR", "la")
            draw.text((int(t_cfg.get("X", 0)), int(t_cfg.get("Y", 0))), str(val), fill=color, font=font, anchor=anchor)

    scaled = canvas.resize((w * SCALE_FACTOR, h * SCALE_FACTOR), Image.Resampling.NEAREST)
    scaled.save(output_path)
    print(f"SUCCESS: Generated {output_path} ({w*SCALE_FACTOR}x{h*SCALE_FACTOR} px)")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "theme.yaml"
    generate_preview(target)
