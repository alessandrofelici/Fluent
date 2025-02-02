from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

app = Flask(__name__)
CORS(app)

# Load API key from environment variable
groq_api_key = os.getenv("GROQ_API_KEY")
model = 'llama-3.3-70b-versatile'


groq_api_key = "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"
# Initialize Groq Chat
groq_chat = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name=model
)

# Set up conversational memory
conversational_memory_length = 5  # Number of messages to remember
memory = ConversationBufferWindowMemory(
    k=conversational_memory_length, 
    memory_key="chat_history", 
    return_messages=True
)

# Define Prompt Template
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{human_input}")
])

# Initialize LangChain Conversation
conversation = LLMChain(
    llm=groq_chat,
    prompt=prompt,
    verbose=False,
    memory=memory
)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    bot_response = conversation.predict(human_input=user_input)  # Pass correct input
    return jsonify({"reply": bot_response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
