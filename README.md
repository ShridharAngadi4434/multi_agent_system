🧠 Multi-Agent Research System (Autogen + MCP Integration)

A modular multi-agent system designed to perform research, analyze data, and generate summaries autonomously.
Built using Microsoft Autogen, integrated with Tavily MCP (web search),
and supporting token usage tracking, async orchestration, and configurable agents.

🚀 Features

✅ Three autonomous agents with distinct roles:

Research Agent → performs web research (via MCP or Tavily API fallback)

Analysis Agent → extracts key patterns, insights, and themes

Summary Agent → generates structured, human-readable summaries

✅ Chained Agent Communication — output from one agent feeds into the next.
✅ MCP Integration (Tavily Remote MCP).
✅ Async Execution — non-blocking orchestration using asyncio.
✅ Error Handling & Logging in every step.
✅ Token Usage Tracking for each agent and total.
✅ Environment-based Config for models and API keys.

🏗️ Project Structure
```
multi_agent_research/
│
├── agents/
│   ├── __init__.py
│   ├── research_agent.py     # Research Agent (web search / Tavily MCP)
│   ├── analysis_agent.py     # Analysis Agent (extracts key themes)
│   ├── summary_agent.py      # Summary Agent (creates final markdown summary)
│
├── utils/
│   ├── __init__.py
│   ├── logger.py             # Central logging configuration
│   ├── mcp_helper.py         # Optional MCP adapter loader
│   ├── model_client.py       # Model setup helper
│   ├── token_tracker.py      # (optional) token tracking helper
│
├── mcp.config.json           # Tavily MCP launcher (optional)
├── main.py                   # Main orchestrator script
├── requirements.txt          # Dependencies
└── README.md                 
```

⚙️ Setup Instructions
1️⃣ Clone and create environment
git clone <your_repo_url>
cd multi_agent_research

# Create a virtual environment
python -m venv mar_env
mar_env\Scripts\activate       # Windows
# source mar_env/bin/activate  # macOS/Linux

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Set environment variables

Create a .env file in your project root:

OPENAI_API_KEY=your_openai_key
MCP_URL="https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>"
TAVILY_API_KEY=your_tavily_api_key
MODEL_NAME=your_model_name

Then load them automatically (or use your terminal set command).

4️⃣ (Optional) MCP Configuration for Tavily

You can define your Tavily MCP server setup in mcp.config.json:

{
  "mcpServers": {
    "tavily-remote-mcp": {
      "command": "npx -y mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>",
      "env": {}
    }
  }
}


This file is optional and does not affect your code runtime —
it’s just a helper for anyone who wants to auto-launch the MCP server.

5️⃣ Run the MCP server (optional)

If you’re using Tavily’s remote MCP:

npx -y mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>


This starts a local MCP bridge that Autogen can connect to via MCP_URL.

6️⃣ Run the Multi-Agent System

Now you can start the orchestration:

python main.py --topic "Quantum Computing"

🧩 Example Output
======================== FINAL SUMMARY ========================

=== RESEARCH SUMMARY ===
Key Developments:
1. Error correction breakthroughs in 2024...
2. IBM's new quantum processor...
3. Google's quantum advantage experiments...

Main Themes:
- Error mitigation techniques
- Scalability challenges
- Commercial applications

Sources:
- [Source 1]: https://...
- [Source 2]: https://...

Generated at: 2025-10-31 14:30:00

===============================================================
Total Tokens Consumed: 1705

⚙️ How It Works (Agent Chain)
flowchart LR
    A[Research Agent] -->|Research Data| B[Analysis Agent]
    B -->|Insights JSON| C[Summary Agent]
    C -->|Final Markdown| D[Output]


Research Agent

Fetches information via MCP (Tavily search)

Falls back to direct Tavily API if MCP unavailable

Analysis Agent

Processes research data

Extracts patterns, key points, and high-level insights

Summary Agent

Converts analysis into a user-friendly Markdown summary

🪵 Logging

All logs are managed using utils/logger.py.
They print to console with timestamps and log levels:

2025-11-01 16:22:44,988 | INFO    | main | 🚀 Starting orchestration for topic: Quantum Computing
2025-11-01 16:22:44,989 | INFO    | model_client | 🧠 Initializing model client with model: gpt-4o-mini-2024-07-18
2025-11-01 16:22:45,541 | INFO    | mcp_helper | Connecting to MCP server at https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>
2025-11-01 16:22:48,329 | INFO    | mcp_helper | ✅ Loaded 4 MCP adapters.
2025-11-01 16:22:48,329 | INFO    | research_agent | ✅ Using 4 MCP tools for Research Agent.
2025-11-01 16:22:48,329 | INFO    | research_agent | 🔧 Tool loaded: tavily_search
2025-11-01 16:22:48,330 | INFO    | research_agent | 🔧 Tool loaded: tavily_extract
2025-11-01 16:22:48,330 | INFO    | research_agent | 🔧 Tool loaded: tavily_crawl
2025-11-01 16:22:48,330 | INFO    | research_agent | 🔧 Tool loaded: tavily_map
2025-11-01 16:22:48,331 | INFO    | research_agent | Researching topic: Quantum Computing
2025-11-01 16:22:54,323 | INFO    | token_tracker | 🧾 Tokens used by research_agent: 1928
2025-11-01 16:22:54,323 | INFO    | research_agent | Research complete.
2025-11-01 16:22:54,323 | INFO    | analysis_agent | Analyzing research data.
2025-11-01 16:23:04,846 | INFO    | token_tracker | 🧾 Tokens used by analysis_agent: 6432
2025-11-01 16:23:04,847 | INFO    | analysis_agent | Analysis complete.
2025-11-01 16:23:10,496 | INFO    | token_tracker | 🧾 Tokens used by summary_agent: 903
2025-11-01 16:23:10,497 | INFO    | summary_agent | ✅ Summary generation complete.

🧾 Token Usage Tracking

Each agent tracks token usage:

🧾 Tokens used by Research Agent: 682
🧾 Tokens used by Analysis Agent: 514
🧾 Tokens used by Summary Agent: 486
Total Tokens Consumed: 1682


✅ Supports both dict and RequestUsage token response types.

🧠 Error Handling

Missing API keys → logged warning, skips step

MCP connection failure → falls back to direct Tavily API

Empty response or failed task → handled gracefully, continues pipeline

🔧 Configurability
Config	Source	Description
OPENAI_API_KEY	.env	OpenAI or compatible model key
MCP_URL	.env	MCP server endpoint (optional)
MODEL_NAME	.env	Model name (gpt-4o-mini-2024-07-18, etc.)
TAVILY_API_KEY	.env	Tavily Web Search key
🧩 Extending the System

You can easily extend:

Add a Citation Agent for automated reference validation.

Add a Visualization Agent for chart/graph creation.

Replace Tavily with Bing/SerpAPI for alternate web search.

🧰 Troubleshooting
Issue	Cause	Fix
MCP connection failed	MCP server not running	Run Tavily MCP manually
OpenAIError: api_key missing	Missing env var	Add OPENAI_API_KEY
Token tracking failed	Different result format	Use updated universal tracking logic
No summary generated	Missing research data	Check web search response

🧑‍💻 Authors

Shridhar Angadi
Multi-Agent Research System Developer | LLMs | Autogen | MCP
