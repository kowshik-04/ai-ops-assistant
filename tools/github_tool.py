import os
import requests
import time

class GitHubTool:
    def __init__(self):
        self.base_url = "https://api.github.com/search/repositories"
        self.token = os.getenv("GITHUB_TOKEN")
        self.max_retries = 3
        self.retry_delay = 1

    def search_repositories(self, query: str, limit: int = 3):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        params = {"q": query, "sort": "stars", "order": "desc", "per_page": limit}

        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
                response.raise_for_status()

                items = response.json().get("items", [])[:limit]
                return [
                    {
                        "name": repo["full_name"],
                        "stars": repo["stargazers_count"],
                        "description": repo.get("description", "No description"),
                        "url": repo["html_url"]
                    }
                    for repo in items
                ]
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise Exception(f"GitHub API error after {self.max_retries} retries: {str(e)}")
        
        return []
