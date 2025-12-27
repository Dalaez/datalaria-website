import os
import sys
import io
from crewai import Crew, Process
from src.agents import BlogAgents
from src.tasks import BlogTasks
from dotenv import load_dotenv

# Fix for Windows Unicode errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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

    # Agents
    analyst = agents.analyst_agent()
    twitter_writer = agents.twitter_writer_agent()
    linkedin_writer = agents.linkedin_writer_agent()

    # Tasks
    analysis_task = tasks.analyze_post_task(analyst, content)
    
    # Multilingual Tasks
    twitter_es = tasks.twitter_task_es(twitter_writer, analysis_task)
    twitter_en = tasks.twitter_task_en(twitter_writer, analysis_task)
    linkedin_es = tasks.linkedin_task_es(linkedin_writer, analysis_task)
    linkedin_en = tasks.linkedin_task_en(linkedin_writer, analysis_task)

    # 4. Create Crew
    # The tasks provided here determine the execution order (Process.sequential is default)
    crew = Crew(
        agents=[analyst, twitter_writer, linkedin_writer],
        tasks=[analysis_task, twitter_es, twitter_en, linkedin_es, linkedin_en],
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

    print("\n\n########################")
    print("## TWITTER (ES) ##")
    print("########################\n")
    print(twitter_es.output.raw if twitter_es.output else "No output")

    print("\n\n########################")
    print("## TWITTER (EN) ##")
    print("########################\n")
    print(twitter_en.output.raw if twitter_en.output else "No output")

    print("\n\n########################")
    print("## LINKEDIN (ES) ##")
    print("########################\n")
    print(linkedin_es.output.raw if linkedin_es.output else "No output")

    print("\n\n########################")
    print("## LINKEDIN (EN) ##")
    print("########################\n")
    print(linkedin_en.output.raw if linkedin_en.output else "No output")

if __name__ == "__main__":
    main()
