# AI Operations Assistant

A multi-agent AI system that accepts natural-language tasks, plans execution steps, calls real APIs, and returns structured answers. Built with FastAPI and powered by OpenAI's LLM for intelligent task orchestration.

## 🏗️ Architecture

This system implements a **three-agent architecture** for robust task execution:

```
User Query → Planner Agent → Executor Agent → Verifier Agent → Final Output
```

### Agent Responsibilities

| Agent | Purpose | Details |
|-------|---------|---------|
| **Planner** | Creates structured execution plan | Uses LLM to convert natural language into JSON plan with tool selection |
| **Executor** | Executes steps and calls APIs | Orchestrates GitHub and Weather API calls with retry logic |
| **Verifier** | Validates output and fixes gaps | Uses LLM to check completeness and generate human-readable summary |

### Data Flow

1. **User Input**: Natural language query via REST API
2. **Planning Phase**: Planner Agent analyzes query and creates structured plan
3. **Execution Phase**: Executor Agent runs plan steps, calling external APIs
4. **Verification Phase**: Verifier Agent validates results and generates summary
5. **Output**: Structured JSON response with all data

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key
- GitHub Personal Access Token
- OpenWeather API key

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ai-ops-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=sk-your-actual-key
GITHUB_TOKEN=ghp_your-actual-token
OPENWEATHER_API_KEY=your-actual-key
```

**Where to get API keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **GitHub Token**: https://github.com/settings/tokens (needs `public_repo` permission)
- **OpenWeather**: https://openweathermap.org/api (free tier works)

## 🎯 How to Run Locally

**Single command to start the server:**

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### Making Requests

**Using curl:**
```bash
curl -X POST "http://localhost:8000/run?query=Find%20top%20AI%20repositories%20and%20Bangalore%20weather"
```

**Using browser:**
```
http://localhost:8000/run?query=Find top AI repositories and Bangalore weather
```

**Using Python requests:**
```python
import requests
response = requests.post("http://localhost:8000/run", params={"query": "Find ML repos and Delhi weather"})
print(response.json())
```

## 📋 Example Prompts

Try these queries to test the system:

1. **"Find top AI GitHub repositories and Bangalore weather"**
2. **"Show me Python trending repos and Delhi weather"**
3. **"Get machine learning projects on GitHub and Mumbai weather"**
4. **"Search for deep learning repositories and Chennai weather"**
5. **"Find React repositories and Hyderabad weather"**

### Expected Output Format

```json
{
  "request": "Find top AI repositories and Bangalore weather",
  "verified": true,
  "missing_data": [],
  "data_sources": ["GitHub API", "OpenWeather API"],
  "summary": "Found 3 top AI repositories with stars ranging from 50k-100k. Current weather in Bangalore is 24°C with clear skies.",
  "results": {
    "github": [
      {"name": "openai/gpt-4", "stars": 95000, "description": "...", "url": "..."}
    ],
    "weather": {
      "city": "Bangalore",
      "temperature_c": 24,
      "condition": "clear sky"
    }
  },
  "execution_log": [
    {"tool": "github", "status": "success"},
    {"tool": "weather", "status": "success"}
  ]
}
```

## 🔧 Project Structure

```
ai-ops-assistant/
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── planner.py         # LLM-powered planning agent
│   ├── executor.py        # API execution orchestrator
│   └── verifier.py        # Result validation agent
├── tools/                 # External API integrations
│   ├── __init__.py
│   ├── github_tool.py     # GitHub API with retry logic
│   └── weather_tool.py    # OpenWeather API integration
├── llm/                   # LLM client wrapper
│   ├── __init__.py
│   └── client.py          # OpenAI client with JSON mode
├── schemas/               # Pydantic schemas
│   ├── __init__.py
│   └── plan_schema.py     # Structured plan schema
├── main.py                # FastAPI application entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
└── README.md             # This file
```

## 🌐 Integrated APIs

### 1. GitHub API
- **Purpose**: Search and retrieve repository data
- **Endpoint**: `https://api.github.com/search/repositories`
- **Authentication**: Personal Access Token
- **Features**: Star count, descriptions, URLs
- **Retry Logic**: 3 attempts with exponential backoff

### 2. OpenWeather API
- **Purpose**: Real-time weather data
- **Endpoint**: `https://api.openweathermap.org/data/2.5/weather`
- **Authentication**: API Key
- **Features**: Temperature, humidity, conditions, wind speed
- **Retry Logic**: 3 attempts with exponential backoff

## ⚙️ Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM | ✅ Yes |
| `GITHUB_TOKEN` | GitHub Personal Access Token | ✅ Yes |
| `OPENWEATHER_API_KEY` | OpenWeather API key | ✅ Yes |

See `.env.example` for template.

## 🧪 Testing

### Quick Test
```bash
# Start server
uvicorn main:app --reload

# In another terminal
curl -X POST "http://localhost:8000/run?query=Find AI repos and Bangalore weather"
```

### Verify Agents
- **Planner**: Check that JSON plan is generated with correct structure
- **Executor**: Verify both API calls succeed
- **Verifier**: Confirm summary is generated and data is complete

## ⚠️ Known Limitations / Tradeoffs

1. **Sequential Execution**: Tools run sequentially, not in parallel (easier debugging, slightly slower)
2. **No Caching**: API responses aren't cached (simpler implementation, higher API usage)
3. **Limited Error Recovery**: If both APIs fail, system returns partial results (graceful degradation)
4. **Fixed Tool Set**: Only GitHub and Weather APIs (extensible design for future additions)
5. **LLM Dependency**: Requires OpenAI API for planning and verification (could add fallback to rule-based)
6. **Rate Limits**: No rate limit handling beyond retries (free tier APIs have limits)

## 🔍 Key Features

✅ **Multi-Agent Architecture**: Clear separation of concerns (Planning, Execution, Verification)  
✅ **LLM-Powered Reasoning**: Structured JSON outputs using OpenAI's JSON mode  
✅ **Real API Integrations**: Live data from GitHub and OpenWeather  
✅ **Retry Logic**: Automatic retry with exponential backoff for API failures  
✅ **Structured Outputs**: Pydantic schemas for type safety  
✅ **Error Handling**: Graceful degradation with detailed execution logs  
✅ **One-Command Deploy**: Runs with single `uvicorn` command  

## 🎓 Design Decisions

- **Why FastAPI?** Fast, modern, automatic API docs, great for demos
- **Why OpenAI?** Reliable structured outputs with JSON mode
- **Why Three Agents?** Clear separation: think (plan), do (execute), check (verify)
- **Why Retry Logic?** Production-ready resilience against transient failures

## 📝 License

MIT License - Feel free to use for learning and projects.

---

**Built with ❤️ for demonstrating agent-based AI systems**
