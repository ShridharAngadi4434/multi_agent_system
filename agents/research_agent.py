import os
import json
import httpx
from utils.logger import setup_logger
from dotenv import load_dotenv
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from utils.token_tracker import extract_token_usage

load_dotenv()

logger = setup_logger("research_agent")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

async def tavily_search(query: str, num: int = 5):
    """Search using Tavily API and return structured list of results."""
    if not TAVILY_API_KEY:
        logger.warning("TAVILY_API_KEY not found. Returning empty results.")
        return []

    url = "https://api.tavily.com/search"
    payload = {"api_key": TAVILY_API_KEY, "query": query, "max_results": num}
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            results = []
            for item in data.get("results", [])[:num]:
                results.append({
                    "title": item.get("title"),
                    "link": item.get("url"),
                    "snippet": item.get("content", "")[:400]
                })
            return results
    except Exception as e:
        logger.exception("Tavily search failed: %s", e)
        return []

def search_tool():
    """Create a FunctionTool for Tavily web search."""
    async def web_search(query: str, max_results: int = 5):
        logger.info(f"web_search called with query={query}")
        results = await tavily_search(query, max_results)
        return json.dumps(results, indent=2) if results else "[]"

    return FunctionTool(
        web_search,
        name="web_search",
        description="Usage: web_search(query: str, max_results: int=5)"
    )

async def build_research_agent(model_client, mcp_adapters=None):
    """Builds the Research Agent with Tavily search tool."""
    
    if mcp_adapters:
        tools = mcp_adapters
        logger.info(f"✅ Using {len(mcp_adapters)} MCP tools for Research Agent.")
    else:
        tools = [search_tool()]
        logger.info("⚠️ No MCP tools detected — using Tavily FunctionTool fallback.")

    for tool in tools:
        try:
            logger.info(f"🔧 Tool loaded: {tool.name}")
        except Exception:
            logger.info(f"🔧 Tool loaded: {tool}")

    agent = AssistantAgent(
        name="research_agent",
        system_message="You are the Research Agent. Use the web_search tool to find up-to-date information about the topic and return concise JSON-formatted findings.",
        model_client=model_client,
        tools=tools,
    )
    return agent


async def run_research(agent: AssistantAgent, topic: str) -> str:
    """Run the research agent to collect data on the topic."""
    try:
        logger.info(f"Researching topic: {topic}")
        result = await agent.run(
            task=f"Research the topic: {topic}. "
                 f"Use available tools. "
                 f"Return a JSON array of objects with title, link, and snippet."
        )
        text = getattr(result, "content", str(result))
        if not text and hasattr(result, "messages"):
            text = result.messages[-1].content

        # ✅ Token usage tracking 
        total_tokens = extract_token_usage(result, agent_name=agent.name)

        # ✅ Clean content
        if isinstance(text, str):
            text = text.replace("\\n", "\n").replace("\\", "").strip()

        logger.info("Research complete.")
        return text.strip(), total_tokens
    
    except Exception as e:
        logger.exception("Research failed: %s", e)
        return "[]"
