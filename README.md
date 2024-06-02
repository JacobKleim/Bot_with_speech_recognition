# Bot_with_speech_recognition

This repository contains two bots: a Telegram bot and a VK bot, developed using Python. Each of them is designed to interact with users through the respective messengers.

## Telegram Bot

The Telegram bot has the following functionality:

- Responds to user text messages.
- Utilizes DialogFlow for message processing and providing responses.
- Can be configured for various commands and dialogue scenarios.

### Example Dialogue with the Telegram Bot:

![Telegram Bot](https://github.com/JacobKleim/Bot_with_speech_recognition/assets/119351169/a95e6728-d910-4f2c-a812-52c05bd852c5)
## VK Bot

The VK bot provides similar functionality but for the VKontakte social network. It also uses DialogFlow for message processing and responding.

### Example Dialogue with the VK Bot:

![VK Bot](https://github.com/JacobKleim/Bot_with_speech_recognition/assets/119351169/9bb7ac3d-c177-4c31-95e2-352ce43d980d)

## DialogFlow

DialogFlow is a platform for creating chatbots, which has extensive capabilities for natural language processing and creating conversational interfaces. We use DialogFlow to train our bots and provide them with intelligent capabilities.

## Examples of Working Bots

You can try out the operation of our bots by following these links:

- [Telegram Bot](https://t.me/assistant_peoples_bot)
- [VK Bot](https://vk.com/invite/2yzODoo)

## Environment      
 Сreate and activate a virtual environment  
   ```
   python -m venv venv
   ```
   ```bash
   source venv/Scripts/activate
   ```
 Get a bot token using **@BotFather** on Telegram.
 Create an .env file and put the bot token in there:
   ```python 
   TELEGRAM_BOT_TOKEN=tg bot token
   ```
   ```python 
   VK_GROUP_TOKEN=vk group token
   ```
   ```python 
   CREDENTIALS=path for 'GOOGLE_APPLICATION_CREDENTIALS'
   ```
   ```python 
   DIALOG_FLOW_AGENT_ID=dialogflow project id
   ```
   ```python 
   ADMIN_TG_ID=admin telegram id
   ```
   ```python 
   SEND_ERROR_BOT_TOKEN=token for error_bot
   ```

## Requirements
   Update the Python package manager to the latest version:
   ```
   python3 -m pip install --upgrade pip
   ```
   Install dependencies:
   ```
   pip install -r requirements.txt
   ``` 



## Run
   ```
   python tg_bot.py
   ```
   ```
   python vk_bot.py
   ```
