# GPT-Powered Chatbot 🤖
This bot is a chatbot powered by OpenAI's GPT-3.5-Turbo model. It generates responses to messages sent by users. Users have a limit on the number of responses they can receive per day, with paid users having a higher limit than free users. The bot uses a MongoDB database to keep track of user information and response counts. An admin can add paid users to the database.

## Environment Variables

To run this project, you will need to add environment variables, please refer [bot.py](https://github.com/i-ryme/TeleGPT/blob/main/bot.py)

## Installation

```bash
git clone https://github.com/i-ryme/TeleGPT
pip3 install -r requirements.txt
python3 bot.py
```

## Deployment

**BEFORE YOU DEPLOY ON HEROKU, YOU SHOULD FORK THE REPO AND CHANGE ITS NAME TO ANYTHING ELSE**<br>
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)</br>

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/i-ryme/TeleGPT&branch=main&name=telegpt)



## Support

For support, email ryme@duck.com or ping me at telegram [@iryme](https://telegram.me/iryme).
## License

[MIT](https://choosealicense.com/licenses/mit/)
