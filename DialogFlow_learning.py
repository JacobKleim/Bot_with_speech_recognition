import json
import os

from dotenv import load_dotenv

load_dotenv()


credentials_path = os.getenv("CREDENTIALS")
dialog_flow_agent_id = os.getenv("DIALOG_FLOW_AGENT_ID")
language_code = "ru-RU"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


with open("data.json", "r", encoding="UTF-8") as file:
    data_json = file.read()


phrases = json.loads(data_json)
training_phrases = phrases['Устройство на работу']['questions']
answer = phrases['Устройство на работу']['answer']


def create_intent(project_id, display_name,
                  training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
            )

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


create_intent(dialog_flow_agent_id, 'Как устроиться к вам на работу',
              training_phrases, [answer])
