# Bot_with_speech_recognition
 

## Environment      
 Сreate and activate a virtual environment  
   ```
   python3 -m venv venv
   ```
   ```bash
   source venv/Scripts/activate
   ```
 Get a bot token using **@BotFather** on Telegram.
 Create an .env file and put the bot token in there:
   ```python 
   TELEGRAM_BOT_TOKEN=bot_token
   ```

## Requirements
   Update the Python package manager to the latest version:
   ```
   python -m pip install --upgrade pip
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