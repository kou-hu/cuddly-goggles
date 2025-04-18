import os
from datetime import datetime
from openai import OpenAI

# OpenAIのAPIキーを安全に取得
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DIARY_FILE = "one_line_diary.txt"

# 今日の日記がすでに書かれてるか確認
def already_written_today():
    if not os.path.exists(DIARY_FILE):
        return False
    today = datetime.now().strftime("%Y-%m-%d")
    with open(DIARY_FILE, "r", encoding="utf-8") as f:
        return any(line.startswith(today) for line in f)

# 日記を書く処理
def write_diary():
    today = datetime.now().strftime("%Y-%m-%d")
    one_line = input("今日の一行日記をどうぞ：")
    with open(DIARY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{today} {one_line}\n")
    print("✅ 日記を保存したよ。")

    # AIから一言コメントもらう
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは優しい相棒です。日記に一言返してください。"},
            {"role": "user", "content": one_line}
        ]
    )

    ai_comment = response.choices[0].message.content
    print("🤖 AIからのひとこと：")
    print(ai_comment)

# 実行部分
if not already_written_today():
    write_diary()
else:
    print("今日はもう書いてあるよ！")

