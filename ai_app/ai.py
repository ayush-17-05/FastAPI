from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.schema import HumanMessage, AIMessage
from langchain_classic.chains import ConversationChain
from dotenv import load_dotenv
import os
from todo_app.database import conversation_collection

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

async def load_memory(user_email:str, conversation_collection):
    """Load past messages from mongodb into memory."""
    memory = ConversationBufferMemory()
    doc = await conversation_collection.find_one({"user_email":user_email})

    if doc and "messages" in doc:
        for msg in doc["messages"]:
            if msg["role"] == "user":
                memory.chat_memory.add_message(HumanMessage(content=msg["content"]))
            else:
                memory.chat_memory.add_message(AIMessage(content=msg["content"]))
    
    return memory

async def save_message(user_email:str, role: str, content: str, conversation_collection):
    """Save a single message to mongodb."""
    await conversation_collection.update_one(
        {"user_email":user_email},
        {"$push":{"messages":{"role":role,"content":content}}},
        upsert=True
    )

async def ask_ai(prompt: str, user_email: str, conversation_collection) -> str:
    memory = await load_memory(user_email, conversation_collection)
    conversation = ConversationChain(llm=llm, memory=memory)

    response=conversation.predict(input=prompt)

    await save_message(user_email,"user",prompt,conversation_collection)
    await save_message(user_email,"ai",response,conversation_collection)

    return response