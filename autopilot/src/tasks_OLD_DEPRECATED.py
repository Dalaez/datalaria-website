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

    def twitter_task_es(self, agent, context_from_analyst):
        return Task(
            description=dedent("""\
                Escribe un hilo viral de Twitter en ESPAÑOL basado en el análisis proporcionado.
                Enfócate en los 'marketing_hooks' y 'key_takeaways'.
                El hilo debe ser impactante, máximo 5 tweets.
                Separados por '---'.
                LANGUAGE: SPANISH
            """),
            expected_output="Una cadena de texto con el hilo en Español, separado por '---'.",
            agent=agent,
            context=[context_from_analyst]
        )

    def twitter_task_en(self, agent, context_from_analyst):
        return Task(
            description=dedent("""\
                Write a viral Twitter thread in ENGLISH based on the analysis provided.
                Focus on the 'marketing_hooks' and 'key_takeaways'.
                The thread should be punchy, max 5 tweets.
                Separated by '---'.
                LANGUAGE: ENGLISH
            """),
            expected_output="A raw string containing the thread in English, separated by '---'.",
            agent=agent,
            context=[context_from_analyst]
        )

    def linkedin_task_es(self, agent, context_from_analyst):
        return Task(
            description=dedent("""\
                Escribe un post profesional para LinkedIn en ESPAÑOL basado en el análisis.
                Enfócate en el valor de negocio y el 'target_audience'.
                Usa un gancho fuerte al principio.
                LANGUAGE: SPANISH
            """),
            expected_output="Texto formateado en Markdown para LinkedIn en Español.",
            agent=agent,
            context=[context_from_analyst]
        )

    def linkedin_task_en(self, agent, context_from_analyst):
        return Task(
            description=dedent("""\
                Write a professional LinkedIn post in ENGLISH based on the analysis provided.
                Focus on business value and 'target_audience'.
                Use a strong hook at the beginning.
                LANGUAGE: ENGLISH
            """),
            expected_output="A markdown formatted text for LinkedIn in English.",
            agent=agent,
            context=[context_from_analyst]
        )
