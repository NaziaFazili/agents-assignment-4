"""
BONUS Part B: Parallel Router Agent (+10 points)

This is an OPTIONAL bonus implementation that executes agents in parallel.

Architecture:
  Orchestrator (SequentialAgent)
    -> Parallel Worker (ParallelAgent)
         -> RemoteA2aAgent("customer_data") with after_agent_callback -> state
         -> RemoteA2aAgent("support_specialist") with after_agent_callback -> state
    -> Summary Agent (LLM Agent) -- synthesizes parallel results

Key concepts:
  - ParallelAgent runs sub-agents concurrently instead of one after another
  - RemoteA2aAgent has NO output_key field (passing one raises a pydantic
    "Extra inputs are not permitted" ValidationError). Store each remote agent's
    output in state with an after_agent_callback instead.
  - Summary agent reads state and combines outputs into cohesive response

Requirements for bonus points:
  - RemoteA2aAgent output stored in state via after_agent_callback (3 pts)
  - ParallelAgent correctly assembled (2 pts)
  - Summary agent with dynamic instruction reading state (3 pts)
  - Full orchestrator assembled correctly (2 pts)
"""

import logging
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# IMPORTANT: Apply A2A compatibility patch
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from shared import a2a_compat  # noqa: F401
from shared.agents_config import (
    CUSTOMER_DATA_AGENT_URL,
    GEMINI_MODEL,
    SUPPORT_AGENT_URL,
)

logger = logging.getLogger(__name__)


# =============================================================================
# BONUS: Summary Instruction Function
# =============================================================================


def create_summary_instruction(readonly_context: ReadonlyContext) -> str:
    """
    Create instruction for summary agent that combines parallel results.

    Implement this function to:
      1. Read customer_data_output from readonly_context.state
      2. Read support_specialist_output from readonly_context.state
      3. Return an instruction telling the LLM to synthesize both outputs

    Hints:
      - data_output = readonly_context.state.get("customer_data_output", "")
      - support_output = readonly_context.state.get("support_specialist_output", "")
      - Instruction should tell the LLM to combine outputs naturally
    """

    logger.info("create summary instruction: ")
    data_output = readonly_context.state.get("customer_data_output", "")
    support_output = readonly_context.state.get("support_specialist_output", "")

    summary_instruction = f"""
      You are a Summary Agent responsible for combining results from the Customer Data Agent and Support Agent.

      Customer Data Agent Results:
      {data_output}

      Support Agent Results:
      {support_output}

      Instructions:
      1. Review the information from both agents.
      2. Combine the results into one clear and helpful response.
      3. Include relevant customer details and support recommendations.
      4. Avoid repeating the same information.
      5. If information is missing, mention it clearly.
      6. Do not invent customer details or ticket information.
      7. Keep the response professional and easy to understand.
      """

    return summary_instruction


def save_customer_data_output(callback_context: CallbackContext):
    for event in reversed(callback_context.session.events):
        if (
            event.author == callback_context.agent_name
            and event.content
            and event.content.parts
        ):
            callback_context.state["customer_data_output"] = "".join(
                part.text or "" for part in event.content.parts
            )
            logger.info("Customer data output saved to state.")
            break


def save_support_output(callback_context: CallbackContext):
    for event in reversed(callback_context.session.events):
        if (
            event.author == callback_context.agent_name
            and event.content
            and event.content.parts
        ):
            callback_context.state["support_specialist_output"] = "".join(
                part.text or "" for part in event.content.parts
            )
            logger.info("Support data output saved to state.")
            break


# =============================================================================
# BONUS: Create Parallel Agent
# =============================================================================


def create_agent() -> SequentialAgent:
    """
    Create a parallel router agent that executes agents concurrently.

    Assemble the full orchestrator:

      1. Create remote_customer_data (RemoteA2aAgent):
         - after_agent_callback that writes this agent's final response text to
           callback_context.state['customer_data_output']

      2. Create remote_support (RemoteA2aAgent):
         - after_agent_callback that writes this agent's final response text to
           callback_context.state['support_specialist_output']

      Hint (after_agent_callback receives a writable CallbackContext):
          for event in reversed(callback_context.session.events):
              if (event.author == callback_context.agent_name
                      and event.content and event.content.parts):
                  callback_context.state[key] = "".join(
                      p.text or "" for p in event.content.parts)
                  break
          return None

      3. Create parallel_worker_agent (ParallelAgent):
         - sub_agents=[remote_customer_data, remote_support]

      4. Create summary_agent (Agent):
         - instruction=create_summary_instruction
         - include_contents='none'

      5. Create orchestrator (SequentialAgent):
         - sub_agents=[parallel_worker_agent, summary_agent]

    Returns:
        Configured SequentialAgent with parallel execution and synthesis
    """
    logger.info("Creating Parallel Router Agent")
    try:
        remote_customer_data = RemoteA2aAgent(
            name="customer_data",
            agent_card=f"{CUSTOMER_DATA_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
            after_agent_callback=save_customer_data_output,
        )

        remote_support = RemoteA2aAgent(
            name="support_specialist",
            agent_card=f"{SUPPORT_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
            after_agent_callback=save_support_output,
        )

        parallel_worker_agent = ParallelAgent(
            name="parallel_worker",
            sub_agents=[remote_customer_data, remote_support],
        )

        summary_agent = Agent(
            name="summary_agent",
            model=GEMINI_MODEL,
            description="Combines customer data and support results.",
            instruction=create_summary_instruction,
            include_contents="none",
        )

        orchestrator = SequentialAgent(
            name="host_agent",
            sub_agents=[parallel_worker_agent, summary_agent],
        )

        logger.info("Parallel Router Agent created successfully")
        return orchestrator
    except Exception:
        logger.exception("Failed to create Parallel Router Agent")
        raise
