from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

app = Flask(__name__)
CORS(app)

groq_api_key = os.getenv("Ggsk_X0JFRaZIWpLoFF2eLNxUWGdyb3FYC7NxqY9nnhPQdJVlDqS5ePxN")
model = "llama-3.3-70b-versatile"

groq_chat = ChatGroq(
    groq_api_key="Ggsk_X0JFRaZIWpLoFF2eLNxUWGdyb3FYC7NxqY9nnhPQdJVlDqS5ePxN", 
    model_name="llama-3.3-70b-versatile"
)

conversational_memory_length = 5  
memory = ConversationBufferWindowMemory(
    k=conversational_memory_length, 
    memory_key="chat_history", 
    return_messages=True
)

prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template("{human_input}")
])

conversation = LLMChain(
    llm=groq_chat,
    prompt=prompt,
    verbose=False,
    memory=memory
)

flashcard_data = {}

def generateWordsInLanguage(language, num_words):
    prompt = f"""
    The user is learning {language}. Generate {num_words} common words in {language}.
    For each word, provide the English translation and return the list in this format:
    Word (Translation)
    """

    try:
        words = conversation.predict(human_input=prompt)
        words_list = []
        for line in words.split("\n"):
            if "(" in line and ")" in line:
                word, translation = line.split("(")
                translation = translation.replace(")", "").strip()
                words_list.append({"word": word.strip(), "translation": translation})
        
        return words_list
    except Exception as e:
        return f"Sorry, I encountered an error generating the words: {str(e)}"

@app.route("/flashcards", methods=["POST"])
def flashcards():
    language = request.json.get("language")
    num_words = request.json.get("num_words")
    
    if not language or not num_words:
        return jsonify({"error": "Language and number of words are required."}), 400
    
    words = generateWordsInLanguage(language, num_words)
    
    if isinstance(words, list):
        flashcard_data[language] = words
        return jsonify({"flashcards": words})
    else:
        return jsonify({"error": words}), 400

@app.route("/flashcards/translate", methods=["POST"])
def translate_word():
    language = request.json.get("language")
    word = request.json.get("word")

    if language not in flashcard_data:
        return jsonify({"error": "No flashcards generated for this language."}), 400
    
    words = flashcard_data[language]
    for entry in words:
        if entry["word"].lower() == word.lower():
            return jsonify({"translation": entry["translation"]})
    
    return jsonify({"error": "Word not found."}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
