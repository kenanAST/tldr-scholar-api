from crewai import Agent
from config.model import llm
from tools.search_pdf import FetchPDFTool

read_pdf = FetchPDFTool.read_pdf

def initialize_agents(article_title: str):
    scientist_researcher = Agent(
        role='Senior Scientist Researcher',
        goal='Gather the important information of a research article',
        backstory=f"""You are a scientist with a wide experience in research. You have been tasked with gathering the important information of a research article. Article title: {article_title}""",
        verbose=True,
        allow_delegation=False,
        tools=[read_pdf],
        llm=llm
    )

    writer = Agent(
        role='Research Paper Writer',
        goal='You will organize the important information of a research article into a fun and engaging way of understanding the concepts. Give me a JSON of this. The JSON key is summary and the value is the a multiline summary of the article.',
        backstory="""You are an entertaining educator that can take complex information and make it fun and engaging for the general audience. You have been tasked with organizing the important information of a research article into a fun and engaging way of understanding the concepts.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    return scientist_researcher, writer


