from custom_crew_agent import OccupancyDataAnalyst, CustomCrew, CustomTask

# Create the occupancy data analyst agent
occupancy_agent = OccupancyDataAnalyst()

# Define a task for the agent
occupancy_task = CustomTask(
    description="Answer occupancy queries using Neo4j data. Query: {query}",
    agent=occupancy_agent,
    expected_output="A text answer to the user's occupancy query, based on Neo4j data."
)

# Create the crew
crew = CustomCrew(
    agents=[occupancy_agent],
    tasks=[occupancy_task]
)

def run_crew_query(user_query: str):
    """Run a query using the custom CrewAI-style implementation."""
    print(f"[Custom Crew Runner] Received query: {user_query}")
    try:
        result = crew.kickoff(inputs={"query": user_query})
        print(f"[Custom Crew Runner] Crew result: {result}")
        return result
    except Exception as e:
        print(f"[Custom Crew Runner] Exception: {e}")
        raise
