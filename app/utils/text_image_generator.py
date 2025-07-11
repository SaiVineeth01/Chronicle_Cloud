from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

def justify_text(draw, text, font, max_width, start_y, line_spacing=10, margin=60, fill="white"):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        w = draw.textlength(test_line, font=font)
        if w <= max_width - margin * 2:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    y = start_y
    for i, line in enumerate(lines):
        line_words = line.split()
        if i == len(lines) - 1 or len(line_words) == 1:
            draw.text((margin, y), line, font=font, fill=fill)
        else:
            total_width = sum(draw.textlength(w, font=font) for w in line_words)
            space_width = (max_width - margin * 2 - total_width) // (len(line_words) - 1)
            x = margin
            for word in line_words:
                draw.text((x, y), word, font=font, fill=fill)
                x += draw.textlength(word, font=font) + space_width
        y += font.getbbox("A")[3] + line_spacing

def generate_blog_image_helper(title, content, width=800, height=400):
    upscale_factor = 2
    W, H = width * upscale_factor, height * upscale_factor
    output_dir = os.path.join("app", "static", "uploads", "blog_images")
    os.makedirs(output_dir, exist_ok=True)

    safe_name = "_".join(title.lower().split())[:40]
    file_path = os.path.join(output_dir, f"{safe_name}.png")

    # Gradient background
    base_color = (70, 120, 240)
    end_color = (40, 90, 200)
    image = Image.new("RGB", (W, H), base_color)
    draw = ImageDraw.Draw(image)
    for y in range(H):
        blend = y / H
        r = int(base_color[0] * (1 - blend) + end_color[0] * blend)
        g = int(base_color[1] * (1 - blend) + end_color[1] * blend)
        b = int(base_color[2] * (1 - blend) + end_color[2] * blend)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", size=64)
        font_content = ImageFont.truetype("arial.ttf", size=36)
    except:
        try:
            font_title = ImageFont.truetype("DejaVuSans.ttf", size=64)
            font_content = ImageFont.truetype("DejaVuSans.ttf", size=36)
        except:
            font_title = ImageFont.load_default()
            font_content = ImageFont.load_default()

    # Emoji logic
    lowered = title.lower()
    if "cybersecurity" in lowered:
        title = "🔒 " + title
    elif "ai" in lowered:
        title = "🤖 " + title
    elif "productivity" in lowered:
        title = "⚙️ " + title
    elif "education" in lowered:
        title = "🎓 " + title
    else:
        title = "📝 " + title

    # Draw title
    draw.text((60, 60), title[:60], fill="white", font=font_title)

    # Justify content
    justify_text(draw, content, font=font_content, max_width=W, start_y=220, margin=60)

    # Watermark
    watermark = "ChronicleCloud AI"
    wm_width = draw.textlength(watermark, font=font_content)
    draw.text((W - wm_width - 40, H - 60), watermark, font=font_content, fill=(230, 230, 255))

    # Downscale for better anti-aliased output
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image.save(file_path)
    return f"uploads/blog_images/{safe_name}.png"
