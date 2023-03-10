# GPT-Powered Chatbot 🤖
This bot is a chatbot powered by OpenAI's GPT-3.5-Turbo model. It generates responses to messages sent by users. Users have a limit on the number of responses they can receive per day, with paid users having a higher limit than free users. The bot uses a MongoDB database to keep track of user information and response counts. An admin can add paid users to the database.

## Environment Variables

To run this project, you will need to add environment variables, please refer [bot.py](https://github.com/i-ryme/TeleGPT/blob/bfe3227d4fc84f555f122749e9f7f61ce1c14471/bot.py#L8)

## Installation

```bash
git clone https://github.com/i-ryme/TeleGPT
pip3 install -r requirements.txt
python3 bot.py
```

## Deployment

**Before you deploy on heroku, you should fork the repo and change its name to anything else**<br>

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)</br>

## Support

For support, email ryme@duck.com or ping me at telegram [@iryme](https://telegram.me/iryme).
## License

[MIT](https://choosealicense.com/licenses/mit/)
