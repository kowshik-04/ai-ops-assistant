from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool

class ExecutorAgent:
    def __init__(self):
        self.github = GitHubTool()
        self.weather = WeatherTool()

    def execute(self, plan):
        results = {}
        execution_log = []

        for step in plan.steps:
            try:
                if step.tool == "github":
                    results["github"] = self.github.search_repositories(**step.params)

                elif step.tool == "weather":
                    results["weather"] = self.weather.get_weather(**step.params)

                execution_log.append(
                    {"tool": step.tool, "status": "success"}
                )

            except Exception as e:
                execution_log.append(
                    {"tool": step.tool, "status": "failed", "error": str(e)}
                )

        return results, execution_log
