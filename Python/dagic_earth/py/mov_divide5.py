import cv2
import os
import numpy as np

# === 入出力設定 ===
video_path = 'C:/Users/yohens/Documents/vscode/Python/venv_test/input.mov/SINTEX-F.uv.2025SON.mov'  # 入力動画のパス
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'  # 出力先フォルダ
output_size = (2048, 1024)
total_frames = 120

# === 除去対象：1つに統合された領域 ===
remove_region = {"x": 3, "y": 800, "w": 440, "h": 224}

# === 格子線設定 ===
grid_color = (200, 200, 200)   # 薄いグレー
grid_thickness = 1             # 最小線幅
num_lat_lines = 3              # 緯線（横）本数
num_lon_lines = 8              # 経線（縦）本数

def draw_inner_grid_lines(img, region, img_size, color, thickness, num_lat, num_lon):
    """補完領域に、画像全体の格子線と同調するような線を描画"""
    x, y, w, h = region["x"], region["y"], region["w"], region["h"]
    img_w, img_h = img_size

    # 経線（縦線）位置を計算（全体を9等分し、8本引く）
    for i in range(num_lon_lines):
        gx = (i + 1) * img_w // (num_lon_lines + 1)
        if x <= gx <= x + w:
            cv2.line(img, (gx, y), (gx, y + h), color, thickness)

    # 緯線（横線）位置を計算（全体を4等分し、3本引く）
    for j in range(num_lat_lines):
        gy = (j + 1) * img_h // (num_lat_lines + 1)
        if y <= gy <= y + h:
            cv2.line(img, (x, gy), (x + w, gy), color, thickness)

    return img

# === 出力フォルダ作成 ===
os.makedirs(output_folder, exist_ok=True)

# === 動画読み込み ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video file: {video_path}")

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
interval = frame_count // total_frames
frame_indices = [i * interval for i in range(total_frames)]

for idx, frame_no in enumerate(frame_indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if not ret:
        print(f"Warning: frame {frame_no} could not be read.")
        continue

    # リサイズ
    resized = cv2.resize(frame, output_size)

    # 補完処理（ぼかしで埋める）
    x, y, w, h = remove_region["x"], remove_region["y"], remove_region["w"], remove_region["h"]
    ref_x_start = min(x + w, output_size[0] - 1)
    ref_x_end = min(ref_x_start + 30, output_size[0])
    ref_area = resized[y:y+h, ref_x_start:ref_x_end]
    fill = cv2.blur(ref_area, (9, 9))
    fill_resized = cv2.resize(fill, (w, h))
    resized[y:y+h, x:x+w] = fill_resized

    # 補完領域に格子線（画像全体の延長線）を描画
    resized = draw_inner_grid_lines(
        resized,
        remove_region,
        img_size=output_size,
        color=grid_color,
        thickness=grid_thickness,
        num_lat=num_lat_lines,
        num_lon=num_lon_lines
    )

    # 保存
    filename = os.path.join(output_folder, f"map_{idx}.jpg")
    cv2.imwrite(filename, resized)
    print(f"Saved: {filename}")

cap.release()
print("完了しました。")