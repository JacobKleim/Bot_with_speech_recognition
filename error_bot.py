import os
import time

from telegram import Bot

send_error_bot_token = os.environ['SEND_ERROR_BOT_TOKEN']
error_bot = Bot(token=send_error_bot_token)
admin_tg_id = os.environ['ADMIN_TG_ID']


def notify_admin(message):
    error_bot.send_message(chat_id=admin_tg_id, text=message)
    time.sleep(10)
