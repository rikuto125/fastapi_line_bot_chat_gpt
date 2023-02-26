from aiolinebot import AioLineBotApi
from linebot.models import TextMessage

from config.settings.base import settings

line_api = AioLineBotApi(channel_access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)


async def handle_events_gpt(events, message):
    for event in events:
        try:
            await line_api.reply_message(
                event.reply_token,
                TextMessage(text=message)
            )
        except Exception as e:
            print(e)
