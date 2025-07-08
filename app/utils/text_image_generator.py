from PIL import Image, ImageDraw, ImageFont
import os

def justify_text(draw, text, font, max_width, start_y, line_spacing=6, margin=40, fill="white"):
    words = text.split()
    lines = []
    current_line = ""

    # Build lines manually
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

    # Draw lines with justification
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
        y += font.getbbox("A")[3] + line_spacing  # Approx line height

def generate_blog_image_helper(title, content, width=800, height=400):
    output_dir = os.path.join("app", "static", "uploads", "blog_images")
    os.makedirs(output_dir, exist_ok=True)

    safe_name = "_".join(title.lower().split())[:40]
    file_path = os.path.join(output_dir, f"{safe_name}.png")

    # Gradient background
    base_color = (70, 120, 240)
    end_color = (40, 90, 200)
    image = Image.new("RGB", (width, height), base_color)
    for y in range(height):
        blend = y / height
        r = int(base_color[0] * (1 - blend) + end_color[0] * blend)
        g = int(base_color[1] * (1 - blend) + end_color[1] * blend)
        b = int(base_color[2] * (1 - blend) + end_color[2] * blend)
        ImageDraw.Draw(image).line([(0, y), (width, y)], fill=(r, g, b))

    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 34)
        font_content = ImageFont.truetype("arial.ttf", 20)
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
    draw.text((40, 30), title[:60], fill="white", font=font_title)

    # Justify content
    justify_text(draw, content, font=font_content, max_width=width, start_y=120, margin=40)

    # Watermark
    watermark = "ChronicleCloud AI"
    wm_width = draw.textlength(watermark, font=font_content)
    draw.text((width - wm_width - 20, height - 30), watermark, font=font_content, fill=(220, 220, 255))

    image.save(file_path)
    return f"uploads/blog_images/{safe_name}.png"
