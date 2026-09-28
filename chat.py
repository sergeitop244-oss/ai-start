import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client =Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = []

print("Чат с ИИ запущен. Напиши 'выход' для завершения.\n")

while True:
    user_input = input("Ты: ")
    if user_input.lower() =="выход":
        print("Пока!")
        break

    messages.append({"role": "user" , "content": user_input})

    response =client.chat.completions.create(model="openai/gpt-oss-120b" ,messages=messages)

    answer =response.choices[0].message.content
    print(f"ИИ: {answer}\n")

    messages.append( {"role" :"assistant", "content": answer})


