import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

# 1. Загружаем ключ
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 2. Загружаем документ
loader = TextLoader("docs/info.txt", encoding="utf-8")
documents = loader.load()

# 3. Разбиваем на куски
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print(f"Разбито на куски: {len(chunks)}")

# 4. Превращаем в векторы
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# 5. Сохраняем в векторную базу
vectorstore = FAISS.from_documents(chunks, embeddings)

# 6. Настраиваем нейросеть
llm = ChatGroq(model="openai/gpt-oss-120b", api_key=api_key)

# 7. Промпт: отвечай только по документу
prompt = ChatPromptTemplate.from_template("""
Ты — ассистент, который отвечает на вопросы, используя ТОЛЬКО информацию из документа ниже.
Если в документе нет ответа — честно скажи: "В документе нет ответа на этот вопрос".

Документ:
{context}

Вопрос: {question}

Ответ:
""")

# 8. Цикл диалога
print("RAG-система запущена. Напиши 'выход' для завершения.\n")

while True:
    question = input("Ты: ")
    if question.lower() == "выход":
        break

    # Ищем 3 самых похожих куска в документе
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)

    # Отправляем в нейросеть
    chain = prompt | llm
    answer = chain.invoke({"context": context, "question": question})

    print(f"ИИ: {answer.content}\n")