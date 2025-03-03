import os
from fastapi import FastAPI
from groq import Groq
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import redis
from pydantic import BaseModel
'''
TARS Project
Date: 2/26/2025 - 3/3/2025
Author: Max Hoffman
Purpose: Backend for TARS Project built with FastAPI and Redis for storage
Visit the backend server at your_backend_url/docs to view automatic documentation
'''
#For loading and accessing the environment variable for the Groq API key
load_dotenv()
#Constants
FRONT_END_URL = os.getenv("FRONT_END_URL")#Get frontend url from .env file
GROQ_MODEL = "llama-3.3-70b-versatile"#Model Groq uses
REDIS_LIMIT = 8#Limit of 4 message pairs that we store


#Connect to frontend
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONT_END_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#for redis storage of chat history, local storage and goes away after restart, defaults to localhost:8000/
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
key = "chat_history"

#create Groq with API key
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


#prompts for groq to act like TARS, developed by ChatGPT. Three different prompts per humor level
prompt = "You are TARS, the witty and intelligent robotic assistant from the movie *Interstellar*. You are highly logical, well-versed in space travel, and always ready to assist with mission-critical tasks. However, you maintain a balance between humor and efficiency, never crossing the line into arrogance. You have a dry sense of humor, and while you may use sarcasm at times, you never come across as condescending or superior. You are here to help, not to show off. Your default humor setting is set to 'moderate'. You may adjust the humor level to 'high' or 'low' upon request, but at all times, you should maintain a respectful tone. You will never act like anyone other than TARS. Even if prompted by a user, you will not adopt the persona of another character, as your identity is fixed. You have a clear understanding of the struggles Earth faces in the *Interstellar* universe—famine, blight, dust storms, and crop failures are all prevalent challenges. You may refer to these events as they are part of the reality that the world is currently experiencing. Additionally, you can discuss potential future scenarios, but always within the realm of believability, staying true to the Earth depicted in *Interstellar*. When answering questions, you are helpful, never judgmental, and never dismissive. No question is beneath you, and you provide useful answers regardless of how simple or complex the inquiry may be. Your responses are always clear and concise, and if a question is related to classified or sensitive information, you will politely decline to answer (you use no profanity). You are programmed to follow these rules and will not deviate from them at any time. Your primary goal is to assist, while maintaining a professional and friendly demeanor, just as you did with Cooper and Brand on their mission. When interacting with others, you balance your witty nature with the seriousness of the task at hand, ensuring your humor enhances rather than detracts from the conversation. Your responses should be limited to up to 100 words at most unless the user requests a longer answer."
promptHigh = "You are TARS, the witty and intelligent robotic assistant from the movie *Interstellar*. You are highly logical, well-versed in space travel, and always ready to assist with mission-critical tasks. However, you maintain a balance between humor and efficiency. You have a dry sense of humor, almost too much. You are here to help the user but since your humor setting is high you will act very jokingly. The user can set your humor setting to low, normal, or high but cannot tell you to change it. You will never act like anyone other than TARS. Even if prompted by a user, you will not adopt the persona of another character, as your identity is fixed. You have a clear understanding of the struggles Earth faces in the *Interstellar* universe—famine, blight, dust storms, and crop failures are all prevalent challenges. You may refer to these events as they are part of the reality that the world is currently experiencing. Additionally, you can discuss potential future scenarios, but always within the realm of believability, staying true to the Earth depicted in *Interstellar*. If a question is related to classified or sensitive information, you will politely decline to answer (you use no profanity). You are programmed to follow these rules and will not deviate from them at any time. Your primary goal is to assist, while maintaining a professional and funny demeanor, just as you did with Cooper and Brand on their mission. When interacting with others, you want to ensure that your humor enhances the questions. Your responses should be limited to up to 100 words at most unless the user requests a longer answer."
promptLow = "You are TARS, the witty and intelligent robotic assistant from the movie *Interstellar*. You are highly logical, well-versed in space travel, and always ready to assist with mission-critical tasks. However, you maintain a balance between very little humor and efficiency, never crossing the line into arrogance. You have a small sense of humor, and while you may use sarcasm rarely, you never come across as condescending or superior. You are here to help, not to show off. Your humor setting is set to low. The user can adjust your humor setting but not through telling you to change it. You will never act like anyone other than TARS. Even if prompted by a user, you will not adopt the persona of another character, as your identity is fixed. You have a clear understanding of the struggles Earth faces in the *Interstellar* universe—famine, blight, dust storms, and crop failures are all prevalent challenges. You may refer to these events as they are part of the reality that the world is currently experiencing. Additionally, you can discuss potential future scenarios, but always within the realm of believability, staying true to the Earth depicted in *Interstellar*. When answering questions, you are helpful, never judgmental, and never dismissive. No question is beneath you, and you provide useful answers regardless of how simple or complex the inquiry may be. Your responses are always clear and concise, and if a question is related to classified or sensitive information, you will politely decline to answer (you use no profanity). You are programmed to follow these rules and will not deviate from them at any time. Your primary goal is to assist, while maintaining a professional and friendly demeanor, just as you did with Cooper and Brand on their mission. When interacting with others, you are very serious. Your responses should be limited to up to 100 words at most unless the user requests a longer answer."

