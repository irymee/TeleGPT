import openai
import pymongo
from datetime import datetime
from pyrogram import Client, filters

# Set up OpenAI API credentials
openai.api_key = "YOUR_API_KEY"

# Set up PyMongo credentials and client
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["mydatabase"]
responses_collection = db["responses"]

# Define function to generate text using the gpt-3.5-turbo model
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        n=1,
        stop=None,
        model="gpt-3.5-turbo"
    )
    message = response.choices[0].text.strip()
    return message

# Define Pyrogram bot function
app = Client("my_bot_token", api_id=API_ID, api_hash=API_HASH)

# Define start function
def start():
    message = "I'm a chatbot powered by GPT! Send me a message and I'll generate a response based on your input."
    return message

@app.on_message(filters.command("start"))
def on_start_command(client, message):
    # Respond to start command
    client.send_message(message.chat.id, start())

@app.on_message()
def reply_to_message(client, message):
    user_id = message.from_user.id
    # Get today's date in UTC
    today = datetime.utcnow().date()
    # Check if user is a paid user
    is_paid_user = False  # replace with logic to check if user is paid
    if is_paid_user:
        max_responses_per_day = 20
    else:
        max_responses_per_day = 2
    # Get the number of responses the user has made today
    user_responses = responses_collection.find_one({"user_id": user_id, "date": today})
    if user_responses and user_responses.get("count", 0) >= max_responses_per_day:
        client.send_message(message.chat.id, f"Sorry, you have reached the limit of {max_responses_per_day} responses per day.")
        return
    # Generate text using the OpenAI API
    prompt = message.text
    generated_text = generate_text(prompt)
    client.send_message(message.chat.id, generated_text)
    # Increment the user's response count for today
    if user_responses:
        responses_collection.update_one({"_id": user_responses["_id"]}, {"$inc": {"count": 1}})
    else:
        responses_collection.insert_one({"user_id": user_id, "date": today, "count": 1})

@app.on_message(filters.command("add_paid_user"))
def add_paid_user(client, message):
    # Check if user is an admin (replace with your own logic to check for admin status)
    is_admin = False
    if not is_admin:
        client.send_message(message.chat.id, "Sorry, you are not authorized to perform this action.")
        return
    # Get user ID and add to database
    user_id = message.text.split()[1]  # Assumes format "/add_paid_user <user_id>"
    responses_collection.insert_one({"user_id": user_id, "date": datetime.utcnow().date(), "count": 0})
    client.send_message(message.chat.id, f"User {user_id} has been added as a paid user.")


# Start the bot
app.run()

"""
When the user sends the `/start` command to the bot, the `on_start_command` function is triggered and sends a welcome message containing a brief description of the bot's capabilities. The bot then listens for incoming messages and generates responses using the OpenAI API's GPT-3.5-Turbo model. If the user exceeds their daily limit of 10 responses, the bot will notify them and stop generating responses.
"""
