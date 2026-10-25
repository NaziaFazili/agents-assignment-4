"""
Part 2: Agent Factory and AgentCard Definitions (Agent Cards, 10 points)

Create AgentCards for A2A discovery and a factory function to create all agents.

AgentCards are the A2A protocol's way of advertising agent capabilities.
They include metadata like name, URL, description, skills, and examples.

Requirements:
  - create_customer_data_agent_card() returns valid AgentCard
  - create_support_agent_card() returns valid AgentCard
  - create_host_agent_card() returns valid AgentCard
  - create_all_agents() returns dict with all agents and cards

Each AgentCard needs:
  - name: Human-readable agent name
  - url: The agent's server URL
  - description: What the agent does
  - version: Version string (e.g., '1.0')
  - capabilities: AgentCapabilities(streaming=True)
  - default_input_modes: ['text/plain']
  - default_output_modes: ['text/plain'] or ['application/json']
  - preferred_transport: TransportProtocol.jsonrpc
  - skills: List of AgentSkill with id, name, description, tags, examples
"""

import logging

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    TransportProtocol,
)

# Import agent creation functions
from customer_data_agent.agent import create_agent as create_customer_data_agent
from host_agent.agent import create_agent as create_host_agent
from shared.agents_config import (
    CUSTOMER_DATA_AGENT_URL,
    HOST_AGENT_URL,
    SUPPORT_AGENT_URL,
)
from support_agent.agent import create_agent as create_support_agent

logger = logging.getLogger(__name__)
# =============================================================================
# 1: Customer Data Agent Card
# =============================================================================


def create_customer_data_agent_card() -> AgentCard:
    """
    Create AgentCard for Customer Data Agent.

    Return an AgentCard with:
      - name='Customer Data Agent'
      - url=CUSTOMER_DATA_AGENT_URL
      - description describing data management capabilities
      - version='1.0'
      - capabilities=AgentCapabilities(streaming=True)
      - default_input_modes=['text/plain']
      - default_output_modes=['application/json']
      - preferred_transport=TransportProtocol.jsonrpc
      - skills: at least one AgentSkill with relevant examples

    Example AgentSkill:
        AgentSkill(
            id='manage_customer_data',
            name='Manage Customer Data',
            description='Access and manage customer information and tickets',
            tags=['customers', 'tickets', 'data', 'database', 'mcp'],
            examples=[
                'Get customer information for ID 5',
                'List all active customers',
                'Show me all open tickets with high priority',
            ],
        )
    """
    logger.info("Creating Customer Data Agent Card")
    try:
        card = AgentCard(
            name="Customer Data Agent",
            url=CUSTOMER_DATA_AGENT_URL,
            description="Manages customer records, support tickets, and database statistics using MCP tools.",
            version="1.0",
            capabilities=AgentCapabilities(streaming=True),
            default_input_modes=["text/plain"],
            default_output_modes=["application/json"],
            preferred_transport=TransportProtocol.jsonrpc,
            skills=[
                AgentSkill(
                    id="manage_customer_data",
                    name="Manage Customer Data",
                    description="Access and manage customer information and support tickets.",
                    tags=["customers", "tickets", "data", "database", "mcp"],
                    examples=[
                        "Get customer information for ID 5",
                        "List all active customers",
                        "Show me all open tickets with high priority",
                        "Create a support ticket for customer 1",
                        "Get customer and ticket statistics",
                    ],
                )
            ],
        )
        logger.info("Customer Data Agent Card successfully")
        return card

    except Exception:
        logger.exception("Failed to create Customer Data Agent Card")
        raise


# =============================================================================
# 2: Support Agent Card
# =============================================================================


