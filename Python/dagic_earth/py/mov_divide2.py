import cv2
import os
import numpy as np

# === 入力と出力設定 ===
video_path = 'C:/Users/yohens/Documents/vscode/Python/venv_test/input.mov/SINTEX-F.uv.2025SON.mov'  # 入力動画のパス
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'  # 出力先フォルダ
output_size = (2048, 1024)  # (幅, 高さ)
total_frames = 120  # 抽出するフレーム数

# === 不要領域（左下）のマスク設定 ===
crop_x, crop_y, crop_w, crop_h = 0, 960, 300, 64  # 左下 corner (x,y,w,h)

# === 出力フォルダ作成 ===
os.makedirs(output_folder, exist_ok=True)

# === 動画読み込み ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video file: {video_path}")

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

interval = frame_count // total_frames
frame_indices = [i * interval for i in range(total_frames)]

for idx, frame_no in enumerate(frame_indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if not ret:
        print(f"Warning: frame {frame_no} could not be read.")
        continue

    # 2048×1024にリサイズ
    resized = cv2.resize(frame, output_size)

    # 不要部分のマスクと補完（周囲のピクセル平均で塗りつぶし）
    roi = resized[crop_y:crop_y+crop_h, crop_x+crop_w:crop_x+crop_w+10]  # 右隣部分を参考に
    mean_color = cv2.blur(roi, (5, 5))
    fill_block = cv2.resize(mean_color, (crop_w, crop_h))
    resized[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w] = fill_block

    # 出力ファイル名
    output_path = os.path.join(output_folder, f"map_{idx}.jpg")
    cv2.imwrite(output_path, resized)
    print(f"Saved: {output_path}")

cap.release()
print("完了しました。")