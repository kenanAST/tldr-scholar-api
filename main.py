from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Crew, Process
import os
from textwrap import dedent
from agents import initialize_agents
from tasks import initialize_tasks
import requests
import json

app = FastAPI()


def run_crew(article_title: str):

    gather_concepts, create_engaging_education = initialize_tasks(article_title)
    scientist_researcher, fun_educator = initialize_agents(article_title)

    crew = Crew(
        agents=[scientist_researcher, fun_educator],
        tasks=[gather_concepts, create_engaging_education],
        verbose=2, # You can set it to 1 or 2 to different logging levels
        process=Process.sequential
    )

    result = crew.kickoff()
    return result


@app.post("/summarize", response_model=dict)
async def summarize_article(article_title: str):
    print("Article Title", article_title)
    raw_data = run_crew(article_title)
    print("RawzData", raw_data)
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
    print("RESPONSE", response.text)
    return {"result": json.loads(response.text)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
