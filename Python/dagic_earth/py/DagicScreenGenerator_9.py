from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

# 画像仕様
width = 512
height = 1024
num_images = 120
start_x = 60
end_x = 200
fixed_y = 485

output_base = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/output_folder/screen'
now = datetime.now().strftime('%Y%m%d_%H%M%S')
output_folder = os.path.join(output_base, now)
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
    bold_font_path = "C:/Windows/Fonts/meiryo.ttc"  # やや太字
    font_label = ImageFont.truetype(font_path, 22)
    font_label_bold = ImageFont.truetype(bold_font_path, 20)
    font_small_1 = ImageFont.truetype(font_path, 20)
    font_small_2 = ImageFont.truetype(font_path, 27)
except:
    print("⚠ 日本語フォントが見つかりません。文字化けの可能性あり。")
    font_label = ImageFont.load_default()
    font_label_bold = font_label
    font_small_1 = font_label
    font_small_2 = font_label

# X座標の移動量
dx = (end_x - start_x) / (num_images - 1)
trajectory = []

# 日付の設定（ただし画像には使用されていない）
start_date = datetime(2025, 9, 1)
end_date = datetime(2025, 11, 30)

# ロゴの読み込み
logo_path = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/logo.gif'
logo_image = Image.open(logo_path).convert("RGBA").resize((60, 60))

for i in range(num_images):
    current_x = int(start_x + dx * i)
    trajectory.append((current_x, fixed_y))

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    if len(trajectory) > 1:
        draw.line(trajectory, fill=trail_color, width=2)

    # 三角形（風向き表示）
    triangle = [
        (current_x + dot_radius, fixed_y),
        (current_x - dot_radius, fixed_y - dot_radius),
        (current_x - dot_radius, fixed_y + dot_radius),
    ]
    draw.polygon(triangle, fill=dot_color)

    # 月と年ラベル
    draw.text((start_x - 50, 470), "9月", fill=text_color, font=font_label_bold)
    draw.text((end_x + 10, 470), "11月", fill=text_color, font=font_label_bold)

    center_x = (start_x + end_x) // 2
    bbox_year = draw.textbbox((0, 0), "2025年", font=font_label_bold)
    year_width = bbox_year[2] - bbox_year[0]
    draw.text((center_x - year_width // 2, 440), "2025年", fill=text_color, font=font_label_bold)

    # 注釈
    draw.text((7, 530), "2025年6月時点に", fill=text_color, font=font_label_bold)
    draw.text((7, 560), "スーパーコンピュータで", fill=text_color, font=font_label_bold)
    draw.text((7, 590), "予測した2025年9月から", fill=text_color, font=font_label_bold)
    draw.text((7, 620), "11月の平均した地上風の状況", fill=text_color, font=font_label_bold)
    draw.text((7, 650), "(未来予測）", fill=text_color, font=font_label_bold)
    draw.text((7, 680), "平年からの異常値（偏差）を描画", fill=text_color, font=font_label_bold)

    # ロゴと出典テキスト
    y_base = 730
    image.paste(logo_image, (7, y_base), logo_image)
    draw.text((70, y_base), "SINTEX-Fによる", fill=text_color, font=font_small_1)
    draw.text((70, y_base + 20), "地上風偏差シミュレーション", fill=text_color, font=font_small_2)

    # 保存
    filename = f"screen_{i}.jpg"
    image.save(os.path.join(output_folder, filename), "JPEG")

print(f"{num_images}枚の画像を '{output_folder}' に出力しました。")