import cv2
import os

# === 入力ファイルと出力設定 ===
video_path = 'C:/Users/yohens/Documents/vscode/Python/venv_test/input.mov/SINTEX-F.uv.2025SON.mov'  # 入力動画ファイル
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'  # 出力先フォルダ
output_size = (2048, 1024)  # 幅x高さ
num_frames = 10  # 取り出すフレーム数（例：等間隔で10枚）

# === フォルダが存在しない場合は作成 ===
os.makedirs(output_folder, exist_ok=True)

# === 動画読み込み ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video file: {video_path}")

# 動画の情報取得
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
duration_sec = frame_count / fps

print(f"Duration: {duration_sec:.2f}s, FPS: {fps:.2f}, Total Frames: {frame_count}")

# 等間隔のフレームインデックスを取得
interval = frame_count // num_frames
frame_indices = [i * interval for i in range(num_frames)]

# フレームを抽出して保存
for idx, frame_no in enumerate(frame_indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if not ret:
        print(f"Warning: Could not read frame at index {frame_no}")
        continue

    # リサイズ（2048x1024）
    resized_frame = cv2.resize(frame, output_size)

    # 保存
    output_path = os.path.join(output_folder, f'map_{idx}.jpg')
    cv2.imwrite(output_path, resized_frame)
    print(f"Saved {output_path}")

cap.release()
print("完了しました。")