def create_support_agent_card() -> AgentCard:
    """
    Create AgentCard for Support Agent.

    Return an AgentCard with:
      - name='Support Agent'
      - url=SUPPORT_AGENT_URL
      - description describing support capabilities
      - version='1.0'
      - capabilities=AgentCapabilities(streaming=True)
      - default_input_modes=['text/plain']
      - default_output_modes=['text/plain']
      - preferred_transport=TransportProtocol.jsonrpc
      - skills: at least one AgentSkill with support-related examples

    Example AgentSkill:
        AgentSkill(
            id='provide_support',
            name='Provide Customer Support',
            description='Troubleshoot issues and provide solutions',
            tags=['support', 'troubleshooting', 'solutions', 'help'],
            examples=[
                "I can't login to my account",
                'How do I reset my password?',
                'My payment failed, what should I do?',
            ],
        )
    """
    logger.info("Creating Support Agent Card")
    try:
        card = AgentCard(
            name="Support Agent",
            url=SUPPORT_AGENT_URL,
            description="Provides customer support, troubleshooting, and ticket assistance using safe MCP tools.",
            version="1.0",
            capabilities=AgentCapabilities(streaming=True),
            default_input_modes=["text/plain"],
            default_output_modes=["text/plain"],
            preferred_transport=TransportProtocol.jsonrpc,
            skills=[
                AgentSkill(
                    id="provide_support",
                    name="Provide Customer Support",
                    description="Troubleshoot customer issues and provide solutions for login, billing, performance, and data export problems.",
                    tags=["support", "troubleshooting", "solutions", "help"],
                    examples=[
                        "I can't login to my account",
                        "How do I reset my password?",
                        "My payment failed, what should I do?",
                        "The application is loading slowly",
                        "I am unable to export my data",
                    ],
                )
            ],
        )

        logger.info("Support Agent Card created successfully")
        return card

    except Exception:
        logger.exception("Failed to create Support Agent Card")
        raise


# =============================================================================
# 3: Host Agent Card
# =============================================================================


def create_host_agent_card() -> AgentCard:
    """
    Create AgentCard for Host Agent (Orchestrator).

    Return an AgentCard with:
      - name='Customer Support Host Agent'
      - url=HOST_AGENT_URL
      - description describing orchestration capabilities
      - version='1.0'
      - capabilities=AgentCapabilities(streaming=True)
      - default_input_modes=['text/plain']
      - default_output_modes=['text/plain']
      - preferred_transport=TransportProtocol.jsonrpc
      - skills: at least one AgentSkill describing comprehensive support

    Example AgentSkill:
        AgentSkill(
            id='comprehensive_support',
            name='Comprehensive Customer Support',
            description='Provides complete support by combining data access and solutions',
            tags=['orchestration', 'support', 'data', 'coordination'],
            examples=[
                "I'm having login issues, can you check my account?",
                'Show me my open tickets and help resolve them',
            ],
        )
    """
    logger.info("Creating Host Agent Card")

    try:
        card = AgentCard(
            name="Customer Support Host Agent",
            url=HOST_AGENT_URL,
            description="Coordinates Customer Data and Support Agents to provide customer information, ticket management, and troubleshooting solutions.",
            version="1.0",
            capabilities=AgentCapabilities(streaming=True),
            default_input_modes=["text/plain"],
            default_output_modes=["text/plain"],
            preferred_transport=TransportProtocol.jsonrpc,
            skills=[
                AgentSkill(
                    id="comprehensive_support",
                    name="Comprehensive Customer Support",
                    description="Provides complete customer support by coordinating customer and ticket data lookup and troubleshooting solutions.",
                    tags=["orchestration", "support", "data", "coordination"],
                    examples=[
                        "I'm having login issues, can you check my account?",
                        "Show me my open tickets and help resolve them",
                        "Check customer 5 and help with a billing issue",
                    ],
                )
            ],
        )

        logger.info("Host Agent Card created successfully")
        return card

    except Exception:
        logger.exception("Failed to create Host Agent Card")
        raise


# =============================================================================
# 4: Factory Function
# =============================================================================


def create_all_agents():
    """
    Create all agents for the customer support system.

    Create all agents and their cards, return a dictionary with:
      {
          'customer_data': {
              'agent': <Agent from create_customer_data_agent()>,
              'card': <AgentCard from create_customer_data_agent_card()>,
              'port': 10020,
          },
          'support': {
              'agent': <Agent from create_support_agent()>,
              'card': <AgentCard from create_support_agent_card()>,
              'port': 10021,
          },
          'host': {
              'agent': <Agent from create_host_agent()>,
              'card': <AgentCard from create_host_agent_card()>,
              'port': 10022,
          },
      }

    Returns:
        Dictionary with all agents and their cards
    """
    logger.info("Creating all Customer Support Agents")

    try:
        agents = {
            "customer_data": {
                "agent": create_customer_data_agent(),
                "card": create_customer_data_agent_card(),
                "port": 10020,
            },
            "support": {
                "agent": create_support_agent(),
                "card": create_support_agent_card(),
                "port": 10021,
            },
            "host": {
                "agent": create_host_agent(),
                "card": create_host_agent_card(),
                "port": 10022,
            },
        }

        logger.info("All Customer Support Agents created successfully")
        return agents

    except Exception:
        logger.exception("Failed to create Customer Support Agents")
        raise
