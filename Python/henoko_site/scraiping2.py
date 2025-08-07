# import datetime
from datetime import datetime
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote, urldefrag
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# プロジェクトディレクトリ：C:\Users\yohens\Documents\vscode\Python\henoko_site
# 仮想環境をacvtivateさせてから実行すること
# vscodeターミナルにてhenoko_siteプロジェクトフォルダへ移動("cd .\henoko_site\"")
# 作成済の仮想環境(.henoko_site_venv)を有効化(".henoko_site_venv\Scripts\activate")
# vscode画面右下から"3.13.0(.henoko_site_venv)"を選択(C:\Users\yohens\Documents\vscode\Python\henoko_site\.henoko_site_venv\Scripts\python.exe)
# 実行時には毎回、ターミナル左に(.henoko_site_venv)となっていることと、右下"3.13.0(.henoko_site_venv)となっていることを確認すること

BASE_URL = "http://henoko.org/"
OUTPUT_DIR = 'henoko_site_output'

# 親ディレクトリ(henoko_site_output)配下にスクリプト実行ごとに新しい出力フォルダを生成
# フォルダ名は"YYYYMMDD_hhmmss"(ex.20250718_133646)
# 今日の日付と時間を取得（秒まで）
datetime_dat = datetime.now()
now = datetime_dat.strftime('%Y%m%d_%H%M%S')
# 新しいディレクトリのパス
OUTPUT_DIR = os.path.join(OUTPUT_DIR, now)
# 新しいディレクトリを作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

visited_pages = set()

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_extension(url):
    return Path(urlparse(url).path).suffix.lower()

def sanitize_path(url):
    parsed = urlparse(url)
    path = parsed.path
    if path.endswith("/"):
        path += "index.html"
    return unquote(path.lstrip("/"))

def download_resource(url, folder):
    try:
        save_path = os.path.join(folder, sanitize_path(url))
        if os.path.exists(save_path):
            return save_path

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"✔ リソース: {url} → {save_path}")
        return save_path
    except Exception as e:
        print(f"✘ リソース失敗: {url} - {e}")
        return None

def rewrite_links(soup, base_url, folder):
    tag_attr = {
        "a": "href",
        "img": "src",
        "script": "src",
        "link": "href"
    }

    for tag, attr in tag_attr.items():
        for el in soup.find_all(tag):
            val = el.get(attr)
            if not val:
                continue

            full_url = urljoin(base_url, val)
            main_url, anchor = urldefrag(full_url)
            ext = get_extension(main_url)

            parsed = urlparse(main_url)
            if parsed.netloc and parsed.netloc != urlparse(BASE_URL).netloc:
                continue

            # HTMLページ
            if ext == ".html":
                scrape(main_url, OUTPUT_DIR)
                rel_path = os.path.relpath(os.path.join(OUTPUT_DIR, sanitize_path(main_url)), folder).replace("\\", "/")
                el[attr] = rel_path + (f"#{anchor}" if anchor else "")
            # その他リソース
            elif ext in [".css", ".js", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".ico", ".woff", ".woff2", ".ttf", ".pdf"]:
                local_path = download_resource(main_url, folder)
                if local_path:
                    rel_path = os.path.relpath(local_path, folder).replace("\\", "/")
                    el[attr] = rel_path

    return soup.prettify()

def scrape(url, folder):
    if url in visited_pages:
        return
    visited_pages.add(url)

    try:
        driver.get(url)
        time.sleep(2)  # JavaScriptのレンダリング待ち
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        processed_html = rewrite_links(soup, url, folder)

        save_path = os.path.join(folder, sanitize_path(url))
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(processed_html)
        print(f"✔ ページ保存: {url} → {save_path}")
    except Exception as e:
        print(f"✘ ページ取得失敗: {url} - {e}")

# ドライバ起動 & 実行
driver = setup_driver()
scrape(BASE_URL, OUTPUT_DIR)
driver.quit()