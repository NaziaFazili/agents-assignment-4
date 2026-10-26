"""
BONUS Part A: Advanced Router Agent with Dynamic Routing (+15 points)

This is an OPTIONAL bonus implementation that adds intelligent routing:
  - Analyzes query intent to determine which agents to invoke
  - Uses before_agent_callback to conditionally skip agents
  - Includes a router LLM agent for task decomposition

Architecture:
  Orchestrator (SequentialAgent)
    -> Router Agent (LLM Agent) -- analyzes query, sets routing decision
    -> Sequential Executor (SequentialAgent)
         -> RemoteA2aAgent("customer_data") with before_agent_callback
         -> RemoteA2aAgent("support_specialist") with before_agent_callback

Requirements for bonus points:
  - analyze_query_intent function works correctly (5 pts)
  - Callback functions properly skip/run agents (4 pts)
  - Router agent with dynamic instruction (3 pts)
  - Full orchestrator assembled correctly (3 pts)
"""

import logging
import os
import sys
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# IMPORTANT: Apply A2A compatibility patch BEFORE importing RemoteA2aAgent
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.genai import types
from shared import a2a_compat  # noqa: F401
from shared.agents_config import (
    CUSTOMER_DATA_AGENT_URL,
    GEMINI_MODEL,
    SUPPORT_AGENT_URL,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [ROUTER_AGENT] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# =============================================================================
# BONUS: Routing Logic Functions
# =============================================================================


def analyze_query_intent(query: str) -> dict:
    """
    Analyze query to determine routing strategy.

    Implement query analysis that returns:
      - needs_data: bool (does the query need customer/ticket data?)
      - needs_support: bool (does the query need support/help?)
      - urgency: str ('low', 'medium', 'high')
      - execution_mode: str ('sequential', 'data_only', 'support_only')

    Hints:
      - Check for data keywords: 'customer', 'ticket', 'id', 'list', 'search'
      - Check for support keywords: 'help', 'issue', 'problem', 'reset', 'fix'
      - Check for urgency keywords: 'urgent', 'immediately', 'asap', 'critical'

    Example return:
        {
            'needs_data': True,
            'needs_support': True,
            'urgency': 'medium',
            'execution_mode': 'sequential'
        }
    """
    query = (query or "").lower()

    data_keywords = (
        "customer",
        "ticket",
        "account",
        "id",
        "list",
        "search",
        "record",
        "statistics",
    )

    support_keywords = (
        "help",
        "issue",
        "problem",
        "reset",
        "fix",
        "login",
        "password",
        "billing",
        "payment",
        "troubleshoot",
    )

    high_urgency = ("urgent", "immediately", "asap", "critical")
    medium_urgency = ("soon", "important", "priority")

    needs_data = any(word in query for word in data_keywords)
    needs_support = any(word in query for word in support_keywords)

    # If query matches neither list, the code defaults to using both agents.
    if not needs_data and not needs_support:
        needs_data = True
        needs_support = True

    if needs_data and needs_support:
        execution_mode = "sequential"
    elif needs_data:
        execution_mode = "data_only"
    else:
        execution_mode = "support_only"

    if any(word in query for word in high_urgency):
        urgency = "high"
    elif any(word in query for word in medium_urgency):
        urgency = "medium"
    else:
        urgency = "low"

    return {
        "needs_data": needs_data,
        "needs_support": needs_support,
        "urgency": urgency,
        "execution_mode": execution_mode,
    }


# =============================================================================
# BONUS: Callback Functions for Dynamic Routing
# =============================================================================


def should_run_customer_data_agent(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """
    Callback to determine if Customer Data Agent should run.

    Check callback_context.state for routing_decision.
      - If needs_data is False, return Content to skip the agent
      - If needs_data is True (or missing), return None to run it

    Hints:
      - routing_decision = callback_context.state.get('routing_decision', {})
      - Return None to run the agent
      - Return types.Content(parts=[types.Part(text="...")]) to skip
    """

    decision = callback_context.state.get("routing_decision", {})
    logger.info("Customer Data routing decision: %s", decision)

    if decision.get("needs_data", True) is False:
        logger.info("Skipping Customer Data Agent")
        return types.Content(parts=[types.Part(text="Customer Data Agent skipped.")])

    logger.info("Running Customer Data Agent")
    return None


def should_run_support_agent(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """
    Callback to determine if Support Agent should run.

    Similar to should_run_customer_data_agent but checks needs_support.
    """
    decision = callback_context.state.get("routing_decision", {})

    if decision.get("needs_support", True) is False:
        logger.info("Skipping Support Agent")
        return types.Content(parts=[types.Part(text="Support Agent skipped.")])

    logger.info("Running Support Agent")
    return None


# =============================================================================
# BONUS: Router Agent with Dynamic Instruction
# =============================================================================


def create_router_instruction(readonly_context) -> str:
    """
    Dynamic instruction for router agent based on query analysis.

    Implement this function to:
      1. Get the user's query from readonly_context.user_content (a types.Content;
         the text is in readonly_context.user_content.parts[0].text)
      2. Call analyze_query_intent(query)
      3. Store routing_decision in session state. NOTE: an instruction provider receives a
         ReadonlyContext, whose .state is a read-only view — assigning to it does not reliably
         persist. Compute and store the decision in a before_agent_callback on the router agent
         (which receives a writable CallbackContext); this function can then read it back.
      4. Return a dynamic instruction string based on the analysis
    """
    decision = readonly_context.state.get("routing_decision", {})

    return f"""
    You are a router agent for a customer support system.

    Routing decision:
    - Needs data: {decision.get("needs_data", True)}
    - Needs support: {decision.get("needs_support", True)}
    - Urgency: {decision.get("urgency", "medium")}
    - Execution mode: {decision.get("execution_mode", "sequential")}

    Briefly explain which agents are needed and why.
    if Needs data is True then customer data agent is required to run.
    if Needs support is TRUE, then support agent is required to run
    """


def before_router_agent(callback_context: CallbackContext) -> Optional[types.Content]:

    content = callback_context.user_content

    query = content.parts[0].text if content and content.parts else ""

    decision = analyze_query_intent(query)

    callback_context.state["routing_decision"] = decision

    logger.info("Routing decision: %s", decision)

    return None


# =============================================================================
# BONUS: Create Advanced Agent
# =============================================================================


def create_agent() -> SequentialAgent:
    """
    Create the advanced router agent with dynamic routing capabilities.

    Assemble the full orchestrator:
      1. Create router_agent (Agent with dynamic instruction)
      2. Create remote_customer_data (RemoteA2aAgent with before_agent_callback)
      3. Create remote_support (RemoteA2aAgent with before_agent_callback)
      4. Create sequential_execution_agent (SequentialAgent with both remotes)
      5. Create orchestrator (SequentialAgent with router + executor)

    Returns:
        Configured SequentialAgent with router and conditional sub-agents
    """
    logger.info("Creating Advanced Router Agent")

    try:
        router_agent = Agent(
            name="query_router",
            model=GEMINI_MODEL,
            description="Analyzes customer requests and makes routing decisions.",
            instruction=create_router_instruction,
            before_agent_callback=before_router_agent,
        )

        remote_customer_data = RemoteA2aAgent(
            name="customer_data",
            agent_card=f"{CUSTOMER_DATA_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
            before_agent_callback=should_run_customer_data_agent,
        )

        remote_support = RemoteA2aAgent(
            name="support_specialist",
            agent_card=f"{SUPPORT_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
            before_agent_callback=should_run_support_agent,
        )

        sequential_executor = SequentialAgent(
            name="sequential_executor",
            sub_agents=[
                remote_customer_data,
                remote_support,
            ],
        )

        orchestrator = SequentialAgent(
            name="host_agent",
            sub_agents=[
                router_agent,
                sequential_executor,
            ],
        )

        logger.info("Advanced Router Agent created successfully")
        return orchestrator
    except Exception:
        logger.exception("Failed to create Advanced Router Agent")
        raise
