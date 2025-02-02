from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

import os

from groq import Groq

userScore = 0
quizState = None

quizData = {
    "spanish": [
        {"question": "How do you say 'Hello' in Spanish?", "answer": "Hola"},
        {"question": "How do you say 'Thank you' in Spanish?", "answer": "Gracias"},
        {"question": "How do you say 'Goodbye' in Spanish?", "answer": "Adiós"},
    ],
    "french": [
        {"question": "How do you say 'Hello' in French?", "answer": "Bonjour"},
        {"question": "How do you say 'Thank you' in French?", "answer": "Merci"},
        {"question": "How do you say 'Goodbye' in French?", "answer": "Au revoir"},
    ]
}

# start the quiz by setting the current question for the user
def startQuiz(language):
    global quizState
    if language not in quizData:
        return "Language not supported for quiz."
    
    quizState = {"language": language, "question_index": 0}
    return quizData[language][0]["question"]

# updates user's score
def updateUserScore(points):
    global userScore 
    userScore += points


# validate the answer and give feedback
def checkAnswer(user_answer):

    global quizState, userScore

    if quizState is None:
        return "Please start the quiz first by typing 'quiz'."

    language = quizState["language"]
    question_index = quizState["question_index"]
    question_data = quizData[language][question_index]

    correct_answer = question_data["answer"]
    if user_answer.lower() == correct_answer.lower():
        updateUserScore(10) 
        feedback = f"Correct! The answer is '{correct_answer}'."
    else:
        feedback = f"Incorrect. The correct answer was '{correct_answer}'."

    # Move to the next question or end the quiz
    quizState["question_index"] += 1
    if quizState["question_index"] < len(quizData[language]):
        next_question = quizData[language][quizState["question_index"]]["question"]
        feedback += f" Next question: {next_question}"
    else:
        feedback += " You've completed the quiz!"
        quizState = None  # Reset quiz state

    return feedback



def chatbotResponse(userInput, userId):

    client = Groq(api_key = "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")
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant that specializes in language learning."
            }, {
                "role": "user",
                "content": userInput,
            }],
            model="llama-3.3-70b-versatile", 
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"
        


@app.route("/chat", methods=["POST"])
def chat():
    userInput = request.json.get("message")
    language = request.json.get("language", "spanish")  # default to Spanish if no language provided


    if not userInput or not isinstance(userInput, str): # checks for if user didn't put enter anything
        return jsonify({"error": "Invalid input"}), 400
    
    
    # if user starts a quiz
    if userInput.lower() == "quiz":
        question = startQuiz(language)
        return jsonify({"response": question})

    # if user is answering a quiz question
    if userInput.lower().startswith("answer:"):
        answer = userInput[7:].strip()  # Extract the answer
        feedback = checkAnswer(answer)
        return jsonify({"response": feedback, "score": userScore})

    # if user is chatting normally
    bot_response = chatbotResponse(userInput)
    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    # app.run(host="0.0.0.0", port=5000, debug=True)
