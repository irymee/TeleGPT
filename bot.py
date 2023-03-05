import openai
import pyrogram
import pymongo
from datetime import datetime

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
app = pyrogram.Client("my_bot_token", api_id=API_ID, api_hash=API_HASH)

@app.on_message()
def reply_to_message(client, message):
    user_id = message.from_user.id
    # Get today's date in UTC
    today = datetime.utcnow().date()
    # Get the number of responses the user has made today
    user_responses = responses_collection.find_one({"user_id": user_id, "date": today})
    if user_responses and user_responses.get("count", 0) >= 10:
        client.send_message(message.chat.id, "Sorry, you have reached the limit of 10 responses per day.")
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

# Start the bot
app.run()
