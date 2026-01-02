import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우 한글 폰트
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1️⃣ 시간대별 조회 수 (선 그래프)
df1 = pd.DataFrame({
    "hour": [9, 12, 15, 18, 21],
    "views": [120, 340, 560, 430, 290]
})
axes[0].plot(df1["hour"], df1["views"])
axes[0].set_title("시간대별 기사 조회 수")
axes[0].set_xlabel("시간")
axes[0].set_ylabel("조회 수")

# 2️⃣ 매체별 기사 수 (막대 그래프)
df2 = pd.DataFrame({
    "media": ["A신문", "B신문", "C신문", "D신문"],
    "article_count": [25, 40, 15, 30]
})
axes[1].bar(df2["media"], df2["article_count"])
axes[1].set_title("매체별 기사 수 비교")
axes[1].set_xlabel("매체")
axes[1].set_ylabel("기사 수")

# 3️⃣ 조회 수 vs 댓글 수 (산점도)
df3 = pd.DataFrame({
    "views": [120, 340, 560, 430, 290],
    "comments": [5, 18, 42, 30, 12]
})
axes[2].scatter(df3["views"], df3["comments"])
axes[2].set_title("조회 수와 댓글 수의 관계")
axes[2].set_xlabel("조회 수")
axes[2].set_ylabel("댓글 수")

plt.tight_layout()
plt.show()
