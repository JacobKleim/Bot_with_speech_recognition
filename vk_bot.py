import logging
import os
import random
import time

from dotenv import load_dotenv

import telegram
import vk_api as vk
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_detect_texts import detect_intent_texts

import error_bot


logger = logging.getLogger(__name__)


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
            logger.error(f'ERROR {e}')
            try:
                error_bot.main(f"error: {e}")
            except telegram.error.NetworkError as ne:
                logger.error(f'NetworkError {ne} while notifying admin')
            time.sleep(5)


if __name__ == '__main__':
    main()
