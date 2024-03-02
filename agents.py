from crewai import Agent
from config.model import OpenAIGPT3LLM
from tools.search_pdf import FetchPDFTool

read_pdf = FetchPDFTool.read_pdf

def initialize_agents(article_title: str):
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

    return scientist_researcher, fun_educator


