# GPT-Powered Chatbot
This bot is a chatbot powered by OpenAI's GPT-3.5-Turbo model. It generates responses to messages sent by users. Users have a limit on the number of responses they can receive per day, with paid users having a higher limit than free users. The bot uses a MongoDB database to keep track of user information and response counts. An admin can add paid users to the database.

## Environment Variables

To run this project, you will need to add the following environment variables.

`API_ID` = `your_api_id`

`API_HASH` = `your_api_hash`

`BOT_TOKEN` = `your_bot_token`

`MONGO_URL` = `your_mongodb_url`

`OPEN_API` = `your_openai_api_key`

## Installation

```bash
git clone https://github.com/i-ryme/TeleGPT
pip3 install -r requirements.txt
python3 bot.py
```
## License

[MIT](https://choosealicense.com/licenses/mit/)
