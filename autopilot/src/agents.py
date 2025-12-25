import os
from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

class BlogAgents:
    def __init__(self):
        # Using CrewAI's LLM wrapper which handles provider switching via LiteLLM.
        # Format: provider/model_name
        self.llm = LLM(
            model="gemini/gemini-3-flash-preview",
            api_key=os.getenv("GOOGLE_API_KEY")
        )

    def analyst_agent(self):
        return Agent(
            role='Senior Tech Editor & Data Analyst',
            goal='Analyze raw content to extract structured insights and marketing hooks',
            backstory=(
                "You are a veteran tech editor with a sharp eye for detail. "
                "You read code and prose with precision. "
                "You don't write fluff, you extract facts, identify the core tech stack, "
                "and pinpoint exactly who needs to read this."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
