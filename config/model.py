from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

OpenAIGPT3LLM = ChatOpenAI(
    model="gpt-3.5-turbo",
)

OpenAIGPT4LLM = ChatOpenAI(
    model="gpt-4",
)

DolphinMistal = Ollama(
    model='dolphin-mistral',
)

Mistal = Ollama(
    model='mistral',
)

llm=Mistal

