# Assignment 4: Reflection

## Student Name: Nazia Fazili

---

## Part 1: MCP Tools + Customer Data Agent

### Toolset Design Decisions
- Which MCP tools did you include in each `tool_filter`, and why?
The Customer Data Agent has access to all 15 MCP tools because it manages customer records and support tickets. Hence it's tool_filter includes all MCP tools. The Support Agent uses a restricted tool_filter that excludes five sensitive operations: adding or updating customers, activating or disabling accounts, and deleting tickets. This makes the system safer by allowing the Support Agent to use only the tools it needs to help customers.

- How does the support toolset's filter limit what the support agent can do?
The support toolset's tool_filter limits which MCP tools the Support Agent can access. It blocks sensitive actions like adding or updating customers, activating or disabling accounts, and deleting tickets. The Support Agent can still look up customer information, troubleshoot problems, and create or update support tickets.

### Data Agent Instruction
- What capabilities did you include in the system instruction?
I included capabilities to retrieve, add, update, and manage customer records and support tickets. The agent can also search and filter records, view statistics, and activate or disable customer accounts. For sensitive actions like deleting tickets or disabling accounts, it must confirm with the user first.

- How does the instruction guide the agent's tool selection?
The instruction tells the agent to first understand the user's request and then choose the correct MCP tool based on its name and description. If information is missing, it asks for clarification. 
---

## Part 2: Multi-Agent A2A System

### Support Agent Design
- What knowledge did you embed in the support agent's instruction?
I included troubleshooting steps for common customer problems such as login issues, failed payments, billing problems, slow performance, feature requests, and data export issues. 

- How does it combine its knowledge base with its filtered MCP toolset?
The Support Agent uses its knowledge base to understand the problem and suggest solutions. It uses MCP tools to look up customer information, check existing tickets, and create or update tickets when needed. 

### Host Agent Orchestration
- How does the SequentialAgent coordinate between sub-agents?
The SequentialAgent coordinates the agents by running them one at a time in a fixed order. It first calls the Customer Data Agent to retrieve customer and ticket information, then calls the Support Agent to troubleshoot the issue and suggest solutions.

- What happens when the Customer Data Agent returns data to the Support Agent?
The Customer Data Agent retrieves customer/ticket information using MCP tools. The Support Agent can use that information to understand the customer's issue, suggest solutions, and create or update support tickets if needed.

### A2A Protocol Insights
- How does agent discovery work via AgentCards?
AgentCards are like business cards for agents. They contain information about each agent such as its name, capabilities, skills, and URL.
When the Host Agent needs to communicate with another agent, it uses the agent's URL to find and read its AgentCard. This tells the Host Agent how to connect to that agent and communicate with it using the A2A protocol.

- What role does the `.well-known/agent-card.json` endpoint play?
The .well-known/agent-card.json endpoint is where an agent's AgentCard can be found. The agent shares information about itself like what it can do and how to contact it. The Host Agent uses this information to find and communicate with them.

- How does RemoteA2aAgent differ from direct function calls?
RemoteA2aAgent lets one agant to communicate with another agent over a network using the A2A protocol. A direct function call runs another function within the same application.
---

## Part 3: Challenges and Solutions

### Technical Challenges
- What was the most difficult part of the implementation?
The most difficult part was understanding how all the agents, MCP tools, and A2A connections work together. 

- How did you debug agent communication issues?
I debugged agent communication issues by checking the logs and error messages to see where the problem was happening. I tested the MCP server and individual agents separately before testing the complete workflow. I also used ADK Web to check whether the agents were communicating correctly.

### Architecture Decisions
- Why is the SequentialAgent pattern appropriate for this use case?
The SequentialAgent pattern works well for this application because the agents need to run in a specific order. The Customer Data Agent runs first to collect customer and ticket information. Then the Support Agent uses that information to understand the issue and provide solutions. This makes the workflow simple, organized, and easier to test and debug.
- What are the trade-offs vs. direct agent calls?
Using SequentialAgent makes the workflow easier to organize because agents run in a fixed order. It also makes testing and debugging easier. However, it can be slower because both agents run even when one is not needed. Direct agent calls can be faster and give more control
---

## Bonus: Routing Modes (if attempted)

### Advanced Router
- How does the dynamic routing decide which agents to call?
Dynamic routing checks the customer's request for keywords and decides whether to run the Data Agent, Support Agent, or both. The decision is saved in session state. Callbacks then run or skip each agent based on that decision. For example, if a customer asks how to reset a password, only the Support Agent runs. If they ask to check their account and fix a login issue, both agents run.

- What callback patterns did you use?
I used before_agent_callback to control which agents run. The Router saves the routing decision, and the callbacks check that decision to either run or skip the Customer Data and Support Agents.

### Parallel Router
- How does parallel execution improve latency?
- What synthesis strategy did you use to combine results?

### Mode Comparison

Report measured wall-clock latency (seconds) for the same query in each mode, and how you measured it.

| Mode | Agents Called | Latency | Context Passing |
|------|-------------|---------|-----------------|
| Basic (Sequential) | | | |
| Advanced (Dynamic) | | | |
| Parallel | | | |

---

## Key Learnings
1. Learned how multiple agents work together.
2. Learned how agents communicate using A2A.
3. Learned how agents use MCP tools to access data.
4. Learned how to limit tool access for each agent.
5. Learned how SequentialAgent runs agents in order.
6. Learned how dynamic routing selects which agents to run.

## Ideas for Improvement
- Make it easier to track how agents communicate.
-
