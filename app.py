from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user_input = ''
    ai_response = ''
    
    if request.method == 'POST':
        user_input = request.form['user_message']  
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
    
    return render_template('chat.html', user_message=user_input, ai_response=ai_response)

if __name__ == '__main__':
    app.run(debug=True)