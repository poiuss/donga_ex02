import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("news_daily.csv")

df["views"] = [120, 180, 220] * (len(df) // 3) + [120, 180, 220][: len(df) % 3]
df["media"] = ["A신문", "B신문", "A신문"] * (len(df) // 3) + ["A신문", "B신문", "A신문"][: len(df) % 3]

df["collected_at"] = pd.to_datetime(df["collected_at"])
df["collected_date"] = df["collected_at"].dt.date

grouped = df.groupby("media")["views"].mean()
daily_count = df.groupby("collected_date").size()

# 한 화면에 3개 그래프
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1. 히스토그램
axes[0].hist(df["views"], bins=5)
axes[0].set_title("기사 조회 수 분포")
axes[0].set_xlabel("조회 수")
axes[0].set_ylabel("기사 수")

# 2. 매체별 평균 조회 수
grouped.plot(kind="bar", ax=axes[1])
axes[1].set_title("매체별 평균 조회 수")
axes[1].set_xlabel("매체")
axes[1].set_ylabel("평균 조회 수")

# 3. 날짜별 기사 수 추이
daily_count.plot(kind="line", marker="o", ax=axes[2])
axes[2].set_title("날짜별 기사 수 추이")
axes[2].set_xlabel("날짜")
axes[2].set_ylabel("기사 수")

plt.tight_layout()
plt.show()