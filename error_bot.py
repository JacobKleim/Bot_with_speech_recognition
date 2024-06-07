import os
import time

from telegram import Bot

from dotenv import load_dotenv


def main(message) -> None:
    load_dotenv()

    send_error_bot_token = os.environ['SEND_ERROR_BOT_TOKEN']
    error_bot = Bot(token=send_error_bot_token)
    admin_tg_id = os.environ['ADMIN_TG_ID']

    error_bot.send_message(chat_id=admin_tg_id, text=message)
    time.sleep(10)


if __name__ == '__main__':
    main()
