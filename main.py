from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from textwrap import dedent
from tools.read_pdf import ScraperTool
import requests
import json

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

class ScrapeResponse(BaseModel):
    result: dict

class SearchResponse(BaseModel):
    result: dict

load_dotenv()


read_pdf = ScraperTool.scrape

OpenAIGPT3LLM = ChatOpenAI(
    model="gpt-3.5-turbo",
)


def run_crew(doi):

    scientist_researcher = Agent(
        role='Senior Scientist Researcher',
        goal='Gather the important information of a research article',
        backstory="""You are a scientist with a wide experience in research. You have been tasked with gathering the important information of a research article. You have been given the DOI of the article.""",
        verbose=True,
        allow_delegation=False,
        tools=[read_pdf],
        llm=OpenAIGPT3LLM
    )

    fun_educator = Agent(
        role='Fun Educator',
        goal='You will organize the important information of a research article into a fun and engaging way of understanding the concepts.',
        backstory="""You are an entertaining educator that can take complex information and make it fun and engaging for the general audience. You have been tasked with organizing the important information of a research article into a fun and engaging way of understanding the concepts.""",
        verbose=True,
        allow_delegation=False,
        llm=OpenAIGPT3LLM
    )

    gather_concepts = Task(
        description=f"""Gather the important information of a research article""",
        agent=scientist_researcher,
    )

    create_engaging_education = Task(
        description=f"""Organize the important information of a research article into a fun and engaging way of understanding the concepts.""",
        agent=fun_educator
    )


    crew = Crew(
        agents=[scientist_researcher, fun_educator],
        tasks=[gather_concepts, create_engaging_education],
        verbose=2, # You can set it to 1 or 2 to different logging levels
        process=Process.sequential
    )

    result = crew.kickoff()
    return result


@app.post("/learn/", response_model=ScrapeResponse)
async def scrape_website(request: ScrapeRequest):
    global url
    doi = dedent(request.doi)
    print("DOI", doi)
    raw_data = run_crew(doi)
    result = json.loads(raw_data)
    return {"result": result}

@app.get("/search", response_model=SearchResponse)
async def search(q: str):
    url = "https://google.serper.dev/scholar"
    payload = json.dumps({
        "q": q
    })
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("RESPONSE", response.text)
    return {"result": json.loads(response.text)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
