import os
from langchain_core.tools import tool
from langchain_classic.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(
    model = "llama3.2"
    # google_api_key = os.getenv("GEMINI_API_KEY")
)

@tool
def summarize_text(text:str)->str:
    """Summarize a given text into 2 sentences.
    Use this when you need to shorten or condense text."""
    response = llm.invoke(f"Summarize this in 2 sentences:\n\n{text}")
    return response.content

@tool
def translate_to_hindi(text:str)->str:
    """Translates English text to Hindi.
    Use this when you need to translate english content to hindi."""
    response = llm.invoke(f"Translate to hindi. Return only translation, nothing else:\n\n{text}")
    return response.content

@tool
def word_counter(text:str)->str:
    """Count the number of words in a text.
    Use this when you want to know how many words are in a text."""
    count = len(text.split())
    return f"The text contains {count} words."

tools = [summarize_text, translate_to_hindi, word_counter]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations = 5,
    handle_parsing_errors=True,
    agent_kwargs={
        "prefix": """You are a helpful assistant. Complete ALL requested tasks in order.
Once you have an observation, move to the NEXT task. Never repeat a tool you already used.
Always finish by translating if translation was requested."""
    }
)

def run_agent(query:str)->str:
    return agent.invoke({"input":query})["output"]