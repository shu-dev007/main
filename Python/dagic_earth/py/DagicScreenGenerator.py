from PIL import Image, ImageDraw
import os

# 画像仕様
width = 512
height = 1024
num_images = 120
start_x = 10
end_x = 502
fixed_y = 512
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'  # 出力先フォルダ


# 出力ディレクトリ作成
os.makedirs(output_folder, exist_ok=True)

# プロットのx座標移動量
dx = (end_x - start_x) / (num_images - 1)

for i in range(num_images):
    # 画像作成（白背景）
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)

    # 現在のx座標
    current_x = int(start_x + dx * i)

    # 点を描画（赤い小さな円）
    draw.ellipse((current_x - 3, fixed_y - 3, current_x + 3, fixed_y + 3), fill="red")

    # ファイル名
    filename = f"screen{i+1}.jpg"
    filepath = os.path.join(output_folder, filename)

    # 画像保存（JPEG形式）
    image.save(filepath, "JPEG")

print(f"{num_images}枚の画像を'{output_folder}'フォルダに出力しました。")
