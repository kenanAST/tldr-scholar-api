from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Crew, Process
import os
from agents import initialize_agents
from tasks import initialize_tasks
from tools.search_pdf import FetchPDFTool
import requests
import json

app = FastAPI()


read_pdf = FetchPDFTool.read_pdf

def run_crew(article_title: str):

    gather_concepts, write_engaging_summary = initialize_tasks(article_title)
    scientist_researcher, writer = initialize_agents(article_title)

    crew = Crew(
        agents=[scientist_researcher, writer],
        tasks=[gather_concepts, write_engaging_summary],
        verbose=2, # You can set it to 1 or 2 to different logging levels
        process=Process.sequential
    )

    result = crew.kickoff()
    return result

@app.get("/summarize", response_model=dict)
async def summarize_article(article_title: str):
    raw_data = run_crew(article_title)
    print("Type: ",type(raw_data))
    result = json.loads(raw_data)
    return {"result": result}

@app.get("/search", response_model=dict)
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
    return {"result": json.loads(response.text)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
