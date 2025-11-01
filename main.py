import asyncio
from utils.model_client import get_model_client
from utils.logger import setup_logger
from utils.mcp_helper import load_mcp_adapters_if_available
from agents.research_agent import build_research_agent, run_research
from agents.analysis_agent import build_analysis_agent, run_analysis
from agents.summary_agent import build_summary_agent, run_summary

logger = setup_logger("main")

async def orchestrate(topic: str):
    """Main Orchestration with MCP integration."""
    logger.info(f"🚀 Starting orchestration for topic: {topic}")
    model_client = get_model_client()

    # Load MCP tool adapters if MCP_URL is set
    mcp_adapters = await load_mcp_adapters_if_available()

    # Build agents
    research_agent = await build_research_agent(model_client, mcp_adapters)
    analysis_agent = await build_analysis_agent(model_client)
    summary_agent = await build_summary_agent(model_client)

    total_tokens = 0

    # Run agents sequentially
    research_data, research_tokens = await run_research(research_agent, topic)
    total_tokens += research_tokens

    analysis_data, analysis_tokens = await run_analysis(analysis_agent, research_data)
    total_tokens += analysis_tokens

    final_summary, summary_tokens = await run_summary(summary_agent, analysis_data, topic)
    total_tokens += summary_tokens

    print("\n\n======================== FINAL SUMMARY ========================\n")
    print(final_summary)
    print("\n===============================================================\n")

    # ✅ Print total token usage
    print(f"Total Tokens Consumed: {total_tokens}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", "-t", required=True, help="Topic to research")
    args = parser.parse_args()

    asyncio.run(orchestrate(args.topic))