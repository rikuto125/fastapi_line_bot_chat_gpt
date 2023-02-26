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


@router.post("/gpt")
async def generate_message(
        request: Request,
        background_tasks: BackgroundTasks
):
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", "")
    )

    if not events:
        raise HTTPException(status_code=400, detail="Invalid request")

    text = str(events[0].message.text)
    reply_message = generate_text(text)

    print("text: ", text)
    print("reply_message", reply_message)

    background_tasks.add_task(handle_events_gpt, events, reply_message)

    return {"message": "OK"}
