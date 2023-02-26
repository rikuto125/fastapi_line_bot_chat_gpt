from fastapi import APIRouter, Request, HTTPException
from starlette.background import BackgroundTasks
from app.services.gpt import generate_text
from app.services.line import handle_events_gpt
from config.settings.base import settings
from linebot import WebhookParser

router = APIRouter(
    prefix='/line_user',
    tags=['line_user'],
)

parser = WebhookParser(channel_secret=settings.LINEBOT_CHANNEL_SECRET)

# 前回の会話を保存するための変数
conversation = {}


@router.post("/gpt")
async def generate_message(
        request: Request,
        background_tasks: BackgroundTasks
):
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", "")
    )

    text = str(events[0].message.text)

    if text == "reset":
        conversation[events[0].source.user_id] = ""
        message = "reset"
        background_tasks.add_task(handle_events_gpt, events, message)
        return {"message": "OK"}

    # 前回の会話を取得する
    prev_conversation = conversation.get(events[0].source.user_id)
    # 前回の会話があれば、前回の出力を前につける
    if prev_conversation:
        text = prev_conversation + "\n" + text
        print("pre_text: ", text)

    reply_message = generate_text(text)

    # 今回の会話を保存する
    conversation[events[0].source.user_id] = reply_message

    print("text: ", text)
    print("reply_message", reply_message)

    background_tasks.add_task(handle_events_gpt, events, reply_message)

    return {"message": "OK"}
