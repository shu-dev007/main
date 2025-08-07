from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime, timedelta

# 画像仕様
width = 512
height = 1024
num_images = 120
start_x = 60
end_x = 200
fixed_y = 485

output_folder = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/output_folder/screen'

datetime_dat = datetime.now()
now = datetime_dat.strftime('%Y%m%d_%H%M%S')
output_folder = os.path.join(output_folder, now)
os.makedirs(output_folder, exist_ok=True)

# 色設定
background_color = "#000000"
dot_color = "#ffd700"
trail_color = "white"
text_color = "white"
dot_radius = 9

# フォント設定
try:
    font_path = "C:/Windows/Fonts/msgothic.ttc"
    bold_font_path = "C:/Windows/Fonts/meiryo.ttc"  # やや太字に見える日本語対応フォント
    font_main = ImageFont.truetype(font_path, 25)
    font_label = ImageFont.truetype(font_path, 22)
    font_label_bold = ImageFont.truetype(bold_font_path, 20)
except:
    print("⚠ 日本語フォントが見つかりません。文字化けの可能性あり。")
    font_main = ImageFont.load_default()
    font_label = font_main
    font_label_bold = font_main

# X座標の移動量
dx = (end_x - start_x) / (num_images - 1)

trajectory = []

start_date = datetime(2025, 9, 1)
end_date = datetime(2025, 11, 30)
total_days = (end_date - start_date).days
delta_per_image = total_days / (num_images - 1)

logo_path = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/logo.gif'
logo_image = Image.open(logo_path).convert("RGBA")
logo_image = logo_image.resize((60, 60))

for i in range(num_images):
    current_x = int(start_x + dx * i)
    trajectory.append((current_x, fixed_y))

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    if len(trajectory) > 1:
        draw.line(trajectory, fill=trail_color, width=2)

    triangle = [
        (current_x + dot_radius, fixed_y),
        (current_x - dot_radius, fixed_y - dot_radius),
        (current_x - dot_radius, fixed_y + dot_radius),
    ]
    draw.polygon(triangle, fill=dot_color)

    bbox_9 = draw.textbbox((0, 0), "9月", font=font_label_bold)
    draw.text((start_x - bbox_9[2] - 15, 470), "9月", fill=text_color, font=font_label)

    bbox_11 = draw.textbbox((0, 0), "11月", font=font_label_bold)
    draw.text((end_x + 10, 470), "11月", fill=text_color, font=font_label)
    # draw.text((end_x + 10, 470), "11月", fill=text_color, font=font_label_bold)

    center_x = (start_x + end_x) // 2
    bbox_year = draw.textbbox((0, 0), "2025年", font=font_label)
    text_2025_width = bbox_year[2] - bbox_year[0]
    # draw.text((center_x - text_2025_width // 2, 440), "2025年", fill=text_color, font=font_label)
    draw.text((center_x - text_2025_width // 2, 440), "2025年", fill=text_color, font=font_label_bold)


    # ⬇ 太字で注釈テキスト（擬似的に太字描画）
    for dx_offset, dy_offset in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        draw.text((7 + dx_offset, 530 + dy_offset), "2025年6月時点に", fill=text_color, font=font_label_bold)
        draw.text((7 + dx_offset, 560 + dy_offset), "スーパーコンピュータで", fill=text_color, font=font_label_bold)
        draw.text((7 + dx_offset, 590 + dy_offset), "予測した2025年9月から", fill=text_color, font=font_label_bold)
        draw.text((7 + dx_offset, 620 + dy_offset), "11月の平均した地上風の状況", fill=text_color, font=font_label_bold)
        draw.text((7 + dx_offset, 650 + dy_offset), "(未来予測）", fill=text_color, font=font_label_bold)
        draw.text((7 + dx_offset, 680 + dy_offset), "平年からの異常値（偏差）を描画", fill=text_color, font=font_label_bold)

    font_small_1 = ImageFont.truetype(font_path, 20)
    font_small_2 = ImageFont.truetype(font_path, 27)

    extra_line1 = "SINTEX-Fによる"
    extra_line2 = "地上風偏差シミュレーション"
    y_base = 730

    image.paste(logo_image, (7, y_base), logo_image)
    text_x = 70
    for dx_offset, dy_offset in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        draw.text((text_x + dx_offset, y_base + dy_offset), extra_line1, fill=text_color, font=font_small_1)

    draw.text((text_x, y_base + 20), extra_line2, fill=text_color, font=font_small_2)

    filename = f"screen_{i}.jpg"
    image.save(os.path.join(output_folder, filename), "JPEG")

print(f"{num_images}枚の画像を '{output_folder}' に出力しました。")