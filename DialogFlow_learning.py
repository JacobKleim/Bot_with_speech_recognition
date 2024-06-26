import argparse
import json
import os

from dotenv import load_dotenv

from google.cloud import dialogflow


def create_intent(project_id, display_name,
                  training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""

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


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="DialogFlow learning script")
    parser.add_argument('-d', '--data_path', type=str, default='data.json',
                        help='Path to the data JSON file')
    args = parser.parse_args()

    credentials_path = os.getenv("CREDENTIALS")
    dialog_flow_agent_id = os.getenv("DIALOG_FLOW_AGENT_ID")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    with open(args.data_path, "r", encoding="UTF-8") as file:
        json_content = file.read()

    phrases = json.loads(json_content)

    for intent_name, intent_info in phrases.items():

        training_phrases = intent_info['questions']
        answer = intent_info['answer']

        create_intent(dialog_flow_agent_id, intent_name,
                      training_phrases, [answer])


if __name__ == '__main__':
    main()
