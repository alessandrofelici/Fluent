from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from groq import Groq

app = Flask(__name__)
CORS(app)

# Load API key from environment variable
groq_api_key = os.getenv("GROQ_API_KEY")
groq_api_key = "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"
model = 'llama-3.3-70b-versatile'

userScore = 0
quizState = None

groq_chat = ChatGroq(
    groq_api_key="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", 
    model_name="llama-3.3-70b-versatile"
)

#remembers last 5 interactions
conversational_memory_length = 5  
memory = ConversationBufferWindowMemory(
    k=conversational_memory_length, 
    memory_key="chat_history", 
    return_messages=True
)

# defines prompt template
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{human_input}")
])


conversation = LLMChain(
    llm=groq_chat,
    prompt=prompt,
    verbose=False,
    memory=memory
)


client = Groq(api_key=groq_api_key)

def generateQuizQuestion(language):
    prompt = f"""
    Generate a random multiple-choice quiz question for someone learning {language}. 
    The question should be related to vocabulary, grammar, or sentence construction. 
    Provide four options (A, B, C, D) and specify the correct answer.

    **Output Format:**
    Question: [Your question here]
    A. [Option A]
    B. [Option B]
    C. [Option C]
    D. [Option D]
    Correct Answer: [Correct option letter]
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "You are a language learning assistant."
            }, {
                "role": "user",
                "content": prompt
            }],
            model="llama-3.3-70b-versatile", 
        )
        response = chat_completion.choices[0].message.content
        lines = response.split('\n')
        question = lines[0].replace("Question: ", "").strip()
        options = [line.split('. ', 1)[1].strip() for line in lines[1:5]]
        correct_answer = lines[5].replace("Correct Answer: ", "").strip()
        return {
            "question": question,
            "options": options,
            "correctAnswer": correct_answer
        }
    except Exception as e:
        return f"Sorry, I encountered an error generating the question: {str(e)}"

def checkAnswer(language, question, user_answer):
    prompt = f"""The user is learning {language}. The question was: '{question}'.
    The user selected answer: '{user_answer}'. Please:
    
    1. Clearly state whether the answer is CORRECT or INCORRECT.
    2. If correct, explain WHY it is the correct answer.
    3. If incorrect, state what the correct answer is and provide a short explanation of why it is correct.
    4. Keep the explanation simple but educational for a beginner learning {language}."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "You are a language learning assistant."
            }, {
                "role": "user",
                "content": prompt
            }],
            model=model, 
        )
        feedback = chat_completion.choices[0].message.content
        return feedback.strip()
    except Exception as e:
        return f"Sorry, I encountered an error evaluating the answer: {str(e)}"

def updateScore(points):
    global userScore
    userScore += points

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    language = request.json.get("language")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    if not language:
        return jsonify({"error": "Language is required"}), 400
    system_prompt = f"""
    You are a friendly and helpful language learning assistant. Your goal is to help users practice and improve their skills in {language}. 
    When the user starts a conversation, you will respond in {language}. 
    You will also provide explanations, corrections, and examples in English if needed to help the user understand.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}")
    ])

    conversation.prompt = prompt

    bot_response = conversation.predict(human_input=user_input)

    return jsonify({"reply": bot_response})

@app.route("/quiz", methods=["POST"])
def quiz():
    language = request.json.get("language")
    
    if not language:
        return jsonify({"error": "Language is required."}), 400
    
    question_data = generateQuizQuestion(language)

    if "error" in question_data:
        return jsonify({"error": question_data["error"]}), 500
    
    global quizState
    quizState = {"language": language, "question": question_data["question"], "options": question_data["options"], "correctAnswer": question_data["correctAnswer"]}

    return jsonify(question_data)

@app.route("/quiz/check", methods=["POST"])
def check_answer():
    global quizState

    if quizState is None:
        return jsonify({"error": "No active quiz question. Start a quiz first."}), 400

    user_answer = request.json.get("userAnswer")  # wants just A,B,C,D

    if not user_answer or user_answer not in ["A", "B", "C", "D"]:
        return jsonify({"error": "Invalid answer format. Please select A, B, C, or D."}), 400

    language = quizState["language"]
    question = quizState["question"]
    correct_answer = quizState["correctAnswer"]
    
    feedback = checkAnswer(language, question, user_answer)

    
    if user_answer in correct_answer:
        updateScore(10)  
        quizState = None 
        return jsonify({"result": f"Correct! {feedback}", "score": userScore})
    else:
        updateScore(-5) 
        quizState = None 
        return jsonify({"result": f"Incorrect. {feedback}", "score": userScore})

if __name__ == "__main__":
    app.run(port=5000, debug=True)