from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime, timedelta

# 画像仕様
width = 512
height = 1024
num_images = 120
start_x = 30
end_x = 482
fixed_y = 80  # 100から20px上にスライド
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'

# 色設定
# background_color = "#171516"
background_color = "#000000"
dot_color = "#ffd700"
trail_color = "white"
text_color = "white"
dot_radius = 9

# フォント設定
try:
    font_path = "C:/Windows/Fonts/msgothic.ttc"
    font_main = ImageFont.truetype(font_path, 25)  # 日付用フォント
    font_label = ImageFont.truetype(font_path, 35)  # 注釈用フォント（25px、太字なし）
except:
    print("⚠ 日本語フォントが見つかりません。文字化けの可能性あり。")
    font_main = ImageFont.load_default()
    font_label = font_main

# 出力フォルダ作成
os.makedirs(output_folder, exist_ok=True)

# X座標移動量
dx = (end_x - start_x) / (num_images - 1)

# 軌跡保持リスト
trajectory = []

# 日付範囲設定（2025年9月1日～11月30日）
start_date = datetime(2025, 9, 1)
end_date = datetime(2025, 11, 30)
total_days = (end_date - start_date).days
delta_per_image = total_days / (num_images - 1)

# 画像生成ループ
for i in range(num_images):
    current_x = int(start_x + dx * i)
    trajectory.append((current_x, fixed_y))

    current_date = start_date + timedelta(days=i * delta_per_image)
    date_str = f"{current_date.year}年{current_date.month}月{current_date.day}日"

    # 画像生成
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 軌跡線描画
    if len(trajectory) > 1:
        draw.line(trajectory, fill=trail_color, width=2)

    # プロット描画
    draw.ellipse(
        (
            current_x - dot_radius,
            fixed_y - dot_radius,
            current_x + dot_radius,
            fixed_y + dot_radius,
        ),
        fill=dot_color,
    )

    # 日付テキスト描画（プロットの上）
    bbox = draw.textbbox((0, 0), date_str, font=font_main)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = max(0, min(width - text_width, current_x - text_width // 2))
    text_y = max(0, fixed_y - dot_radius - text_height - 5)
    draw.text((text_x, text_y), date_str, fill=text_color, font=font_main)

    # 注釈テキスト（位置固定）
    draw.text((30, 650), "SINTEX(平均)", fill=text_color, font=font_label)
    draw.text((30, 700), "2025年9月–11月平均", fill=text_color, font=font_label)
    draw.text((30, 750), "地上風偏差×地上風偏差", fill=text_color, font=font_label)

    # ファイル名（screen_0.jpg～screen_119.jpg）
    filename = f"screen_{i}.jpg"
    image.save(os.path.join(output_folder, filename), "JPEG")

print(f"{num_images}枚の画像を '{output_folder}' に出力しました。")
