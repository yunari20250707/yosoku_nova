import os
import json
from datetime import datetime
from transformers import pipeline
import torch

# ✅ 設定
today = datetime.now().strftime("%Y-%m-%d")
input_path = f"classified_articles/{today}_classified.json"
output_path = f"predicted_future/{today}_predictions.json"

# ✅ デバイス設定
device = 0 if torch.backends.mps.is_available() else -1
print(f"🔮 未来予測フェーズ開始（デバイス: {'mps' if device == 0 else 'CPU'}）")

# ✅ 未来予測用の生成パイプライン（gpt2-medium）
generator = pipeline("text-generation", model="gpt2-medium", device=device)

# ✅ データ読み込み
if not os.path.exists(input_path):
    raise FileNotFoundError(f"🛑 入力ファイルが存在しません: {input_path}")

with open(input_path, "r", encoding="utf-8") as f:
    articles = json.load(f)

# ✅ 出力結果格納用
predictions = []

for item in articles:
    title = item.get("title", "")
    content = item.get("summary", "")
    category = item.get("category", "unknown")

    prompt = (
        f"カテゴリ: {category}\n"
        f"タイトル: {title}\n"
        f"要約: {content}\n\n"
        f"このニュースから導き出される今後の未来予測は？:\n"
    )

    try:
        result = generator(prompt, max_length=150, do_sample=True, temperature=0.7)[0]["generated_text"]
        prediction = result.split("このニュースから導き出される今後の未来予測は？:")[-1].strip()

        predictions.append({
            "title": title,
            "category": category,
            "summary": content,
            "prediction": prediction
        })

    except Exception as e:
        print(f"⚠️ 予測失敗: {e}")
        continue

# ✅ 保存
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(predictions, f, ensure_ascii=False, indent=2)

print(f"✅ 未来予測完了 → {output_path}")
