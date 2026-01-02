import os
import re
import requests
from bs4 import BeautifulSoup

ARTICLE_URL = "https://n.news.naver.com/article/082/0001360934?sid=102"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Referer": "https://news.naver.com/",
}

def safe_filename(name: str, max_len: int = 80) -> str:
    name = re.sub(r'[\\/:*?"<>|]+', "_", name).strip()
    name = re.sub(r"\s+", " ", name)
    return (name[:max_len] if len(name) > max_len else name) or "article"

def get_article_text(session: requests.Session, url: str) -> dict:
    r = session.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # 제목 (케이스별 대비)
    title_el = soup.select_one("#title_area span") or soup.select_one("h2#title_area") or soup.select_one("h2.media_end_head_headline")
    title = title_el.get_text(strip=True) if title_el else ""

    # 본문
    body_el = soup.select_one("#dic_area") or soup.select_one("#newsct_article") or soup.select_one("article#dic_area")
    body = body_el.get_text("\n", strip=True) if body_el else ""

    # 날짜
    date_el = soup.select_one("span.media_end_head_info_datestamp_time") or soup.select_one("time")
    date = date_el.get_text(strip=True) if date_el else ""

    # 언론사(가능하면)
    press_el = soup.select_one("a.media_end_head_top_logo img") or soup.select_one("a.press_logo img")
    press = press_el.get("alt", "").strip() if press_el else ""

    return {"title": title, "body": body, "date": date, "press": press}

def main():
    session = requests.Session()
    data = get_article_text(session, ARTICLE_URL)

    if not data["title"] and not data["body"]:
        print("기사 텍스트를 못 찾았어. (셀렉터 변경 필요)")
        return

    save_dir = os.path.join(os.getcwd(), "article_texts")
    os.makedirs(save_dir, exist_ok=True)

    fname = safe_filename(data["title"] if data["title"] else "naver_article") + ".txt"
    fpath = os.path.join(save_dir, fname)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(f"URL: {ARTICLE_URL}\n")
        if data["press"]:
            f.write(f"언론사: {data['press']}\n")
        if data["date"]:
            f.write(f"날짜: {data['date']}\n")
        if data["title"]:
            f.write(f"\n제목: {data['title']}\n")
        f.write("\n본문:\n")
        f.write(data["body"].strip() + "\n")

    print("저장 완료:", fpath)

if __name__ == "__main__":
    main()