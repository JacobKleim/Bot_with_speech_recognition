import logging
import os
import time

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_detect_texts import detect_intent_texts
from error_bot import notify_admin

load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

credentials_path = os.getenv("CREDENTIALS")
dialog_flow_agent_id = os.getenv("DIALOG_FLOW_AGENT_ID")
language_code = "ru-RU"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    text = update.message.text
    response = detect_intent_texts(
        dialog_flow_agent_id,
        update.effective_user.id,
        [text],
        language_code)
    if response:
        update.message.reply_text(response)


def main() -> None:
    """Start the bot."""
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    max_retries = 5
    retry_count = 0

    while True:
        try:
            updater = Updater(bot_token)

            dispatcher = updater.dispatcher

            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(CommandHandler("help", help_command))

            dispatcher.add_handler(
                MessageHandler(Filters.text & ~Filters.command, echo))
            updater.start_polling()

            updater.idle()

        except ConnectionError as con_error:
            logger.error(f'Error{con_error}')
            notify_admin(f"error: {con_error}")
            retry_count += 1
            if retry_count >= max_retries:
                time.sleep(60)
                retry_count = 0
        except requests.exceptions.ReadTimeout as rt_error:
            logger.error(f'Error{rt_error}')
            notify_admin(f"error: {rt_error}")
            time.sleep(60)

        except Exception as e:
            logger.error(f'ERROR {e}')
            notify_admin(f"error: {e}")
            time.sleep(5)


if __name__ == '__main__':
    main()
