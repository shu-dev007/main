from PIL import Image, ImageDraw
import os

# 画像仕様
width = 512
height = 1024
num_images = 120
start_x = 30
end_x = 482
fixed_y = 600
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'  # 出力先フォルダ

# 色指定
background_color = "#171516"  # 背景：暗色
dot_color = "#ffd700"         # プロット：金色
trail_color = "white"         # 軌跡：白
dot_radius = 9                # プロット半径

# 出力ディレクトリ作成
os.makedirs(output_folder, exist_ok=True)

# x座標の移動量
dx = (end_x - start_x) / (num_images - 1)

# 軌跡のための座標リスト
trajectory = []

for i in range(num_images):
    # 現在のx座標
    current_x = int(start_x + dx * i)
    trajectory.append((current_x, fixed_y))

    # 背景画像作成
    image = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(image)

    # 軌跡（白い線）
    if len(trajectory) > 1:
        draw.line(trajectory, fill=trail_color, width=2)

    # プロット（金色の円）
    draw.ellipse(
        (
            current_x - dot_radius,
            fixed_y - dot_radius,
            current_x + dot_radius,
            fixed_y + dot_radius
        ),
        fill=dot_color
    )

    # ファイル名生成
    filename = f"screen{i+1}.jpg"
    filepath = os.path.join(output_folder, filename)

    # 保存
    image.save(filepath, "JPEG")

print(f"{num_images}枚の画像を'{output_folder}'フォルダに出力しました。")
