import logging
import os
import time

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_detect_texts import detect_intent_texts

import error_bot


logger = logging.getLogger(__name__)


LANGUAGE_CODE = "ru-RU"


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
    )


def get_answer(update: Update,
               context: CallbackContext,
               dialog_flow_agent_id) -> None:
    """Answer the user message using Dialogflow."""
    text = update.message.text
    response = detect_intent_texts(
        dialog_flow_agent_id,
        update.effective_user.id,
        [text],
        LANGUAGE_CODE)
    update.message.reply_text(response.fulfillment_text)


def main() -> None:
    """Start the bot."""
    load_dotenv()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    dialog_flow_agent_id = os.getenv("DIALOG_FLOW_AGENT_ID")
    credentials_path = os.getenv("CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']

    while True:
        try:
            updater = Updater(bot_token)

            dispatcher = updater.dispatcher

            dispatcher.add_handler(CommandHandler("start", start))

            dispatcher.add_handler(
                MessageHandler(Filters.text & ~Filters.command,
                               lambda update,
                               context: get_answer(update,
                                                   context,
                                                   dialog_flow_agent_id)))
            updater.start_polling()

            updater.idle()

        except Exception as e:
            logger.error(f'ERROR {e}')
            error_bot.main(f"error: {e}")
            time.sleep(5)


if __name__ == '__main__':
    main()
