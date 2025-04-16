from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# OLD: direct OpenAI call 
# response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "user", "content": user_input}
#     ],
#     max_tokens=150,
#     temperature=0.7
# )
# ai_response = response.choices[0].message.content


# NEW: LangChain setup
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

basic_prompt = PromptTemplate(
    input_variables=["user_question"],
    template="Answer the following question as clearly as possible:\n\n{user_question}"
)

# LLM and prompt template into a chain - reusable and flexible
chat_chain = LLMChain(llm=llm, prompt=basic_prompt)

@app.route('/')
def home():
    return render_template('home.html')

def detect_intent(user_message):
    resource_keywords = ["guide", "tips", "recommend", "resource", "article", "tools"]
    if any(keyword in user_message.lower() for keyword in resource_keywords):
        return "resource"
    else:
        return "chat"

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user_input = ''
    ai_response = ''
    resources = []

    if request.method == 'POST':
        user_input = request.form['user_message']

        if detect_intent(user_input) == "resource":
            # resources = search_google(user_input)  # ToDo
            titles = ', '.join([res['title'] for res in resources])
            ai_response = f"I found some helpful resources for you: {titles}. Want to explore one?"
        else:
            # NEW: LangChain chat_chain to generate response vs OpenAI directly
            ai_response = chat_chain.run(user_question=user_input)

    return render_template('chat.html', user_message=user_input, ai_response=ai_response, resources=resources)