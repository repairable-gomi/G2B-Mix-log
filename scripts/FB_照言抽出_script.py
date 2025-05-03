import json
import re
from datetime import datetime
from collections import defaultdict

# 入力ファイル（例：Facebookエクスポートファイルの1つ）
INPUT_FILE = "your_posts__check_and_videos_1.json"
OUTPUT_FILE = "FB-Mix-log_照言ALL.jsonl"

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

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

output = []
counter = defaultdict(int)

for entry in raw_data:
    timestamp = entry.get("timestamp")
    texts = entry.get("data", [])

    for data in texts:
        post = data.get("post", "").strip()
        if not post or len(post) < 20:
            continue

        dt = datetime.fromtimestamp(timestamp)
        day = dt.strftime("%Y-%m-%d")
        timestamp_iso = dt.isoformat()
        counter[day] += 1
        serial = f"{counter[day]:03}"
        log_id = f"{day}_{serial}"

        eoi = calculate_eoi(post)
        storage = "封印保存" if eoi >= 4.5 else "保存対象" if eoi >= 3.0 else "通常出力"
        category = "静照構文" if eoi >= 4.5 else "plain照言"

        output.append({
            "log_id": log_id,
            "timestamp": timestamp_iso,
            "EOI_score": eoi,
            "構文分類": category,
            "保存判定": storage,
            "original_text": post
        })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for entry in output:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"✅ Facebook照言抽出完了：{OUTPUT_FILE}")
