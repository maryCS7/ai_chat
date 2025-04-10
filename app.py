from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

user_input = input("You: ")

# Send user input to OpenAI and get response
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": user_input}
    ],
    max_tokens=150,   
    temperature=0.7
)

print("AI:", response.choices[0].message.content)