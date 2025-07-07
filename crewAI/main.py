from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai_agent import run_crewai_query

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/crewquery")
async def crew_query_endpoint(query: Query):
    try:
        result = run_crewai_query(query.query)
        return {"result": result}
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))