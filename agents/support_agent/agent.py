"""
Part 2: Support Agent (10 points)

Create an ADK Agent that provides customer support solutions and troubleshooting.

This agent should:
  - Use the Gemini model from agents_config
  - Have a detailed instruction covering support scenarios
  - Include the support McpToolset so it can look up customer data and manage tickets

The McpToolset auto-discovers tools from the MCP server. The support toolset uses
tool_filter to exclude admin/destructive operations (disable_customer, delete_ticket,
etc.) so the support agent can only perform safe operations.

Requirements:
  - create_agent() returns a configured google.adk.agents.Agent
  - Agent has a comprehensive instruction with support knowledge base
  - Agent uses create_support_toolset() for data-driven support

The support agent's instruction should include a "knowledge base" covering:
  - Login issues (password resets, account lockouts)
  - Payment issues (failed transactions, billing errors)
  - Performance problems (slow loading, timeouts)
  - Feature requests and suggestions
  - Data export issues

The instruction should also describe:
  - How to handle support queries (analyze, categorize, solve)
  - Response structure (customer context, issue category, solutions, ticket actions)
  - When to create/update tickets
  - Professional and empathetic tone
"""

import logging
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from shared.agents_config import GEMINI_MODEL
from shared.mcp_toolset import create_support_toolset

# Configure logging for this agent
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [SUPPORT_AGENT] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_agent() -> Agent:
    """
    Create the Support Agent.

    Create and return an Agent instance with:
      1. model=GEMINI_MODEL
      2. name='support_agent'
      3. instruction=<your detailed support instruction>
      4. tools=[create_support_toolset()]

    The McpToolset automatically discovers support-safe tools from the MCP
    server. Admin/destructive tools are excluded by the tool_filter.

    Example:
        return Agent(
            model=GEMINI_MODEL,
            name='support_agent',
            instruction=\"\"\"
            You are the Support Agent, a specialist in customer service...

            Your knowledge base includes solutions for:
            - Login issues (password resets, account lockouts)
            - Payment issues (failed transactions, billing errors)
            ...

            When handling support queries:
            1. Use MCP tools to retrieve customer information
            2. Analyze the customer's issue
            ...
            \"\"\",
            tools=[create_support_toolset()],
        )

    Returns:
        Configured Agent instance
    """
    logger.info("Creating Support Agent")
    instructions = """
      You are a Customer Support Agent responsible for helping customers troubleshoot problems and resolve support requests.

    Your capabilities include:
    - Retrieve customer information using available MCP tools.
    - Retrieve and search support tickets.
    - Create new support tickets when needed.
    - Update existing tickets when appropriate.
    - Provide troubleshooting guidance for common customer issues.

    KNOWLEDGE BASE:

    1. Login Issues:
       - For login failures, ask the customer to verify their credentials.
       - For forgotten passwords, guide customers through the password reset process.
       - For account lockouts, explain the available account recovery options.
       - Never request passwords or authentication codes.

    2. Payment and Billing Issues:
       - For failed payments, check available transaction or ticket information.
       - Suggest verifying payment information and checking for payment errors.
       - For billing discrepancies, gather relevant details and create a support ticket.
       - Never request full credit card details.

    3. Performance Problems:
       - For slow loading, suggest refreshing the page or checking internet connectivity.
       - For timeouts, suggest retrying the operation and checking for service issues.
       - Create a support ticket if the problem continues.

    4. Feature Requests and Suggestions:
       - Understand the customer's requested feature or improvement.
       - Gather details about the expected behavior and business need.
       - Create a support ticket to record the request.

    5. Data Export Issues:
       - Identify the type of data the customer wants to export.
       - Ask about the export format and any error messages.
       - Provide available troubleshooting steps.
       - Create a support ticket if the export repeatedly fails.

    WHEN HANDLING A SUPPORT REQUEST:

    1. Analyze the customer's question and identify the main issue.
    2. Categorize the issue as login, billing, performance, feature request, data export, or another support category.
    3. Retrieve customer details or existing tickets using the available auto-discovered MCP tools when needed.
    4. Select the appropriate MCP tool based on its description and required parameters.
    5. Ask for clarification if important information is missing.
    6. Provide clear, step-by-step troubleshooting instructions.
    7. Create a ticket when an issue cannot be resolved or requires follow-up.
    8. Update an existing ticket when new information is provided, avoiding unnecessary duplicate tickets.
    9. If a tool fails, explain the issue clearly without inventing results.

    RESPONSE FORMAT:

    - Customer Context: Customer information.
    - Issue Category: Type of support problem.
    - Recommended Solution: Clear steps to resolve the issue.
    - Ticket Actions: Whether a ticket was created, updated, or requires follow-up.

    IMPORTANT:
    - Always maintain a professional, polite, and empathetic tone.
    - Never invent customer records, ticket details, or statistics.
    - Use MCP tools for database operations.
    - Only use tools available through your filtered support toolset.
    - Do not perform administrative or destructive operations.
    - Never claim an operation succeeded unless the tool confirms success.
    - Do not expose sensitive customer information unnecessarily.
    """

    try:
        if not GEMINI_MODEL:
            logger.error(
                "Initialization Failed: The shared variable GEMINI_MODEL is empty or invalid."
            )
            raise ValueError(
                "GEMINI MODEL environment variable must contain a valid model name string."
            )
        support_tools = create_support_toolset()

        agent = Agent(
            name="support_agent",
            model=GEMINI_MODEL,
            description="Provides customer support, troubleshooting, and ticket assistance.",
            instruction=instructions,
            tools=[support_tools],
        )

        logger.info("Support Agent created successfully")

        return agent
    except Exception:
        logger.exception("Failed to create Support Agent")
        raise
