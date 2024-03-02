from agents import initialize_agents
from crewai import Task


def initialize_tasks(article_title: str):

    scientist_researcher, fun_educator = initialize_agents(article_title)

    gather_concepts = Task(
        description=f"""Gather the important information of a research article. Article Title: {article_title}""",
        agent=scientist_researcher,
    )

    create_engaging_education = Task(
        description=f"""Organize the important information of a research article into a fun and engaging way of understanding the concepts. Article Title: {article_title}""",
        agent=fun_educator
    )

    return gather_concepts, create_engaging_education