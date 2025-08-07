from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime, timedelta

# 画像仕様
width = 512
height = 1024
num_images = 120
start_x = 60  # プロット開始点
end_x = 200    # プロット終了点
fixed_y = 512   # プロットY位置

output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'

# 色設定
background_color = "#000000"
dot_color = "#ffd700"
trail_color = "white"
text_color = "white"
dot_radius = 9  # 三角形のサイズ

# フォント設定
try:
    font_path = "C:/Windows/Fonts/msgothic.ttc"
    font_main = ImageFont.truetype(font_path, 25)
    font_label = ImageFont.truetype(font_path, 25)# 文字の大きさ指定
except:
    print("⚠ 日本語フォントが見つかりません。文字化けの可能性あり。")
    font_main = ImageFont.load_default()
    font_label = font_main

# 出力フォルダ作成
os.makedirs(output_folder, exist_ok=True)

# X座標の移動量
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

    # 画像生成
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 軌跡線描画
    if len(trajectory) > 1:
        draw.line(trajectory, fill=trail_color, width=2)

    # プロット（三角形）
    triangle = [
        (current_x + dot_radius, fixed_y),                 # 右
        (current_x - dot_radius, fixed_y - dot_radius),    # 左上
        (current_x - dot_radius, fixed_y + dot_radius),    # 左下
    ]
    draw.polygon(triangle, fill=dot_color)

    # 「9月」表示（左隣に縦中央揃え）
    bbox_9 = draw.textbbox((0, 0), "9月", font=font_label)
    draw.text(
        (start_x - bbox_9[2] - 15, fixed_y - bbox_9[3] // 2),#文字列"9月"の横位置指定
        "9月", fill=text_color, font=font_label
    )

    # 「11月」表示（右隣に縦中央揃え）
    bbox_11 = draw.textbbox((0, 0), "11月", font=font_label)
    draw.text(
        (end_x + 10, fixed_y - bbox_11[3] // 2),
        "11月", fill=text_color, font=font_label
    )

    # 「2025年」中央上部に表示（重ならないY位置に）
    center_x = (start_x + end_x) // 2
    bbox_year = draw.textbbox((0, 0), "2025年", font=font_label)
    text_2025_width = bbox_year[2] - bbox_year[0]
    draw.text(
        (center_x - text_2025_width // 2, 450),# ← ここの Y 座標が縦位置（文字列"2025年"）
        "2025年", fill=text_color, font=font_label
    )

    # 注釈テキスト（固定位置）
    draw.text((7, 620), "SINTEX(平均)", fill=text_color, font=font_label)
    draw.text((7, 650), "2025年9月–11月平均", fill=text_color, font=font_label)
    draw.text((7, 680), "地上風偏差×地上風偏差", fill=text_color, font=font_label)

    # ファイル名
    filename = f"screen_{i}.jpg"
    image.save(os.path.join(output_folder, filename), "JPEG")

print(f"{num_images}枚の画像を '{output_folder}' に出力しました。")
