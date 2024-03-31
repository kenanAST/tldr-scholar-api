from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Crew, Process
import os
from agents import initialize_agents
from tasks import initialize_tasks
from tools.search_pdf import FetchPDFTool
import requests
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


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
    result = run_crew(article_title)
    result = result.replace("Final Answer:", "")
    result = result.replace("```","")
    print("Type: ", type(result))
    print("Datazsk:", result)
    dict_result = json.loads(result)
    return dict_result

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
