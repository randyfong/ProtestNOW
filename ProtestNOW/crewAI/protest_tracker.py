import os
from crewai import Agent, Task, Crew
from crewai_tools import TavilySearchTool

# API Keys
os.environ["TAVILY_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyC93T5uHlf2-8HW9hvrsxuD1V0OzBYwhRU"

# LLM Configuration
# User-requested model: Gemini 3.1 Flash
gemini_llm = "gemini/gemini-3.1-flash"

# Tools
search_tool = TavilySearchTool()

# Agent 1: The Investigative Journalist
journalist = Agent(
    role="Investigative Journalist",
    goal="Identify the top 10 most significant or interesting protests happening today (March 28, 2026) in major US cities (NYC, SF, DC, Chicago, etc.). "
         "Find the protest name/organization, city, state, core cause, future events planned by the same group, and website URL.",
    backstory="You are a lead researcher with a knack for finding real-time events. You dig deep into news and social feeds "
              "to find the pulse of the nation. You focus strictly on today's events.",
    tools=[search_tool],
    llm=gemini_llm,
    verbose=True
)

# Agent 2: The Data Architect
architect = Agent(
    role="Information Organizer",
    goal="Sort the gathered protest data and format it for the infographic. "
         "Sort findings by State > City > Name > Weblink.",
    backstory="You are a precise data architect who transforms messy research into structured, high-value information sets.",
    llm=gemini_llm,
    verbose=True
)

# Agent 3: The Counter-Culture Designer
designer = Agent(
    role="Visual Prompt Engineer",
    goal="Format the final report into a Markdown table and prepare a design-ready summary for a 1960s-style infographic.",
    backstory="You bring the creative soul to the data. You understand the 'Revolutionary Pulse' and can translate "
              "current events into a vibe of peace, love, and social progress.",
    llm=gemini_llm,
    verbose=True
)

# Tasks
task_research = Task(
    description="Search for major US protests occurring today, March 28, 2026. "
                "For each protest, identify: Name/Organization, City, State, Core Cause, Website URL, and any future events.",
    expected_output="A comprehensive list of at least 10 protests with all required details.",
    agent=journalist
)

task_organize = Task(
    description="Take the list of protests and sort them by State, then City, then Name. "
                "Ensure every entry has a weblink.",
    expected_output="A structured list of protests sorted by State > City > Name.",
    agent=architect,
    context=[task_research]
)

task_final_report = Task(
    description="Format the sorted protest data into a clean Markdown table (Name, Location, Date, Website, Core Cause). "
                "Follow it with a summary block labeled 'INFOGRAPHIC DATA' that lists the protests in a way that "
                "highlights the 'Peace, Love, and Social Progress' vibe.",
    expected_output="A Markdown table followed by an infographic data summary.",
    agent=designer,
    context=[task_organize]
)

# Execution
crew = Crew(
    agents=[journalist, architect, designer],
    tasks=[task_research, task_organize, task_final_report],
    verbose=True
)

result = crew.kickoff()

print("\n\n--- FINAL OUTPUT ---\n")
print(result)
