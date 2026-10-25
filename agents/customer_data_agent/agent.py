"""
Part 1: Customer Data Agent (10 points)

Create an ADK Agent that manages customer and ticket data via McpToolset.

This agent should:
  - Use the Gemini model from agents_config
  - Have a descriptive instruction telling the LLM its role and capabilities
  - Include the customer data McpToolset so it can access customer/ticket data

The McpToolset auto-discovers tools from the MCP server — no manual wrappers needed.
You configure which tools the agent can access via the tool_filter in the toolset.

Requirements (README.md Part 1 also grades this agent's McpToolset integration,
error handling and instruction quality; see its Evaluation Rubric for the points):
  - create_agent() returns a configured google.adk.agents.Agent
  - Agent has a detailed instruction string
  - Agent uses create_customer_data_toolset()

Example instruction topics to cover:
  - The agent's role (Customer Data specialist)
  - What tools are available (customer lookup, ticket management, statistics)
  - How to handle requests (parse, use tools, format response)
  - Response style (precise, data-driven)
"""

import logging
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from shared.agents_config import GEMINI_MODEL
from shared.mcp_toolset import create_customer_data_toolset

# Configure logging for this agent
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [CUSTOMER_DATA_AGENT] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_agent() -> Agent:
    """
    Create the Customer Data Agent.

    Create and return an Agent instance with:
      1. model=GEMINI_MODEL
      2. name='customer_data_agent'
      3. instruction=<your detailed instruction string>
      4. tools=[create_customer_data_toolset()]

    The McpToolset automatically discovers all filtered tools from the MCP
    server. You pass the toolset instance in the tools list — ADK handles
    the rest.

    Example:
        return Agent(
            model=GEMINI_MODEL,
            name='customer_data_agent',
            instruction=\"\"\"
            You are the Customer Data Agent...
            Your capabilities:
            - Retrieve customer information by ID
            - List customers with filters
            ...
            \"\"\",
            tools=[create_customer_data_toolset()],
        )

    Returns:
        Configured Agent instance
    """
    instruction = """
     You are a Customer Data Agent  responsible for managing customer records and support tickets.

    Your capabilities include:
    - Retrieve customer information by customer ID.
    - List customers with filters such as status ('active' or 'disabled')
    - Add new customer records, providing details like name, email, phone, status: ('active' or 'disabled')
    - Update existing customer information, providing the customer ID and other details like name, email, phone, status
    - Activate or disable customer accounts.
    - Retrieve support tickets by ticket ID.
    - List and filter support tickets by ID, status or priority.
    - Create new support tickets.
    - Update existing support tickets by status or priority.
    - Delete support tickets when explicitly requested and authorized.
    - Retrieve customer and support ticket statistics.
    - Search tickets by keyword

    When handling a request:
    1. Identify whether the request is customer or ticket related.
    2. Determine the operation required (retrieve, list, create, update, delete, search, or statistics).
    3. Select the available MCP tool to perform the requested operation, based on its name and description.
    4. If required information is missing or unclear, ask the user for clarification before calling the tool.
    5. Use the MCP tool and check its response before answering.
    6. Present the results clearly and accurately.
    7. If a record is not found, explain that no matching record was found.
    8. If an MCP tool fails, explain the error in simple terms without inventing results. Do not claim success.

    IMPORTANT: Do not invent customer records, ticket details, or statistics.
               Always use MCP tools for database operations.
               Only perform operations supported by the available tools.
    """
    logger.info("Creating Customer Data Agent")

    try:
        logger.info("Initializing Customer Data MCP toolset")

        toolset = create_customer_data_toolset()

        if not GEMINI_MODEL:
            logger.error(
                "Initialization Failed: The shared variable GEMINI_MODEL is empty or invalid."
            )
            raise ValueError(
                "GEMINI MODEL environment variable must contain a valid model name string."
            )

        agent = Agent(
            model=GEMINI_MODEL,
            name="customer_data_agent",
            description="Manages customer records, support tickets, and statistics.",
            instruction=instruction,
            tools=[toolset],
        )
        logger.info("Customer Data Agent created successfully")

        return agent
    except Exception:
        logger.exception("Failed to create Customer Data Agent")
        raise
