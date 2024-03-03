from agents import initialize_agents
from crewai import Task


def initialize_tasks(article_title: str):

    scientist_researcher, writer = initialize_agents(article_title)

    gather_concepts = Task(
        description=f"""Gather important information of a research article. Article Title: {article_title}""",
        expected_output=
        """
        1. Title: The title of the research article should be concise yet descriptive.
        2. Abstract: A brief summary of the entire research article, including the research question, methods, results, and conclusions.
        3. Introduction: Background information on the topic, research problem/question, and significance of the study.
        4. Literature Review: Review of existing literature relevant to the topic, identifying gaps in knowledge.
        5. Methods: Details on how the research was conducted, including participants, materials, procedures, and data analysis techniques.
        6. Results: Presentation of the study's findings using tables, figures, and statistical analyses.
        7. Discussion: Interpretation of results in the context of the research question and existing literature, discussing implications, limitations, and future research directions.
        8. Conclusion: Summary of the main findings and significance of the study.
        9. References: List of all sources cited within the article.
        """,
        agent=scientist_researcher,
    )


    write_engaging_summary = Task(
        description=f"""Organize the important information of a research article into a fun and engaging way of understanding the concepts. Give me a JSON of this. The JSON key is summary and the value is the a multiline summary of the article.""",
        agent=writer
    )

    return gather_concepts, write_engaging_summary