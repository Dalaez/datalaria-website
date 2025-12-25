from crewai import Task
from textwrap import dedent

class BlogTasks:
    def analyze_post_task(self, agent, content):
        return Task(
            description=dedent(f"""\
                Analyze the following blog post content from a technical and marketing perspective.
                
                CONTENT:
                ----------
                {content}
                ----------
                
                Your analysis must be thorough. Identify the target audience, the specific technologies mentioned,
                and the key takeaways. Also, create catchy marketing hooks to promote this post.
            """),
            expected_output=dedent("""\
                A valid JSON object containing the following keys:
                - "summary": "A concise summary of the post (max 2 sentences)",
                - "target_audience": "Who is this for?",
                - "tech_stack": ["List", "of", "technologies"],
                - "key_takeaways": ["List", "of", "3", "key", "points"],
                - "marketing_hooks": ["List", "of", "3", "tweet-style", "hooks"]
            """),
            agent=agent
        )
