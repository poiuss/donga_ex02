import pandas as pd
from datetime import datetime
import os

# 1) (API 대신) 가짜 응답 JSON 준비: 실제 API가 주는 형태를 흉내냄
fake_response = {
    "articles": [
        {
            "title": "AI 뉴스 예제 1",
            "publishedAt": "2026-01-02T09:00:00Z",
            "content": "키 없이 파이프라인 구조를 확인하기 위한 더미 기사입니다."
        },
        {
            "title": "AI 뉴스 예제 2",
            "publishedAt": "2026-01-02T10:30:00Z",
            "content": "API 호출 대신 JSON 구조→정리→저장 흐름만 테스트합니다."
        },
        {
            "title": "AI 뉴스 예제 3",
            "publishedAt": "2026-01-02T11:15:00Z",
            "content": "articles 배열을 순회하며 필요한 필드만 추출합니다."
        }
    ]
}

# 2) 응답 구조 확인(원래는 response.json().keys()로 보던 부분)
print("최상위 키:", fake_response.keys())

# 3) 기사 목록 꺼내기(원래 data = response.json(); articles = data["articles"]와 동일)
articles = fake_response["articles"]
print("기사 개수:", len(articles))

# 4) 필요한 항목만 선별해서 구조화(리스트 of dict 형태로 통일)
structured_data = []
for article in articles:
    structured_data.append({
        "title": article.get("title"),
        "date": article.get("publishedAt"),
        "content": article.get("content")
    })

# 5) DataFrame으로 변환해 정형 데이터 확인
df = pd.DataFrame(structured_data)

# 6) 수집 시점 기록(자동 수집 파이프라인에서 중요)
df["collected_at"] = datetime.now()

# 7) 상위 5개 확인(실습 확인용)
print(df.head())

# 8) CSV로 저장(utf-8-sig는 엑셀에서 한글 깨짐 방지에 유리)
output_file = "news_daily.csv"

if os.path.exists(output_file):
    df.to_csv(output_file, mode="a", header=False, index=False, encoding="utf-8-sig")
else:
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"저장 완료: {output_file}")