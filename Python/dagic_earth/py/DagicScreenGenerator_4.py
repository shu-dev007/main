from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime, timedelta

# 画像仕様
width = 512
height = 1024
num_images = 120
start_x = 30
end_x = 482
fixed_y = 100  # ← Y座標を100に変更
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'

# 色設定
background_color = "#171516"
dot_color = "#ffd700"
trail_color = "white"
text_color = "white"
dot_radius = 9

# フォント設定（日本語対応フォント）
try:
    font_path = "C:/Windows/Fonts/msgothic.ttc"  # MSゴシック（日本語対応）
    font = ImageFont.truetype(font_path, 20)
except:
    print("⚠ 日本語フォントが見つかりません。文字化けする可能性があります。")
    font = ImageFont.load_default()

# 出力フォルダ作成
os.makedirs(output_folder, exist_ok=True)

# X座標の移動量
dx = (end_x - start_x) / (num_images - 1)

# 軌跡保持用リスト
trajectory = []

# 日付設定（2025年9月1日～11月30日）
start_date = datetime(2025, 9, 1)
end_date = datetime(2025, 11, 30)
total_days = (end_date - start_date).days
delta_per_image = total_days / (num_images - 1)

# 各画像を生成
for i in range(num_images):
    current_x = int(start_x + dx * i)
    trajectory.append((current_x, fixed_y))

    # 日本語日付（例：2025年9月1日）
    current_date = start_date + timedelta(days=i * delta_per_image)
    date_str = f"{current_date.year}年{current_date.month}月{current_date.day}日"

    # 背景画像作成
    image = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(image)

    # 軌跡線描画
    if len(trajectory) > 1:
        draw.line(trajectory, fill=trail_color, width=2)

    # プロット描画（金色の円）
    draw.ellipse(
        (
            current_x - dot_radius,
            fixed_y - dot_radius,
            current_x + dot_radius,
            fixed_y + dot_radius
        ),
        fill=dot_color
    )

    # テキストサイズ取得
    bbox = draw.textbbox((0, 0), date_str, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # テキスト位置計算（画像内に収める）
    text_x = max(0, min(width - text_width, current_x - text_width // 2))
    text_y = max(0, fixed_y - dot_radius - text_height - 5)

    # 日付描画
    draw.text((text_x, text_y), date_str, fill=text_color, font=font)

    # 保存
    filename = f"screen{i+1}.jpg"
    image.save(os.path.join(output_folder, filename), "JPEG")

print(f"{num_images}枚の画像を '{output_folder}' に出力しました。")
