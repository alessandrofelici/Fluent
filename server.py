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


groq_api_key = os.getenv("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")
model = "llama-3.3-70b-versatile"



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



userScore = 0
quizState = None


# def generateQuizQuestion(language):
#     # prompt = f"""
#     # The user is learning {language}. Generate a **new** multiple-choice quiz question 
#     # that has not been asked before in this session. The question should be about 
#     # vocabulary, grammar, or sentence structure. Provide four options (A, B, C, D).

#     # If the user has answered a similar question before, **avoid repeating it**.
#     # """

#     prompt = f"""
#     The user is learning {language}. Generate a **language-specific** multiple-choice quiz question for a beginner in {language}. 
#     The question should be related to **vocabulary, grammar, or sentence construction** in {language}, and provide four options (A, B, C, D).
#     Ensure the question is specific to {language} and not a generic language question.

#     If the user has answered a similar question before, **avoid repeating it**.
#     """



def generateQuizQuestion(language):
    # prompt = f"Generate a random multiple-choice quiz question for someone learning {language}. The question should be related to vocabulary, grammar, or sentence construction, and provide four options (A, B, C, D)."

    prompt = f"""
    The user is learning {language}. Generate a **language-specific** multiple-choice quiz question for a beginner in {language}. 
    The question should be related to **vocabulary, grammar, or sentence construction** in {language}, and provide four options (A, B, C, D).
    Ensure the question is specific to {language} and not a generic language question.

    If the user has answered a similar question before, **avoid repeating it**.
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
        question = chat_completion.choices[0].message.content
        return question.strip()
    except Exception as e:
        return f"Sorry, I encountered an error generating the question: {str(e)}"


# def checkAnswer(language, question, user_answer):
#     prompt = f"""The user is learning {language}. The question was: '{question}'.
#     The user selected answer: '{user_answer}'. Please:
    
#     1. Clearly state whether the answer is CORRECT or INCORRECT.
#     2. If correct, explain WHY it is the correct answer.
#     3. If incorrect, state what the correct answer is and provide a short explanation of why it is correct.
#     4. Keep the explanation simple but educational for a beginner learning {language}."""

#     try:
#         chat_completion = client.chat.completions.create(
#             messages=[{
#                 "role": "system",
#                 "content": "You are a language learning assistant."
#             }, {
#                 "role": "user",
#                 "content": prompt
#             }],
#             model=model, 
#         )
#         feedback = chat_completion.choices[0].message.content
#         return feedback.strip()
#     except Exception as e:
#         return f"Sorry, I encountered an error evaluating the answer: {str(e)}"

def updateScore(points):
    global userScore
    userScore += points


def checkAnswer(language, question, user_answer):
    prompt = f"""
    The user is learning {language}. The question was: '{question}'.
    The user selected answer: '{user_answer}'.

    1. Clearly state whether the answer is **CORRECT** or **INCORRECT**.
    2. If correct, explain **why** it is the correct answer.
    3. If incorrect, state **the correct answer** and provide a short **educational** explanation.
    4. Ensure the response is **beginner-friendly** and provides learning reinforcement.
    """
    
    try:
        feedback = conversation.predict(human_input=prompt)
        return feedback.strip()
    except Exception as e:
        return f"Sorry, I encountered an error evaluating the answer: {str(e)}"


def updateScore(points):
    global userScore
    userScore += points

@app.route("/quiz", methods=["POST"])
def quiz():
    language = request.json.get("language")
    
    
    question = generateQuizQuestion(language)
    
    
    global quizState
    quizState = {"language": language, "question": question}
    
    return jsonify({"question": question})


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

    
    feedback = checkAnswer(language, question, user_answer)

    
    if "correct" in feedback.lower():
        updateScore(10)  
        quizState = None 
        return jsonify({"result": f"Correct! {feedback}", "score": userScore})
    else:
        updateScore(-5) 
        quizState = None 
        return jsonify({"result": f"Incorrect. {feedback}", "score": userScore})

if __name__ == "__main__":
    app.run(port=5000, debug=True)