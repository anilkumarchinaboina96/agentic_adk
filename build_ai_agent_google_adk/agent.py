import os

from dotenv import load_dotenv
from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.apps import App
from google.adk.tools.exit_loop_tool import exit_loop

load_dotenv()

MODEL = os.getenv("MODEL", "gemini-3.6-flash")

planner = Agent(
   name="Planner",
   model=MODEL,
   description="Creates a content plan from the user's topic.",
   instruction="""
Create a Markdown content plan for the user's topic.
Include a title, introduction, 4-6 main sections with useful bullets, and a
conclusion. Store only the plan in the `blog_outline` state key.
""",
   output_key="blog_outline",
)

writer = Agent(
   name="Writer",
   model=MODEL,
   description="Writes an article from the content plan.",
   instruction="""
Write a complete Markdown article from `{blog_outline}`.
Follow the plan, explain both how and why, and include concise examples when
useful. Store only the article in the `blog_post` state key.
""",
   output_key="blog_post",
)

reviewer = Agent(
   name="Reviewer",
   model=MODEL,
   description="Reviews the article and ends the loop when it is acceptable.",
   instruction="""
Review `{blog_post}` against `{blog_outline}` for completeness, organization,
clarity, and technical accuracy.

If the article passes, call `exit_loop`.
If it needs revision, give concise, specific feedback for the Writer. Do not
rewrite the article yourself.
""",
   tools=[exit_loop],
)

review_cycle = LoopAgent(
   name="ReviewCycle",
   description="Rewrites and reviews the article, bounded to three attempts.",
   sub_agents=[writer, reviewer],
   max_iterations=3,
)

finalizer = Agent(
   name="Finalizer",
   model=MODEL,
   description="Returns the completed article to the user.",
   instruction="""
Return `{blog_post}` exactly as Markdown.
Do not return JSON, the outline, review feedback, or an explanation of the
workflow. The article itself must be your complete response.
""",
   output_key="final_response",
)

root_agent = SequentialAgent(
   name="ContentWorkflow",
   description="Plans, writes, reviews, and returns an article.",
   sub_agents=[planner, review_cycle, finalizer],
)

app = App(
   name="build_ai_agent_google_adk",
   root_agent=root_agent,
)
