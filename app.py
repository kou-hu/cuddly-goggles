from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI
import os

# Flaskアプリ起動
app = Flask(__name__)

# 各種キーを環境変数から取得
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# LINEからのWebhookを受け取るエンドポイント
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("エラー:", e)
        abort(400)

    return "OK"

# メッセージを受け取ったときの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # OpenAIでコメント生成
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは優しい相棒です。日記に一言返してください。"},
            {"role": "user", "content": user_message}
        ]
    )

    ai_reply = response.choices[0].message.content

    # LINEで返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ai_reply)
    )

if __name__ == "__main__":
    app.run()

