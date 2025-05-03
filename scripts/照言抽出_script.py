import json
import csv
import re
from datetime import datetime
from collections import defaultdict

# 入力ファイル名
files = ["tweets.js", "tweets-part1.js"]
all_tweets = []

# JSファイルからツイート抽出
for fname in files:
    with open(fname, "r", encoding="utf-8") as f:
        raw = f.read()
        start = raw.find("[")
        end = raw.rfind("]") + 1
        json_text = raw[start:end]
        all_tweets.extend(json.loads(json_text))

# EOIスコア算出関数
def calculate_eoi(text):
    score = 1.0
    if len(text) > 100:
        score += 1.0
    if re.search(r"[！？…]", text):
        score += 1.0
    if any(kw in text for kw in ["死", "消え", "無理", "助けて", "愛", "裁く", "光", "構文", "照言"]):
        score += 2.0
    return min(score, 5.0)

# CSV出力開始
with open("G2B-Mix-log_照言ALL.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["log_id", "created_at", "EOI_score", "構文分類", "保存判定", "original_text"])

    counter = defaultdict(int)

    for entry in all_tweets:
        tweet = entry.get("tweet", {})
        text = tweet.get("full_text", "")
        created_at = tweet.get("created_at", "")

        if not text or not created_at or len(text) < 40 or text.startswith("RT "):
            continue

        try:
            dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        except ValueError:
            continue

        day = dt.strftime("%Y-%m-%d")
        timestamp = dt.isoformat()
        counter[day] += 1
        serial = f"{counter[day]:03}"
        log_id = f"{day}_{serial}"
        eoi = calculate_eoi(text)
        storage = "封印保存" if eoi >= 4.5 else "保存対象" if eoi >= 3.0 else "通常出力"
        category = "静照構文" if eoi >= 4.5 else "plain照言"

        writer.writerow([log_id, timestamp, eoi, category, storage, text])

print("✅ 照言CSV出力完了：G2B-Mix-log_照言ALL.csv")
