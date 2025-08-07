import cv2
import os
import numpy as np

# === 入出力設定 ===
video_path = 'C:/Users/yohens/Documents/vscode/Python/venv_test/input.mov/SINTEX-F.uv.2025SON.mov'  # 入力動画のパス
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'  # 出力先フォルダ
output_size = (2048, 1024)  # 幅 x 高さ
total_frames = 120  # 出力する画像枚数

# === 除去対象の左下3領域（修正版） ===
remove_regions = [
    {"x": 0, "y": 800, "w": 440, "h": 70},   # SINTEX（平均）領域（上方向に拡張）
    {"x": 0, "y": 870, "w": 420, "h": 90},   # 凡例情報（やや小さく）
    {"x": 0, "y": 960, "w": 300, "h": 64},   # Menuボタン
]

# === 出力先フォルダの作成 ===
os.makedirs(output_folder, exist_ok=True)

# === 動画読み込み ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video file: {video_path}")

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

# === 等間隔にフレーム番号を抽出 ===
interval = frame_count // total_frames
frame_indices = [i * interval for i in range(total_frames)]

for idx, frame_no in enumerate(frame_indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if not ret:
        print(f"Warning: frame {frame_no} could not be read.")
        continue

    # リサイズ（2048×1024）
    resized = cv2.resize(frame, output_size)

    # === 各不要領域を右隣で補完 ===
    for region in remove_regions:
        x, y, w, h = region["x"], region["y"], region["w"], region["h"]

        # 補完参照エリア（右隣領域）取得
        ref_x_start = min(x + w, output_size[0] - 1)
        ref_x_end = min(ref_x_start + 30, output_size[0])  # 少し広めに取得
        ref_area = resized[y:y+h, ref_x_start:ref_x_end]

        # ブラーで補完生成
        fill = cv2.blur(ref_area, (9, 9))
        fill_resized = cv2.resize(fill, (w, h))
        resized[y:y+h, x:x+w] = fill_resized

    # === 保存 ===
    filename = os.path.join(output_folder, f"map_{idx}.jpg")
    cv2.imwrite(filename, resized)
    print(f"Saved: {filename}")

cap.release()
print("完了しました。")