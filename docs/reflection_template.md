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
The most difficult part was understanding how all the agents, MCP tools, and A2A connections work together. I also struggled with understanding the code structure and which modules run first. 

- How did you debug agent communication issues?

### Architecture Decisions
- Why is the SequentialAgent pattern appropriate for this use case?
- What are the trade-offs vs. direct agent calls?

---

## Bonus: Routing Modes (if attempted)

### Advanced Router
- How does the dynamic routing decide which agents to call?
- What callback patterns did you use?

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
1.
2.
3.

## Ideas for Improvement
-
-
