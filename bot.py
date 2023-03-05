import openai
import pymongo
from datetime import datetime
from pyrogram import Client, filters
from os import environ

# Environment variables
BOT_TOKEN = environ.get("TOKEN")
API_ID = environ.get("API_ID")
API_HASH = environ.get("API_HASH")
MONGO_URL = environ.get("MONGO_URL")

# Set up OpenAI API credentials
openai.api_key = "OPENAI_API"

# Set up PyMongo credentials and client
mongo_client = pymongo.MongoClient(MONGOURL)
db = mongo_client["mydatabase"]
responses_collection = db["responses"]
users_collection = db["users"]

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
app = Client("bot_token=BOT_TOKEN", api_id=API_ID, api_hash=API_HASH)

# Define start function
def start():
    message = "I'm a chatbot powered by GPT! Send me a message and I'll generate a response based on your input."
    return message

# Define function to add a user to the database
def add_user_to_db(user_id, is_paid=False):
    users_collection.insert_one({"user_id": user_id, "is_paid": is_paid, "remaining_replies": 20 if is_paid else 2})

@app.on_message(filters.command("start"))
def on_start_command(client, message):
    # Respond to start command
    client.send_message(message.chat.id, start())

@app.on_message()
def reply_to_message(client, message):
    user_id = message.from_user.id
    # Check if the user is in the database, add them if not
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        add_user_to_db(user_id)
        user = users_collection.find_one({"user_id": user_id})
    # Check if the user is a paid user
    is_paid = user.get("is_paid", False)
    remaining_replies = user.get("remaining_replies", 0)
    if remaining_replies == 0:
        client.send_message(message.chat.id, "Sorry, you have reached your daily limit of replies.")
        return
    # Get today's date in UTC
    today = datetime.utcnow().date()
    # Get the number of responses the user has made today
    user_responses = responses_collection.find_one({"user_id": user_id, "date": today})
    if user_responses and user_responses.get("count", 0) >= remaining_replies:
        client.send_message(message.chat.id, "Sorry, you have reached your daily limit of replies.")
        return
    # Generate text using the OpenAI API
    prompt = message.text
    generated_text = generate_text(prompt)
    client.send_message(message.chat.id, generated_text)
    # Decrement the user's remaining reply count for today
    users_collection.update_one({"user_id": user_id}, {"$inc": {"remaining_replies": -1}})
    # Increment the user's response count for today
    if user_responses:
        responses_collection.update_one({"_id": user_responses["_id"]}, {"$inc": {"count": 1}})
    else:
        responses_collection.insert_one({"user_id": user_id, "date": today, "count": 1})

@app.on_message(filters.command("add_paid_user") & filters.user(ADMIN))
def add_paid_user(client, message):
    user_id = message.text.split()[1]
    users_collection.update_one({"user_id": user_id}, {"$set": {"paid": True}}, upsert=True)
    client.send_message(message.chat.id, f"User {user_id} has been added as a paid user.")

# Start the bot
app.run()
