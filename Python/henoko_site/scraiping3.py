import os
import json
import asyncio
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from urllib.parse import urlparse, urljoin, urldefrag
from playwright.async_api import async_playwright


# プロジェクトディレクトリ：C:\Users\yohens\Documents\vscode\Python\henoko_site
# 仮想環境をacvtivateさせてから実行すること
# vscodeターミナルにてhenoko_siteプロジェクトフォルダへ移動("cd .\henoko_site\")
# 作成済の仮想環境(.henoko_site_venv)を有効化(".henoko_site_venv\Scripts\activate")
# vscode画面右下から"3.13.0(.henoko_site_venv)"を選択(C:\Users\yohens\Documents\vscode\Python\henoko_site\.henoko_site_venv\Scripts\python.exe)
# 実行時には毎回、ターミナル左に(.henoko_site_venv)となっていることと、右下"3.13.0(.henoko_site_venv)となっていることを確認すること


visited = set()
manifest = {}
resource_folder = "assets"

# ファイル名処理
def sanitize_filename(url):
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path or path.endswith("/"):
        path += "index.html"
    return path.replace("/", "_")

def get_local_resource_name(resource_url):
    parsed = urlparse(resource_url)
    name = parsed.path.strip("/")
    if not name or name.endswith("/"):
        name += "index"
    return name.replace("/", "_")

async def download_resource(page, resource_url, folder, log):
    try:
        name = get_local_resource_name(resource_url)
        filepath = os.path.join(folder, name)
        if not os.path.exists(filepath):
            response = await page.request.get(resource_url)
            if response.ok:
                content = await response.body()
                with open(filepath, "wb") as f:
                    f.write(content)
                log(f"📦 リソース: {resource_url} -> {name}")
        return os.path.join(resource_folder, name)
    except Exception as e:
        log(f"⚠️ 失敗: {resource_url} - {e}")
        return resource_url

async def download_page(browser, url, base_url, folder, log):
    global visited, manifest
    url, _ = urldefrag(url)
    if url in visited:
        return
    visited.add(url)

    page = await browser.new_page()
    try:
        await page.goto(url, timeout=15000)
        await page.wait_for_load_state('networkidle')
    except Exception as e:
        log(f"❌ ページ取得失敗: {url} - {e}")
        await page.close()
        return

    html = await page.content()

    for selector, attr in [("img", "src"), ("script", "src"), ("link", "href")]:
        elements = await page.locator(selector).all()
        for el in elements:
            try:
                val = await el.get_attribute(attr)
                if val and not val.startswith("data:") and not val.startswith("mailto:"):
                    resource_url = urljoin(url, val)
                    local_path = await download_resource(page, resource_url, os.path.join(folder, resource_folder), log)
                    html = html.replace(val, local_path)
            except:
                continue

    filename = sanitize_filename(url)
    filepath = os.path.join(folder, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    log(f"✅ ページ保存: {url} -> {filepath}")

    manifest[url] = filename

    links = await page.locator('a').all()
    for link in links:
        try:
            href = await link.get_attribute("href")
            if href:
                next_url = urljoin(url, href)
                parsed = urlparse(next_url)
                if parsed.netloc == urlparse(base_url).netloc:
                    await download_page(browser, next_url, base_url, folder, log)
        except:
            continue

    await page.close()

async def download_entire_site(start_url, folder, log):
    global visited, manifest
    visited = set()
    manifest = {}

    os.makedirs(os.path.join(folder, resource_folder), exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        await download_page(browser, start_url, start_url, folder, log)
        await browser.close()

    manifest_path = os.path.join(folder, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    log(f"\n📄 manifest.json 保存: {manifest_path}")
    log(f"\n🎉 ダウンロード完了: {folder}")

def run_async_task(start_url, folder, log):
    asyncio.run(download_entire_site(start_url, folder, log))

# GUI構築
def start_gui():
    root = tk.Tk()
    root.title("サイト完全保存ツール（JavaScript対応）")

    tk.Label(root, text="保存対象URL：").grid(row=0, column=0, sticky="w")
    url_entry = tk.Entry(root, width=60)
    url_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="保存先フォルダ：").grid(row=1, column=0, sticky="w")
    folder_entry = tk.Entry(root, width=60)
    folder_entry.grid(row=1, column=1, padx=5, pady=5)

    def select_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder)

    browse_button = tk.Button(root, text="参照", command=select_folder)
    browse_button.grid(row=1, column=2, padx=5)

    log_box = scrolledtext.ScrolledText(root, width=80, height=25)
    log_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)
        root.update()

    def on_download():
        url = url_entry.get().strip()
        folder = folder_entry.get().strip()
        if not url or not folder:
            messagebox.showwarning("入力エラー", "URLと保存先を入力してください。")
            return
        log_box.delete(1.0, tk.END)
        threading.Thread(target=run_async_task, args=(url, folder, log), daemon=True).start()

    download_button = tk.Button(root, text="ダウンロード開始", command=on_download)
    download_button.grid(row=2, column=1, pady=10)

    root.mainloop()

if __name__ == '__main__':
    start_gui()