
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
import os
import datetime

app = Flask(__name__)

# あなたのチャネルアクセストークンとシークレットに置き換えてね
LINE_CHANNEL_ACCESS_TOKEN = '2074152eebe12b4fa19a3df502fdf993'
LINE_CHANNEL_SECRET = '5NBmdmiUOtIJGnLrVxMNR/TXV+abV8qPB1Fskjta6p1FdK7uklQ5d7JrOU+IqRQbOw6L95gtEAWRWAMaHj5ENDP4EPE/OHW9SVnJL1sebhe0bOabdVYX0YRO4bSoZL8KUr++Rqi9KBOjKOKf9JXGNwdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

DIARY_FILE = 'diary.json'

# ファイルの読み書き処理
def load_diary():
    if os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_diary(data):
    with open(DIARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    today = str(datetime.date.today())

    diary = load_diary()

    if user_id not in diary:
        diary[user_id] = {}

    if text.startswith("日記:"):
        content = text[3:].strip()
        diary[user_id][today] = content
        save_diary(diary)
        reply = f"✅ 日記を保存したよ！\n\n{content}"
    elif "今日の分" in text:
        content = diary.get(user_id, {}).get(today, "まだ日記が書かれていないみたい。")
        reply = f"📅 今日の日記:\n{content}"
    elif "過去" in text:
        past_entries = diary.get(user_id, {})
        if past_entries:
            random_date = sorted(past_entries.keys())[-1]  # 最後の日記
            reply = f"📖 過去の日記（{random_date}）:\n{past_entries[random_date]}"
        else:
            reply = "まだ日記がひとつもないよ。"
    else:
        reply = "「日記:〇〇」で日記を書けるよ！\n「今日の分」や「過去」で読み返せるよ！"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run()


































































































































