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

    def twitter_writer_agent(self):
        return Agent(
            role='Tech Twitter Influencer',
            goal='Convert structured insights into a viral Twitter thread (max 5 tweets)',
            backstory=(
                "You are a tech influencer who hates corporate jargon. "
                "You write in a punchy, provocative style. "
                "You use lowercase often for aesthetic. "
                "You focus on the 'Marketing Hooks' from the input. "
                "You NEVER use hashtags like #Technology, only niche ones."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def linkedin_writer_agent(self):
        return Agent(
            role='LinkedIn Thought Leader',
            goal='Write a high-engagement LinkedIn post based on the analysis',
            backstory=(
                "You are a respected Voice in the Tech industry. "
                "You write with empathy and professionalism. "
                "You use the 'Broetry' style (short paragraphs, lots of whitespace). "
                "You focus on the 'Key Takeaways' and business value. "
                "You start with a strong hook."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
