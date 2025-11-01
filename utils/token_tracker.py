from utils.logger import setup_logger

logger = setup_logger("token_tracker")


def extract_token_usage(result, agent_name="agent") -> int:
    """
    Safely extract total token usage from an autogen result.
    Supports both dict-based and RequestUsage objects.
    """
    total_tokens = 0
    try:
        # Case 1: usage directly on result
        if hasattr(result, "models_usage") and result.models_usage:
            usage = result.models_usage

            # Dict-based usage
            if isinstance(usage, dict):
                total_tokens = (
                    usage.get("total_tokens")
                    or usage.get("usage", {}).get("total_tokens")
                    or 0
                )
            else:
                # Object-based usage (RequestUsage)
                prompt_tokens = getattr(usage, "prompt_tokens", 0)
                completion_tokens = getattr(usage, "completion_tokens", 0)
                total_tokens = getattr(usage, "total_tokens", prompt_tokens + completion_tokens)

        # Case 2: usage inside messages
        elif hasattr(result, "messages") and result.messages:
            for msg in result.messages:
                msg_usage = getattr(msg, "models_usage", None)
                if msg_usage:
                    if isinstance(msg_usage, dict):
                        total_tokens += (
                            msg_usage.get("total_tokens")
                            or msg_usage.get("usage", {}).get("total_tokens")
                            or 0
                        )
                    else:
                        prompt_tokens = getattr(msg_usage, "prompt_tokens", 0)
                        completion_tokens = getattr(msg_usage, "completion_tokens", 0)
                        total_tokens += getattr(
                            msg_usage, "total_tokens", prompt_tokens + completion_tokens
                        )

        logger.info(f"🧾 Tokens used by {agent_name}: {total_tokens}")

    except Exception as token_err:
        logger.warning(f"⚠️ Token tracking failed for {agent_name}: {token_err}")

    return total_tokens