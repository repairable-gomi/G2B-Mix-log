import json
import argparse
from datetime import datetime

# コマンドライン引数設定
parser = argparse.ArgumentParser(description="G2B照言フィルタ出力ツール")
parser.add_argument("--source", choices=["x", "fb", "both"], default="both", help="抽出元を指定")
parser.add_argument("--date", type=str, help="日付指定 (YYYY-MM-DD)")
parser.add_argument("--month", type=str, help="月指定 (YYYY-MM)")
args = parser.parse_args()

# ファイルパス指定
sources = {
    "x": "X_nekama_log/G2B-Mix-log_照言ALL.jsonl",
    "fb": "FB_realname_log/FB-Mix-log_照言ALL.jsonl"
}

# データ読込
entries = []
for key, path in sources.items():
    if args.source in [key, "both"]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                entries += [json.loads(line) for line in f if line.strip()]
        except FileNotFoundError:
            print(f"⚠️ ファイルが見つかりません: {path}")

# フィルタ処理
def match(entry):
    ts = entry.get("timestamp", "")
    if args.date:
        return ts.startswith(args.date)
    elif args.month:
        return ts.startswith(args.month)
    return False

filtered = [e for e in entries if match(e)]

# 出力ファイル名の生成
suffix = args.date or args.month or "filtered"
output_path = f"G2B-Mix-log_filtered_{suffix}.jsonl"

# 保存
with open(output_path, "w", encoding="utf-8") as f:
    for entry in filtered:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"✅ 抽出完了：{output_path}")
