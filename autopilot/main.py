import os
import sys
from crewai import Crew, Process
from src.agents import BlogAgents
from src.tasks import BlogTasks
from dotenv import load_dotenv

def main():
    # 1. Load Environment Variables
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in .env file.")
        print("Please copy .env.example to .env and add your key.")
        return

    # 2. Read Content
    post_path = os.path.join("content", "sample_post.md")
    try:
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {post_path}")
        return

    # 3. Instantiate Agents and Tasks
    agents = BlogAgents()
    tasks = BlogTasks()

    analyst = agents.analyst_agent()
    analysis_task = tasks.analyze_post_task(analyst, content)

    # 4. Create Crew
    crew = Crew(
        agents=[analyst],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True
    )

    # 5. Kickoff
    print("## Starting Datalaria Autopilot Analysis ##")
    result = crew.kickoff()
    
    print("\n\n########################")
    print("## FINAL ANALYSIS RESULT ##")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    main()
