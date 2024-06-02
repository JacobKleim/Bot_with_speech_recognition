import logging
import os
import random
import time

import requests
import telegram
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

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


def echo(event, vk_api):
    response = detect_intent_texts(
        dialog_flow_agent_id,
        event.user_id,
        [event.text],
        language_code)
    if response:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response,
            random_id=random.randint(1, 1000)
        )


def main() -> None:
    vk_group_token = os.getenv("VK_GROUP_TOKEN")
    max_retries = 5
    retry_count = 0

    while True:
        try:
            vk_session = vk.VkApi(token=vk_group_token)
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    echo(event, vk_api)

        except ConnectionError as con_error:
            logger.error(f'Error {con_error}')
            try:
                notify_admin(f"error: {con_error}")
            except telegram.error.NetworkError as ne:
                logger.error(f'NetworkError {ne} while notifying admin')
            retry_count += 1
            if retry_count >= max_retries:
                time.sleep(60)
                retry_count = 0

        except requests.exceptions.ReadTimeout as rt_error:
            logger.error(f'Error {rt_error}')
            try:
                notify_admin(f"error: {rt_error}")
            except telegram.error.NetworkError as ne:
                logger.error(f'NetworkError {ne} while notifying admin')
            time.sleep(60)

        except telegram.error.NetworkError as ne:
            logger.error(f'NetworkError {ne}')
            time.sleep(60)

        except Exception as e:
            logger.error(f'ERROR {e}')
            try:
                notify_admin(f"error: {e}")
            except telegram.error.NetworkError as ne:
                logger.error(f'NetworkError {ne} while notifying admin')
            time.sleep(5)


if __name__ == '__main__':
    main()
