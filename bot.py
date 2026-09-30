print("TEST: файл запустился")
import os 
import asyncio
from dotenv import load_dotenv
from groq import Groq 
from aiogram import Bot, Dispatcher,types

load_dotenv()

groq_client =Groq(api_key=os.getenv("GROQ_API_KEY"))
bot =Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

# история деологов для каждого пользователя 
histories = {}

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if user_id not in histories:
        histories[user_id] = []
    histories[user_id].append({"role":"user", "content":text})

    response = groq_client.chat.completions.create(model="openai/gpt-oss-120b",messages=histories[user_id])

    answer = response.choices[0].message.content 
    histories[user_id].append({"role":"assistant", "content": answer})

    await message.answer(answer)

async def start_bot():
        print("Бот запущен...")
        await dp.start_polling(bot)

asyncio.run(start_bot())
