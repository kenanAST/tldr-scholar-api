from agents import scientist_researcher, fun_educator
from crewai import Task


gather_concepts = Task(
    description=f"""Gather the important information of a research article""",
    agent=scientist_researcher,
)

create_engaging_education = Task(
    description=f"""Organize the important information of a research article into a fun and engaging way of understanding the concepts.""",
    agent=fun_educator
)