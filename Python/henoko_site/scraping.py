import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

BASE_URL = "http://henoko.org/"
OUTPUT_DIR = "henoko_site"

visited = set()

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def download_file(url, folder):
    local_filename = os.path.join(folder, os.path.basename(urlparse(url).path))
    try:
        with requests.get(url, stream=True, timeout=10) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✔ {url} → {local_filename}")
    except Exception as e:
        print(f"✘ {url} 失敗: {e}")

def scrape(url, folder):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # 保存先フォルダ
        os.makedirs(folder, exist_ok=True)

        # ページ本体を保存
        filename = os.path.join(folder, "index.html")
        with open(filename, "w", encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"✔ ページ保存: {filename}")

        # リンクされた画像・CSS・JSなどを保存
        for tag in soup.find_all(["a", "img", "link", "script"]):
            attr = "href" if tag.name in ["a", "link"] else "src"
            file_url = tag.get(attr)
            if not file_url:
                continue
            full_url = urljoin(url, file_url)
            if not is_valid_url(full_url):
                continue

            if any(full_url.endswith(ext) for ext in [".jpg", ".png", ".gif", ".css", ".js", ".pdf", ".html"]):
                download_file(full_url, folder)

            # ページ内リンクなら再帰
            if BASE_URL in full_url and full_url.endswith(".html"):
                subfolder = os.path.join(folder, os.path.basename(full_url).replace(".html", ""))
                scrape(full_url, subfolder)

    except Exception as e:
        print(f"✘ ページ取得失敗: {url} - {e}")

# 実行
scrape(BASE_URL, OUTPUT_DIR)