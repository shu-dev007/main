from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
# import sys
# sys.stdout.reconfigure(encoding='utf-8')

# === 設定 ===

# 画像サイズ・プロット数
width = 512
height = 1024
num_images = 120
start_x = 60
end_x = 200
fixed_y = 485

# 色設定
background_color = "#000000"
dot_color = "#ffd700"
trail_color = "white"
text_color = "white"
dot_radius = 9

# 出力フォルダ
output_base = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/output_folder/screen'
now = datetime.now().strftime('%Y%m%d_%H%M%S')
output_folder = os.path.join(output_base, now)
os.makedirs(output_folder, exist_ok=True)

# フォント設定
try:
    font_path = "C:/Windows/Fonts/msgothic.ttc"
    bold_font_path = "C:/Windows/Fonts/meiryo.ttc"
    font_label = ImageFont.truetype(font_path, 22)
    font_label_bold = ImageFont.truetype(bold_font_path, 20)
    font_small_1 = ImageFont.truetype(font_path, 20)
    font_small_2 = ImageFont.truetype(font_path, 27)
except:
    print("⚠ 日本語フォントが見つかりません。文字化けの可能性あり。")
    font_label = font_label_bold = font_small_1 = font_small_2 = ImageFont.load_default()

# ロゴ画像の読み込みとリサイズ
logo_path = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/logo.gif'
logo_image = Image.open(logo_path).convert("RGBA").resize((60, 60))

# 擬似太字描画関数
# def draw_bold_text(draw, position, text, font, fill):
#     for dx_offset, dy_offset in [(0, 0), (1, 0), (0, 1), (1, 1)]:
#         draw.text((position[0] + dx_offset, position[1] + dy_offset), text, font=font, fill=fill)

# def draw_bold_text(draw, position, text, font, fill):
#     for dx_offset in [-1, 0, 1]:
#         for dy_offset in [-1, 0, 1]:
#             draw.text((position[0] + dx_offset, position[1] + dy_offset), text, font=font, fill=fill)

# def draw_bold_text(draw, position, text, font, fill):
#     # 中心＋上下左右の5方向
#     for dx_offset, dy_offset in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
#         draw.text((position[0] + dx_offset, position[1] + dy_offset), text, font=font, fill=fill)

def draw_bold_text(draw, position, text, font, fill):
    # 中央と右隣の2回だけ描画 → ほんのり太く
    for dx_offset, dy_offset in [(0, 0), (1, 0)]:
        draw.text((position[0] + dx_offset, position[1] + dy_offset), text, font=font, fill=fill)

# 軌跡生成
dx = (end_x - start_x) / (num_images - 1)
trajectory = []

# === メインループ ===
for i in range(num_images):
    current_x = int(start_x + dx * i)
    trajectory.append((current_x, fixed_y))

    # 背景画像
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 軌跡の線
    if len(trajectory) > 1:
        draw.line(trajectory, fill=trail_color, width=2)

    # 現在位置を三角形で表示
    triangle = [
        (current_x + dot_radius, fixed_y),
        (current_x - dot_radius, fixed_y - dot_radius),
        (current_x - dot_radius, fixed_y + dot_radius),
    ]
    draw.polygon(triangle, fill=dot_color)

    # 年と月ラベル
    center_x = (start_x + end_x) // 2
    bbox_year = draw.textbbox((0, 0), "2025年", font=font_label_bold)
    year_width = bbox_year[2] - bbox_year[0]
    draw_bold_text(draw, (center_x - year_width // 2, 440), "2025年", font_label_bold, text_color)

    draw_bold_text(draw, (start_x - 50, 470), "9月", font_label_bold, text_color)
    draw_bold_text(draw, (end_x + 10, 470), "11月", font_label_bold, text_color)

    # 注釈テキスト（6行）
    draw_bold_text(draw, (7, 530), "2025年6月時点に", font_label_bold, text_color)
    draw_bold_text(draw, (7, 560), "スーパーコンピュータで", font_label_bold, text_color)
    draw_bold_text(draw, (7, 590), "予測した2025年9月から", font_label_bold, text_color)
    draw_bold_text(draw, (7, 620), "11月の平均した地上風の状況", font_label_bold, text_color)
    draw_bold_text(draw, (7, 650), "(未来予測）", font_label_bold, text_color)
    draw_bold_text(draw, (7, 680), "平年からの異常値（偏差）を描画", font_label_bold, text_color)

    # ロゴと出典テキスト
    y_base = 730
    image.paste(logo_image, (7, y_base), logo_image)
    draw_bold_text(draw, (70, y_base), "SINTEX-Fによる", font_small_1, text_color)
    draw.text((70, y_base + 20), "地上風偏差シミュレーション", fill=text_color, font=font_small_2)

    # ファイル保存
    filename = f"screen_{i}.jpg"
    image.save(os.path.join(output_folder, filename), "JPEG")

# 完了メッセージ
print(f"{num_images}枚の画像を '{output_folder}' に出力しました。")