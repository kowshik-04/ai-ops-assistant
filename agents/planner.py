import json
from llm.client import LLMClient
from schemas.plan_schema import Plan

class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def create_plan(self, user_query: str) -> Plan:
        system_prompt = """You are a Planner Agent. Convert natural language requests into structured execution plans.

Available Tools:
1. github: search_repositories with {"query": "search term", "limit": number}
2. weather: get_weather with {"city": "city name"}

Output only valid JSON with steps array. Extract cities from query, default to Bangalore."""

        plan_json = self.llm.generate_json(system_prompt, user_query)
        plan_dict = json.loads(plan_json)
        return Plan(**plan_dict)
