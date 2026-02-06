import json
from llm.client import LLMClient

class VerifierAgent:
    def __init__(self):
        self.llm = LLMClient()
    
    def verify(self, user_query: str, results: dict, execution_log: list):
        # Basic validation
        missing = []
        
        if "github" not in results or not results["github"]:
            missing.append("github")
        
        if "weather" not in results:
            missing.append("weather")
        
        verified = len(missing) == 0
        
        # LLM-powered quality check and summary generation
        summary = self._generate_summary(user_query, results, verified)
        
        return {
            "request": user_query,
            "verified": verified,
            "missing_data": missing,
            "data_sources": ["GitHub API", "OpenWeather API"],
            "summary": summary,
            "results": results,
            "execution_log": execution_log
        }
    
    def _generate_summary(self, user_query: str, results: dict, verified: bool) -> str:
        if not verified:
            return "Incomplete execution: Some data sources failed to respond."
        
        system_prompt = """You are a Verifier Agent. Generate a concise summary.
    Output JSON: {"summary": "your summary"}"""
        
        user_prompt = f"""
User Query: {user_query}

Results:
{json.dumps(results, indent=2)}

Create a brief summary that answers the user's question using the data above.
"""
        
        try:
            response = self.llm.generate_json(system_prompt, user_prompt)
            summary_data = json.loads(response)
            return summary_data.get("summary", "Results retrieved successfully.")
        except Exception:
            return "Results retrieved successfully."
