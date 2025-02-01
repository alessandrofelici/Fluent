import os

from groq import Groq

client = Groq(api_key = "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")


print("Whats up? enter to leave\n")
request = input()
while(request != ""):

    chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": "you are a helpful assistant is kind and professional. You will help users, specifically by teaching them a spoken langauge. You may help them in other ways but your primary goal is to teach langauge."
            },
            {
                "role": "user",
                "content": request,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    print(chat_completion.choices[0].message.content)
    print("\nThats all. Anything else? enter to leave\n")
    request = input()
print("See ya later")