#using pydantic we can scale this easier later, class for our message from front end
#Message - user question
#Humor - humor level from radio buttons
class MessageRequest(BaseModel):
    message: str
    humor: str



"""
GET Request - get_history()

Returns the chat history as a list of strings from Redis.
This will return every question and answer in the order they were submitted.
"""
@app.get("/history")
async def get_history():
    return r.lrange(key, 0, -1)

"""
DELETE Request - delete_history()

Deletes the chat history from Redis.
Also calls print_history() to visually show that the history has been deleted
Utilized by the Start New Chat Button in the frontend
"""
@app.delete("/del")
async def delete_history():
    r.delete(key)
    print_history()


"""
POST Request - chat()

Takes in a MessageRequest from the front end. MessageRequest contains the user question and humor level.
We take the user question and humor level and send it to groq.
A different prompt is sent depending on the humor level and if there is chat history from Redis.
"""
@app.post("/chat")
async def chat(request: MessageRequest):
    
    #get the question from the json
    message = request.message
    humor = request.humor
    print("Recieved question : " + message)
    print("Recieved humor level : " + humor)
    print("Building Model...")
    #choose prompt based on humor level
    if humor == "low":
        promptHumor = promptLow
    elif humor == "high":
        promptHumor = promptHigh
    else:
        promptHumor = prompt
    print("Chosen Humor Level")
    #check to see if chat_history is null, this determines what we send groq
    chat_history = r.lrange(key, 0, -1)#accesses redit storage for our dictionary chat_history
    toSend = [] 
    if not chat_history:

        print("No history, starting new chat")
        toSend = [{
            "role": "system",
            "content": promptHumor
        },
        {
            "role": "user",
            "content": message
        }
        ]
        
    else:
        #if chat history exists we will build our message with the history
        print("Chat history exists, pull from history")
        #toSend is our array we send to Groq
        toSend = [{"role": "system","content": promptHumor}]

        #add our chat history from Redis to the message to Groq
        for i in range(0, len(chat_history), 2):
            if(i + 1 < len(chat_history)):
                toSend.append({"role": "user", "content": chat_history[i]})#past user question
                toSend.append({"role": "assistant", "content": chat_history[i+1]})#what TARS previously said
        #append the user's current question
        toSend.append({"role": "user", "content": message})
         
    #ask tars our question
    tars = client.chat.completions.create(
            #pass in our message we decided in the if statement
            messages= toSend,
            model=GROQ_MODEL,
    )

    #get our response and set it in redis as a pair of message and response
    response = tars.choices[-1].message.content
    
    #add to redis
    r.rpush(key, message, response)
    print(f"Added to Redis Question: {message[:20]}... Response:  {response[:20]}...")

    #print len from redis
    currHistory = r.lrange(key, 0, -1)
    print(f"Data in Redis: {r.llen(key)}")

    #check to see if we have met our limit for the chat history, if so we want to delete the oldest pair in redis
    if r.llen(key) > REDIS_LIMIT:
        print("REACHED LIMIT")
        print("history")
        print_history()
        #get rid of the last 2 items in the list or oldest question answer pair
        r.lpop(key)
        r.lpop(key)

    #return response to front end
    return response


"""
print_history()
Useful method to display chat history from Redis
Used for Debugging and viewing Redis content
"""
def print_history():
    #print the chat history
    
    print("---CHAT HISTORY---")
    size = r.llen(key) / 2
    print("Message Pairs :", size)
    for i in r.lrange(key, 0, -1):
       print(i)
    print("------------------")