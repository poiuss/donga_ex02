import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

ARTICLE_URL = "https://n.news.naver.com/article/082/0001360934?sid=102"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Referer": "https://news.naver.com/",
}

def safe_filename(name: str, max_len: int = 80) -> str:
    name = re.sub(r'[\\/:*?"<>|]+', "_", name).strip()
    name = re.sub(r"\s+", " ", name)
    return (name[:max_len] if len(name) > max_len else name) or "image"

def guess_ext(url: str) -> str:
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        if path.endswith(ext):
            return ext
    return ".jpg"

def extract_image_urls(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    seen = set()

    # 1) 공유 대표 이미지(보통 1개)
    meta = soup.select_one("meta[property='og:image']")
    if meta and meta.get("content"):
        u = meta["content"].strip()
        if u:
            seen.add(u)
            urls.append(u)

    # 2) 본문 이미지들 (n.news 기준 dic_area가 가장 흔함)
    for img in soup.select("#dic_area img, #newsct_article img, .newsct_article img"):
        src = img.get("data-src") or img.get("data-original") or img.get("src")
        if not src:
            continue
        src = urljoin(base_url, src)
        if src not in seen:
            seen.add(src)
            urls.append(src)

    return urls

def download(session: requests.Session, img_url: str, save_dir: str, base_name: str) -> str:
    r = session.get(img_url, headers=headers, timeout=15, stream=True)
    r.raise_for_status()

    ext = guess_ext(img_url)
    fpath = os.path.join(save_dir, f"{safe_filename(base_name)}{ext}")

    with open(fpath, "wb") as f:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)

    return fpath

def main():
    session = requests.Session()
    res = session.get(ARTICLE_URL, headers=headers, timeout=10)
    res.raise_for_status()

    img_urls = extract_image_urls(res.text, ARTICLE_URL)
    if not img_urls:
        print("이미지를 못 찾았어.")
        return

    save_dir = os.path.join(os.getcwd(), "article_images")
    os.makedirs(save_dir, exist_ok=True)

    print(f"찾은 이미지 수: {len(img_urls)}")
    saved = 0
    for i, u in enumerate(img_urls, 1):
        try:
            path = download(session, u, save_dir, f"naver_article_img_{i:02d}")
            saved += 1
            print(f"[저장됨] {path}")
        except Exception as e:
            print(f"[실패] {u} -> {e}")

    print(f"\n저장 완료: {saved}개")
    print("폴더:", save_dir)

if __name__ == "__main__":
    main()