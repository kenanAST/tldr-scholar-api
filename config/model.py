from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OpenAIGPT3LLM = ChatOpenAI(
    model="gpt-3.5-turbo",
)

OpenAIGPT4LLM = ChatOpenAI(
    model="gpt-4",
)

llm=OpenAIGPT3LLM

