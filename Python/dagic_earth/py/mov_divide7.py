import cv2
import os
import numpy as np

# === 入出力設定 ===
video_path = 'C:/Users/yohens/Documents/vscode/Python/venv_test/input.mov/SINTEX-F.uv.2025SON.mov'
output_folder = 'C:/Users/yohens/Documents/vscode/Python/venv_test/output_folder'
output_size_temp = (2055, 1024)  # 一旦広くリサイズ
output_size_final = (2048, 1024)
total_frames = 120

# 除去対象領域（凡例や文字）
remove_region = {"x": 3, "y": 800, "w": 440, "h": 224}

# 出力先フォルダ作成
os.makedirs(output_folder, exist_ok=True)

# === 黒余白補完関数 ===
def fill_black_edges(img):
    h, w = img.shape[:2]
    mask = cv2.inRange(img, (0, 0, 0), (5, 5, 5))  # 非常に暗い領域を検出

    # 左端補完
    for x in range(w):
        if np.any(mask[:, x]):
            ref = img[:, x + 1] if x + 1 < w else img[:, x]
            for i in range(x, -1, -1):
                img[:, i] = ref
            break

    # 右端補完
    for x in range(w - 1, -1, -1):
        if np.any(mask[:, x]):
            ref = img[:, x - 1] if x - 1 >= 0 else img[:, x]
            for i in range(x, w):
                img[:, i] = ref
            break

    # 上端補完
    for y in range(h):
        if np.any(mask[y, :]):
            ref = img[y + 1, :] if y + 1 < h else img[y, :]
            for i in range(y, -1, -1):
                img[i, :] = ref
            break

    # 下端補完
    for y in range(h - 1, -1, -1):
        if np.any(mask[y, :]):
            ref = img[y - 1, :] if y - 1 >= 0 else img[y, :]
            for i in range(y, h):
                img[i, :] = ref
            break

    return img

# === 動画読み込み ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video file: {video_path}")

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
interval = max(frame_count // total_frames, 1)
frame_indices = [i * interval for i in range(total_frames)]

for idx, frame_no in enumerate(frame_indices):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if not ret or frame is None:
        print(f"Warning: frame {frame_no} could not be read.")
        continue

    # 一旦2055×1024にリサイズ
    resized = cv2.resize(frame, output_size_temp, interpolation=cv2.INTER_LINEAR)

    # 除去領域補完
    x, y, w, h = remove_region["x"], remove_region["y"], remove_region["w"], remove_region["h"]
    margin = 30
    if x + w + margin < output_size_temp[0]:
        ref_area = resized[y:y + h, x + w:x + w + margin]
    else:
        ref_area = resized[y:y + h, x - margin:x]

    if ref_area is not None and ref_area.size > 0:
        blurred = cv2.blur(ref_area, (11, 11))
        fill_patch = cv2.resize(blurred, (w, h), interpolation=cv2.INTER_LINEAR)
        resized[y:y + h, x:x + w] = fill_patch

    # 黒余白補完
    filled = fill_black_edges(resized)

    # 左3px, 右4px を除去 → 最終出力サイズは 2048x1024
    final_img = filled[:, 3:2051]

    # 保存
    filename = os.path.join(output_folder, f"map_{idx}.jpg")
    cv2.imwrite(filename, final_img)
    print(f"Saved: {filename}")

cap.release()
print("完了しました。")
