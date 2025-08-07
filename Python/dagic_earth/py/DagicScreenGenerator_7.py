from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime, timedelta

# プロジェクトディレクトリ：C:\Users\yohens\Documents\vscode\Python\dagic_earth
# 仮想環境をacvtivateさせてから実行すること
# vscodeターミナルにてdagic_earthプロジェクトフォルダへ移動("cd .\dagic_earth\"")
# 作成済の仮想環境(.dagic_earth_venv)を有効化(".dagic_earth_venv\Scripts\activate")
# vscode画面右下から"3.13.0(.dagic_earth_venv)"を選択
# 実行時には毎回、ターミナル左に(.dagic_earth_venv)となっていることと、右下"3.13.0(.dagic_earth_venv)となっていることを確認すること


# 画像仕様
width = 512
height = 1024
num_images = 120  # 出力ファイル数
start_x = 60  # プロット開始点
end_x = 200   # プロット終了点
# fixed_y = 512  # プロットY位置
fixed_y = 485  # プロットY位置

# output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'
# output_folder = 'output_folder/screen'
output_folder = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/output_folder/screen'


# 親ディレクトリ(output_folder/screen)配下にスクリプト実行ごとに新しい出力フォルダを生成
# フォルダ名は"YYYYMMDD_hhmmss"(ex.20250718_133646)
# 今日の日付と時間を取得（秒まで）
datetime_dat = datetime.now()
now = datetime_dat.strftime('%Y%m%d_%H%M%S')
# 新しいディレクトリのパス
output_folder = os.path.join(output_folder, now)
# 新しいディレクトリを作成
os.makedirs(output_folder, exist_ok=True)


# 色設定
background_color = "#000000"
dot_color = "#ffd700"
trail_color = "white"
text_color = "white"
dot_radius = 9  # 三角形のサイズ

# フォント設定
try:
    font_path = "C:/Windows/Fonts/msgothic.ttc"
    # font_path = "C:/Windows/Fonts/NotoSans-Regular.ttf"
    bold_font_path = "NotoSans-Bold.ttf"
    font_main = ImageFont.truetype(font_path, 25)
    # font_label = ImageFont.truetype(font_path, 25)
    font_label = ImageFont.truetype(font_path, 22)
    # font_label = ImageFont.truetype(bold_font_path, 23)
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

# ロゴ読み込み
# logo_path = 'C:/Users/yohens/Documents/vscode/Python/venv_test/logo.gif'  # 実行ファイルと同じディレクトリにあると仮定
logo_path = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/logo.gif'  # 実行ファイルと同じディレクトリにあると仮定
logo_image = Image.open(logo_path).convert("RGBA")
logo_image = logo_image.resize((60, 60))  # 必要に応じてサイズ調整

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
        (current_x + dot_radius, fixed_y),
        (current_x - dot_radius, fixed_y - dot_radius),
        (current_x - dot_radius, fixed_y + dot_radius),
    ]
    draw.polygon(triangle, fill=dot_color)

    # 「9月」表示
    bbox_9 = draw.textbbox((0, 0), "9月", font=font_label)
    # draw.text((start_x - bbox_9[2] - 15, fixed_y - bbox_9[3] // 2),
    draw.text((start_x - bbox_9[2] - 15, 470),
              "9月", fill=text_color, font=font_label)

    # 「11月」表示
    bbox_11 = draw.textbbox((0, 0), "11月", font=font_label)
    # draw.text((end_x + 10, fixed_y - bbox_11[3] // 2),
    draw.text((end_x + 10, 470),
              "11月", fill=text_color, font=font_label)

    # 「2025年」中央上部に表示
    center_x = (start_x + end_x) // 2
    bbox_year = draw.textbbox((0, 0), "2025年", font=font_label)
    text_2025_width = bbox_year[2] - bbox_year[0]
    # draw.text((center_x - text_2025_width // 2, 450),
    draw.text((center_x - text_2025_width // 2, 440),
              "2025年", fill=text_color, font=font_label)

    # 注釈テキスト（固定位置）
    # draw.text((7, 620), "SINTEX(平均)", fill=text_color, font=font_label)
    # draw.text((7, 650), "2025年9月–11月平均", fill=text_color, font=font_label)
    # draw.text((7, 680), "地上風偏差×地上風偏差", fill=text_color, font=font_label)

    draw.text((7, 530), "2025年6月時点に", fill=text_color, font=font_label)
    draw.text((7, 560), "スーパーコンピュータで", fill=text_color, font=font_label)
    draw.text((7, 590), "予測した2025年9月から", fill=text_color, font=font_label)
    draw.text((7, 620), "11月の平均した地上風の状況", fill=text_color, font=font_label)
    draw.text((7, 650), "(未来予測）", fill=text_color, font=font_label)
    draw.text((7, 680), "平年からの異常値（偏差）を描画", fill=text_color, font=font_label)

    # サブ注釈フォント
    font_small_1 = ImageFont.truetype(font_path, 20)
    font_small_2 = ImageFont.truetype(font_path, 27)

    # 追加テキスト
    # extra_line1 = "地球シミュレータによる"
    extra_line1 = "SINTEX-Fによる"
    # extra_line2 = "地上風偏差予測モデル"
    extra_line2 = "地上風偏差シミュレーション"
    y_base = 710 + 20  # 表示Y位置

    # JAMSTECロゴ貼り付け
    image.paste(logo_image, (7, y_base), logo_image)

    # テキスト描画（ロゴの右に）
    text_x = 70  # ロゴの右側に配置
    for dx_offset, dy_offset in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        draw.text((text_x + dx_offset, y_base + dy_offset), extra_line1, fill=text_color, font=font_small_1)

    draw.text((text_x, y_base + 20), extra_line2, fill=text_color, font=font_small_2)

    # ファイル保存
    filename = f"screen_{i}.jpg"
    image.save(os.path.join(output_folder, filename), "JPEG")

print(f"{num_images}枚の画像を '{output_folder}' に出力しました。")