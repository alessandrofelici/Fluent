from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

client = Groq(api_key = "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")


userScore = 0
quizState = None


def generateQuizQuestion(language):
    prompt = f"Generate a random multiple-choice quiz question for someone learning {language}. The question should be related to vocabulary, grammar, or sentence construction, and provide four options (A, B, C, D). Clearly specify which option is correct."

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
            model="llama-3.3-70b-versatile", 
        )
        feedback = chat_completion.choices[0].message.content
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
