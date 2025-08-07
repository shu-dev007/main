import cv2
import os
import numpy as np

# === 入出力設定 ===
video_path = 'C:/Users/yohens/Documents/vscode/Python/venv_test/input.mov/SINTEX-F.uv.2025SON.mov'  # 入力動画のパス
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'  # 出力先フォルダ
output_size = (2048, 1024)
total_frames = 120

# === 除去対象領域 ===
remove_region = {"x": 3, "y": 800, "w": 440, "h": 224}

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

    # 除去領域情報
    x, y, w, h = remove_region["x"], remove_region["y"], remove_region["w"], remove_region["h"]

    # === 補完用の参照領域を選択 ===
    margin = 30  # 参照幅（ぼかし用）
    if x + w + margin < output_size[0]:
        # 右隣を使う
        ref_area = resized[y:y+h, x+w:x+w+margin]
    elif x - margin >= 0:
        # 左隣を使う
        ref_area = resized[y:y+h, x-margin:x]
    elif y - margin >= 0:
        # 上を使う
        ref_area = resized[y-margin:y, x:x+w]
    else:
        # 取得不可→そのままスキップ
        ref_area = None

    # 補完処理
    if ref_area is not None and ref_area.size > 0:
        # ぼかして拡大して連続的に見せる
        blurred = cv2.blur(ref_area, (11, 11))
        fill_resized = cv2.resize(blurred, (w, h), interpolation=cv2.INTER_LINEAR)
        resized[y:y+h, x:x+w] = fill_resized

    # JPGとして保存
    filename = os.path.join(output_folder, f"map_{idx}.jpg")
    cv2.imwrite(filename, resized)
    print(f"Saved: {filename}")

cap.release()
print("完了しました。")