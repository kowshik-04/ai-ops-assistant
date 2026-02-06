from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
import os

app = FastAPI(
    title="AI Operations Assistant",
    description="Multi-agent AI system for task planning and execution",
    version="1.0.0"
)

planner = PlannerAgent()
executor = ExecutorAgent()
verifier = VerifierAgent()

@app.get("/")
def root():
    """Serve the UI"""
    return FileResponse("index.html")

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "operational",
        "service": "AI Operations Assistant",
        "version": "1.0.0",
        "endpoints": {
            "ui": "GET /",
            "api": "POST /run?query=<your_query>",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.post("/run")
def run_task(query: str):
    """
    Execute a natural language task using multi-agent system
    
    Args:
        query: Natural language query (e.g., "Find AI repos and Mumbai weather")
    
    Returns:
        Structured JSON with results from GitHub and Weather APIs
    """
    plan = planner.create_plan(query)
    results, log = executor.execute(plan)
    final_output = verifier.verify(query, results, log)
    return final_output

