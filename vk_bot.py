import logging
import os
import random
import time

from dotenv import load_dotenv

import telegram
import vk_api as vk
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_detect_texts import detect_intent_texts

from tg_bot import TelegramErrorHandler


logger = logging.getLogger('VK_BOT')


LANGUAGE_CODE = "ru-RU"


def get_answer(event, vk_api, dialog_flow_agent_id):
    """Answer the user message using Dialogflow."""
    response = detect_intent_texts(
        dialog_flow_agent_id,
        event.user_id,
        [event.text],
        LANGUAGE_CODE)
    if not response.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main() -> None:
    load_dotenv()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    dialog_flow_agent_id = os.getenv("DIALOG_FLOW_AGENT_ID")
    credentials_path = os.getenv("CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    vk_group_token = os.getenv("VK_GROUP_TOKEN")

    send_error_tg_bot_token = os.environ['SEND_ERROR_BOT_TOKEN']
    admin_tg_id = os.environ['ADMIN_TG_ID']

    telegram_error_handler = TelegramErrorHandler(send_error_tg_bot_token,
                                                  admin_tg_id)
    telegram_error_handler.setLevel(logging.ERROR)
    logger.addHandler(telegram_error_handler)

    while True:
        try:
            logger.info('Bot started')
            vk_session = vk.VkApi(token=vk_group_token)
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    get_answer(event, vk_api, dialog_flow_agent_id)

        except Exception as e:
            try:
                logger.error(f'ERROR {e}')
            except telegram.error.NetworkError as ne:
                logger.error(f'NetworkError {ne} while notifying admin')
            time.sleep(10)


if __name__ == '__main__':
    main()
