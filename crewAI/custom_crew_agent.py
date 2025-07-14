import requests
from tool import neo4j_query_tool

class OccupancyDataAnalyst:
    """Custom agent that mimics CrewAI agent behavior but uses Ollama directly."""
    
    def __init__(self):
        self.role = "Occupancy Data Analyst"
        self.goal = "Answer queries related to occupancy data using Neo4j database"
        self.backstory = """You are an expert data analyst specializing in building occupancy and space utilization. 
        You have deep knowledge of Neo4j graph databases and Cypher query language."""
        self.tools = [neo4j_query_tool]
        self.verbose = True
        
    def execute_task(self, task_description: str, user_query: str) -> str:
        """Execute a task using the agent's capabilities."""
        
        if self.verbose:
            print(f"\n# Agent: {self.role}")
            print(f"## Task: {task_description}")
            print(f"## Query: {user_query}")
        
        # Step 1: Analyze the query and generate Cypher
        cypher_prompt = f"""
You are an expert in converting natural language queries to Cypher queries for a Neo4j database.

IMPORTANT: You must provide a COMPLETE Cypher query with proper RETURN clause.

DATABASE SCHEMA:
The database contains Occupancy nodes with these properties:
- Floor: The floor name (e.g., "First Floor", "Second Floor")
- SiteDetails: Location details (e.g., "Kalwa_Switchboard_ShopFloor")  
- RecordDate: Date in format 'YYYY-MM-DD'
- LocationCode: Location code (e.g., "LOC-IN-KALWA")
- WiFiCount: Number of WiFi connections (integer)
- TimeSlot: Time range (e.g., "01:45 - 02:00")

EXAMPLES:
Question: "What is the WiFi count on the First Floor of Kalwa location on date 6/14/2025?"
Cypher: MATCH (o:Occupancy) WHERE o.Floor = 'First Floor' AND o.LocationCode = 'LOC-IN-KALWA' AND o.RecordDate = '2025-06-14' RETURN sum(o.WiFiCount) as total_wifi_count

Question: "Show me occupancy data for Kalwa location"
Cypher: MATCH (o:Occupancy) WHERE o.LocationCode = 'LOC-IN-KALWA' RETURN o.Floor, o.RecordDate, o.WiFiCount, o.TimeSlot LIMIT 10

Question: "What is the total WiFi count for all locations?"
Cypher: MATCH (o:Occupancy) RETURN sum(o.WiFiCount) as total_wifi_count

Now convert this question to a COMPLETE Cypher query with RETURN clause:
Question: {user_query}
Cypher:"""

        try:
            if self.verbose:
                print("## Thought: I need to convert the natural language query to Cypher and execute it")
                print("## Using tool: neo4j_query_tool")
            
            # Get Cypher query from Ollama
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3:8b",
                    "prompt": cypher_prompt,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                return f"Error generating Cypher query: {response.status_code}"
            
            cypher_query = response.json().get("response", "").strip()
            
            # Clean up the Cypher query - extract the complete query
            if "MATCH" in cypher_query:
                # Find the start of the MATCH clause
                start_idx = cypher_query.find("MATCH")
                cypher_query = cypher_query[start_idx:]
                
                # Find the end - look for RETURN clause
                if "RETURN" in cypher_query:
                    # Take everything until the end of the RETURN clause
                    lines = cypher_query.split('\n')
                    complete_query = ""
                    for line in lines:
                        complete_query += line.strip() + " "
                        if "RETURN" in line and ("as" in line.lower() or line.strip().endswith(")")):
                            break
                    cypher_query = complete_query.strip()
                else:
                    # If no RETURN found, take the first line only
                    cypher_query = cypher_query.split('\n')[0].strip()
            
            if self.verbose:
                print(f"## Tool Input: {cypher_query}")
            
            # Execute the Cypher query
            db_result = neo4j_query_tool._run(cypher_query)
            
            if self.verbose:
                print(f"## Tool Output: {db_result}")
            
            if "Error" in db_result:
                return f"Database query failed: {db_result}"
            
            # Generate natural language response
            response_prompt = f"""
Based on this database query result, provide a clear, natural language answer to the user's question.

User Question: {user_query}
Database Result: {db_result}

Provide a concise, helpful answer in a conversational tone:"""

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3:8b",
                    "prompt": response_prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                natural_response = response.json().get("response", "").strip()
                
                if self.verbose:
                    print(f"## Final Answer: {natural_response}")
                
                return natural_response
            else:
                return f"Based on the database query, here's the raw data: {db_result}"
                
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            if self.verbose:
                print(f"## Error: {error_msg}")
            return error_msg

class CustomCrew:
    """Custom crew implementation that mimics CrewAI behavior."""
    
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks
        self.verbose = True
        
    def kickoff(self, inputs):
        """Execute the crew tasks."""
        
        if self.verbose:
            print("╭" + "─" * 100 + "╮")
            print("│" + " " * 40 + "Crew Execution Started" + " " * 38 + "│")
            print("│" + " " * 100 + "│")
            print("│  Crew Execution Started" + " " * 76 + "│")
            print("│  Name: custom_crew" + " " * 81 + "│")
            print("│" + " " * 100 + "│")
            print("╰" + "─" * 100 + "╯")
        
        # Execute the task with the first agent
        agent = self.agents[0]
        task = self.tasks[0]
        user_query = inputs.get("query", "")
        
        result = agent.execute_task(task.description, user_query)
        
        if self.verbose:
            print("╭" + "─" * 100 + "╮")
            print("│" + " " * 40 + "Crew Execution Completed" + " " * 36 + "│")
            print("│" + " " * 100 + "│")
            print("│  Status: ✅ Success" + " " * 79 + "│")
            print("│" + " " * 100 + "│")
            print("╰" + "─" * 100 + "╯")
        
        return result

class CustomTask:
    """Custom task implementation that mimics CrewAI Task."""
    
    def __init__(self, description, agent, expected_output):
        self.description = description
        self.agent = agent
        self.expected_output = expected_output
