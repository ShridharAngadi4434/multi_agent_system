from utils.logger import setup_logger
from autogen_agentchat.agents import AssistantAgent
from utils.token_tracker import extract_token_usage

logger = setup_logger("analysis_agent")

async def build_analysis_agent(model_client):
    agent = AssistantAgent(
        name="analysis_agent",
        system_message="You are the Analysis Agent. Given research results (JSON text), extract key points, themes, and patterns.",
        model_client=model_client,
    )
    return agent

async def run_analysis(agent: AssistantAgent, research_text: str) -> str:
    try:
        logger.info("Analyzing research data.")
        prompt = (
            "Analyze the following research data (JSON format). "
            "Return a JSON with 'key_points', 'themes', and 'summary'. "
            f"RESEARCH_DATA:\n{research_text}"
        )
        result = await agent.run(task=prompt)
        
        text = getattr(result, "content", None)
        if not text and hasattr(result, "messages") and result.messages:
            text = result.messages[-1].content
        if not text:
            text = str(result)

        # ✅ Token usage tracking (via centralized helper)
        total_tokens = extract_token_usage(result, agent_name=agent.name)

        # ✅ Clean content
        if isinstance(text, str):
            text = text.replace("\\n", "\n").replace("\\", "").strip()

        logger.info("Analysis complete.")
        return text.strip(), total_tokens
    
    except Exception as e:
        logger.exception("Analysis failed: %s", e)
        return "{}"