from utils.logger import setup_logger
from autogen_agentchat.agents import AssistantAgent
from utils.token_tracker import extract_token_usage
import datetime

logger = setup_logger("summary_agent")

async def build_summary_agent(model_client):
    agent = AssistantAgent(
        name="summary_agent",
        system_message=(
            "You are the Summary Agent. Given analyzed data, produce a clear, "
            "professional Markdown summary using the structure below:\n\n"
            "Topic: <topic>\n"
            "=== RESEARCH SUMMARY ===\n"
            "Key Developments:\n"
            "1. ...\n"
            "2. ...\n"
            "Main Themes:\n"
            "- ...\n"
            "Sources:\n"
            "- [Source 1]: https://...\n"
            "Generated at: <timestamp>\n\n"
            "Ensure your output matches this format exactly — no extra commentary."
        ),
        model_client=model_client,
    )
    return agent


async def run_summary(agent: AssistantAgent, analysis_text: str, topic: str) -> str:
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt = (
            f"Topic: {topic}\n\n"
            "You are given analyzed research data in JSON or text format below.\n"
            "Generate a Markdown summary strictly following this format:\n\n"
            "=== RESEARCH SUMMARY ===\n"
            "Key Developments:\n"
            "1. ...\n"
            "Main Themes:\n"
            "- ...\n"
            "Sources:\n"
            "- [Source 1]: https://...\n\n"
            f"Add 'Generated at: {now}' at the end.\n\n"
            f"ANALYSIS_DATA:\n{analysis_text}"
        )

        result = await agent.run(task=prompt)

        # ✅ Extract clean text content
        if hasattr(result, "messages") and result.messages:
            text = result.messages[-1].content
        elif hasattr(result, "content"):
            text = result.content
        else:
            text = str(result)

        # ✅ Token usage tracking
        total_tokens = extract_token_usage(result, agent_name=agent.name)

        # ✅ Decode escaped characters
        text = text.encode("utf-8").decode("unicode_escape")
        text = text.replace("\\n", "\n").replace("\\t", "\t").strip()

        if "Generated at:" not in text:
            text += f"\n\nGenerated at: {now}"

        logger.info("✅ Summary generation complete.")
        return text.strip(), total_tokens

    except Exception as e:
        logger.exception("❌ Summary generation failed: %s", e)
        return (
            f"Topic: {topic}\n\n"
            "=== RESEARCH SUMMARY ===\n"
            "Summary generation failed due to an internal error.\n"
            f"Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )