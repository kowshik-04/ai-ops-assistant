import json
from llm.client import LLMClient
from schemas.plan_schema import Plan

class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def create_plan(self, user_query: str) -> Plan:
        system_prompt = """
You are a Planner Agent. Your job is to convert natural language requests into a structured execution plan.

Available Tools:
1. github:
   - Action: search_repositories
   - Params: {"query": "search term", "limit": number (default 3)}
   
2. weather:
   - Action: get_weather
   - Params: {"city": "city name"}

Output Format (JSON only):
{
  "steps": [
    {"tool": "github", "action": "search_repositories", "params": {"query": "AI", "limit": 3}},
    {"tool": "weather", "action": "get_weather", "params": {"city": "Bangalore"}}
  ]
}

Rules:
- Output ONLY valid JSON matching the schema above
- Include ALL necessary steps to fulfill the request
- Extract city names from the query, default to "Bangalore" if not specified
- For GitHub searches, extract relevant keywords
- No explanations, just JSON
"""

        plan_json = self.llm.generate_json(system_prompt, user_query)
        plan_dict = json.loads(plan_json)
        return Plan(**plan_dict)
