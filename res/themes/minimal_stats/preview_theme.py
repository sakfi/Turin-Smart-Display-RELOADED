import sys
import os
from ruamel.yaml import YAML
from PIL import Image, ImageDraw, ImageFont

SCALE_FACTOR = 4

MOCK_DATA = {
    "cpu_temperature": 54.0,
    "cpu_percent": 38.0,
    "gpu_temperature": 62.0,
    "gpu_percent": 84.0,
    "ram_percent": 58.0,
    "gpu_memory_percent": 71.0,
    "gpu_frequency": 2450.0,
}

def load_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def render_theme(yaml_path):
    yaml = YAML(typ="safe")
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.load(f)

    disp = config.get("display", {})
    w = int(disp.get("width", 80))
    h = int(disp.get("height", 160))
    bg_color = disp.get("background", "#000000")

    canvas = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(canvas)

    elements = (config.get("static_elements") or []) + (config.get("dynamic_elements") or [])

    for el in elements:
        el_type = el.get("type", "")

        if el_type == "line":
            draw.line(
                [(el.get("x1", 0), el.get("y1", 0)), (el.get("x2", 0), el.get("y2", 0))],
                fill=el.get("color", "#FFFFFF"),
                width=int(el.get("width", 1)),
            )

        elif el_type == "rect":
            fill = el.get("color") if el.get("fill", False) else None
            outline = el.get("color") if not el.get("fill", False) else None
            draw.rectangle(
                [el["x"], el["y"], el["x"] + el["width"], el["y"] + el["height"]],
                fill=fill,
                outline=outline,
                width=int(el.get("width_border", 1)),
            )

        elif el_type in ("text", "sensor_text", "time_text"):
            text = ""
            if el_type == "text":
                text = str(el.get("text", ""))
            elif el_type == "sensor_text":
                val = MOCK_DATA.get(el.get("sensor"), 0.0)
                fmt = el.get("format", "{}")
                try:
                    text = fmt.format(val)
                except Exception:
                    text = f"{val}"
            elif el_type == "time_text":
                text = "14:32"

            font = load_font(el.get("font", ""), int(el.get("size", 10)))
            align = el.get("align", "left")
            x, y = el.get("x", 0), el.get("y", 0)

            anchor = "la"
            if align == "center":
                anchor = "ma"
            elif align == "right":
                anchor = "ra"

            draw.text((x, y), text, fill=el.get("color", "#FFFFFF"), font=font, anchor=anchor)

        elif el_type == "sensor_bar":
            bx, by = el.get("x", 0), el.get("y", 0)
            bw, bh = el.get("width", 60), el.get("height", 4)
            min_v, max_v = el.get("min", 0), el.get("max", 100)
            cur_v = MOCK_DATA.get(el.get("sensor"), 0)

            pct = max(0.0, min(1.0, (cur_v - min_v) / (max_v - min_v)))
            fill_w = int(bw * pct)

            draw.rectangle([bx, by, bx + bw, by + bh], fill=el.get("background_color", "#222222"))
            if fill_w > 0:
                draw.rectangle([bx, by, bx + fill_w, by + bh], fill=el.get("fill_color", "#FFFFFF"))

    scaled = canvas.resize((w * SCALE_FACTOR, h * SCALE_FACTOR), Image.Resampling.NEAREST)
    out_file = "preview.png"
    scaled.save(out_file)
    print(f"Rendered successfully to {out_file} ({w * SCALE_FACTOR}x{h * SCALE_FACTOR}px). Opening...")
    os.startfile(out_file)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "theme.yaml"
    render_theme(target)
