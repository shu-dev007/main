import cv2
import os
import numpy as np

# === 入出力設定 ===
video_path = 'C:/Users/yohens/Documents/vscode/Python/venv_test/input.mov/SINTEX-F.uv.2025SON.mov'  # 入力動画のパス
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'  # 出力先フォルダ
output_size = (2048, 1024)  # 幅 x 高さ
total_frames = 120  # 出力する画像枚数

# === 除去対象の左下2領域 ===
remove_regions = [
    {"x": 0, "y": 850, "w": 420, "h": 110},  # 凡例テキスト領域
    {"x": 0, "y": 960, "w": 300, "h": 64},   # Menu 領域
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

        # 右隣から参考領域を取得
        ref = resized[y:y+h, x+w:x+w+20]  # 少し右を参照
        fill = cv2.blur(ref, (5, 5))      # ブラーでなじませる
        fill_resized = cv2.resize(fill, (w, h))
        resized[y:y+h, x:x+w] = fill_resized

    # === 保存 ===
    filename = os.path.join(output_folder, f"map_{idx}.jpg")
    cv2.imwrite(filename, resized)
    print(f"Saved: {filename}")

cap.release()
print("完了しました。")