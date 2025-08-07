import cv2
import os
import numpy as np
# from datetime import datetime, timedelta

# プロジェクトディレクトリ：C:\Users\yohens\Documents\vscode\Python\dagic_earth
# 仮想環境をacvtivateさせてから実行すること
# vscodeターミナルにてdagic_earthプロジェクトフォルダへ移動("cd .\dagic_earth\"")
# 作成済の仮想環境(.dagic_earth_venv)を有効化(".dagic_earth_venv\Scripts\activate")
# vscode画面右下から"3.13.0(.dagic_earth_venv)"を選択(C:\Users\yohens\Documents\vscode\Python\dagic_earth\.dagic_earth_venv\Scripts\python.exe)
# 実行時には毎回、ターミナル左に(.dagic_earth_venv)となっていることと、右下"3.13.0(.dagic_earth_venv)となっていることを確認すること

# === 入出力設定 ===
video_path = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/input.mov/SINTEX-F.uv.2025SON.mov'
# output_folder = 'output_folder/map'
# output_folder = 'output_folder/screen'
output_folder = 'C:/Users/yohens/Documents/vscode/Python/dagic_earth/output_folder/map'


output_size_temp = (2056, 1024)   # 一時的な拡大サイズ
output_size_final = (2048, 1024)  # 最終トリミング後のサイズ
total_frames = 120

# 除去対象領域（凡例・メニューなど）
remove_region = {"x": 3, "y": 800, "w": 440, "h": 224}

# 親ディレクトリ(output_folder/screen)配下にスクリプト実行ごとに新しい出力フォルダを生成
# フォルダ名は"YYYYMMDD_hhmmss"(ex.20250718_133646)
# 今日の日付と時間を取得（秒まで）
datetime_dat = datetime.now()
now = datetime_dat.strftime('%Y%m%d_%H%M%S')
# 新しいディレクトリのパス
output_folder = os.path.join(output_folder, now)
# 新しいディレクトリを作成
os.makedirs(output_folder, exist_ok=True)

# === 黒い余白の補完関数 ===
def fill_black_edges(img):
    h, w = img.shape[:2]
    mask = cv2.inRange(img, (0, 0, 0), (5, 5, 5))  # 真っ黒に近い領域をマスク

    # 左側補完
    for x in range(w):
        if np.any(mask[:, x]):
            ref = img[:, x + 1] if x + 1 < w else img[:, x]
            for i in range(x, -1, -1):
                img[:, i] = ref
            break

    # 右側補完
    for x in range(w - 1, -1, -1):
        if np.any(mask[:, x]):
            ref = img[:, x - 1] if x - 1 >= 0 else img[:, x]
            for i in range(x, w):
                img[:, i] = ref
            break

    # 上側補完
    for y in range(h):
        if np.any(mask[y, :]):
            ref = img[y + 1, :] if y + 1 < h else img[y, :]
            for i in range(y, -1, -1):
                img[i, :] = ref
            break

    # 下側補完
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

    # 一時リサイズ（2056×1024）
    resized = cv2.resize(frame, output_size_temp, interpolation=cv2.INTER_LINEAR)

    # 除去領域補完処理
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

    # 黒余白補完処理
    filled = fill_black_edges(resized)

    # 左4px、右4px を除去して 2048×1024 にトリミング
    final_img = filled[:, 4:2052]

    # 保存
    filename = os.path.join(output_folder, f"map_{idx}.jpg")
    cv2.imwrite(filename, final_img)
    print(f"Saved: {filename}")

cap.release()
print("完了しました。")
