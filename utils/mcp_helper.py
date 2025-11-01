import os
from utils.logger import setup_logger

logger = setup_logger("mcp_helper")

try:
    from autogen_ext.tools.mcp import (
        StreamableHttpServerParams,
        mcp_server_tools,
    )
except ImportError:
    logger.warning("autogen-ext[mcp] not installed or unavailable.")
    StreamableHttpServerParams = None
    mcp_server_tools = None


async def load_mcp_adapters_if_available():
    """
    Attempts to load MCP tool adapters from a server if MCP_URL is provided.
    Returns a list of adapters (or empty if unavailable).
    """
    mcp_url = os.getenv("MCP_URL")

    if not mcp_url:
        logger.info("MCP_URL not provided, skipping MCP setup.")
        return []

    if mcp_server_tools is None:
        logger.warning("MCP extension not available.")
        return []

    try:
        server_params = StreamableHttpServerParams(
            url=mcp_url,
            timeout=30.0,
            sse_read_timeout=300.0,
            terminate_on_close=True,
        )
        logger.info(f"Connecting to MCP server at {mcp_url} ...")
        adapters = await mcp_server_tools(server_params)
        logger.info(f"✅ Loaded {len(adapters)} MCP adapters.")
        return adapters
    except Exception as e:
        logger.exception(f"MCP connection failed: {e}")
        return []
