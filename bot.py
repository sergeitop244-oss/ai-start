
import os 
import asyncio
from dotenv import load_dotenv
from groq import Groq 
from aiogram import Bot, Dispatcher,types
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
# === RAG: загрузка документа ===
loader = TextLoader("docs/info.txt", encoding="utf-8")
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
vectorstore = FAISS.from_documents(chunks, embeddings)

rag_prompt = ChatPromptTemplate.from_template("""
Ты — ассистент, который отвечает на вопросы, используя ТОЛЬКО информацию из документа ниже.
Если в документе нет ответа — честно скажи: "В документе нет ответа на этот вопрос".

Документ:
{context}

Вопрос: {question}

Ответ:
""")

rag_llm = ChatGroq(model="openai/gpt-oss-120b",api_key=os.getenv("GROQ_API_KEY")) 
rag_chain = rag_prompt | rag_llm

groq_client =Groq(api_key=os.getenv("GROQ_API_KEY"))
bot =Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

# история деологов для каждого пользователя 
histories = {}

@dp.message()
async def handle_message(message:types.Message):
    question = message.text

    docs = vectorstore.similarity_search(question,k=3)
    context ="\n\n".join(doc.page_content for doc in docs)

    answer = rag_chain.invoke({"context": context,"question": question})
    await message.answer(answer.content)

async def start_bot():
        print("Бот запущен...")
        await dp.start_polling(bot)

asyncio.run(start_bot())
