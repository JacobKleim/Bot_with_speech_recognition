import logging
import os
import random

from dotenv import load_dotenv

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_detect_texts import detect_intent_texts


load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

credentials_path = os.getenv("CREDENTIALS")
dialog_flow_agent_id = os.getenv("DIALOG_FLOW_AGENT_ID")
language_code = "ru-RU"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


def echo(event, vk_api):
    responce = detect_intent_texts(
        dialog_flow_agent_id,
        event.user_id,
        [event.text],
        language_code)
    vk_api.messages.send(
        user_id=event.user_id,
        message=responce,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    vk_group_token = os.getenv("VK_GROUP_TOKEN")
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)