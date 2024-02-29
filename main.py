from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Crew, Process
import os
from textwrap import dedent
from agents import scientist_researcher, fun_educator
from tasks import gather_concepts, create_engaging_education
import requests
import json

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

class ScrapeResponse(BaseModel):
    result: dict

class SearchResponse(BaseModel):
    result: dict

def run_crew(doi):

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
