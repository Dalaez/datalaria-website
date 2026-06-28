---
title: "MCP (Model Context Protocol): The Standard That Wants to Be the USB of Artificial Intelligence"
date: 2026-06-28
draft: false
categories: ["Artificial Intelligence", "Engineering"]
tags: ["mcp", "model context protocol", "tool calling", "function calling", "anthropic", "llm", "api"]
description: "A technical analysis of Anthropic's MCP protocol, the open standard for connecting LLMs with external tools. A comparison with native Tool Calling and its impact on agent architecture."
summary: "Today, every LLM has its own way of connecting to your databases and tools. It's a chaos of proprietary integrations. MCP (Model Context Protocol) promises to end this by becoming the 'universal plug' of AI. We analyze if it's truly the future or just another standard that will die trying."
social_text: "Today every AI has its own way of connecting to your databases. It's an integration hell. Is MCP (Model Context Protocol) the 'universal USB' that will save us, or just another standard doomed to fail? I analyze it in depth 🔌🤖📊 #AI #MCP #Anthropic #ToolCalling #Engineering"
image: cover.png
weight: 10
authorAvatar: datalaria-logo.png
---

If you've ever tried building an AI agent system in production, you know the pain. During the construction of the [agentic radar for Obsolescence](/en/posts/obs_part5_radar_agent/), I faced the problem of connecting Gemini 2.5 with my Supabase database and an external API. I had to write custom code to adapt the tool schema (*Tool Calling*) to the exact format that Google demands.

If tomorrow I decided to migrate that exact same system to Anthropic's Claude or OpenAI's GPT-4o, I would have to rewrite the entire tool integration layer because each vendor uses its own JSON dialect and its own argument validation logic (*Function Calling*).

It's the same chaos we lived through in the late 90s with mobile phone chargers: every brand had its proprietary connector. Then USB arrived and unified everything. That is exactly the ambition behind **MCP (Model Context Protocol)**: to become the USB of Artificial Intelligence.

![MCP Protocol Architecture Diagram](mcp_diagram.png)

### What Exactly is the Model Context Protocol?

Initially proposed by Anthropic and rapidly adopted by a coalition of open-source companies, MCP is an open standard for connecting AI models with data sources and tools.

The design premise is elegantly simple, separating the architecture into two independent pieces:
1. **MCP Hosts**: Applications or frameworks where the LLM resides (for example, the Claude desktop app, a LangChain script, or your own Python application).
2. **MCP Servers**: Lightweight, small programs that expose data or tools to the Host following a strict standard contract (for example, an MCP server that reads your PostgreSQL database, another that reads your GitHub repository).

The magic happens in the middle. The Host (the LLM) tells the MCP Server: *"What tools and resources do you have available?"*. The server responds in a universal format. From there, the LLM can read, write, or execute actions without the developer having had to write a proprietary integration between *that specific model* and *that specific tool*.

### Comparison: MCP vs Native Tool Calling

On this blog, I have vehemently defended why **[Tool Calling is infinitely superior to traditional RAG](/en/posts/obs_part5_radar_agent/)** for industrial applications that require precision. MCP does not replace Tool Calling; it standardizes it.

Let's look at the architectural difference:

| Feature | Classic Tool Calling | MCP (Model Context Protocol) |
| :--- | :--- | :--- |
| **Integration** | 1-to-1 (Specific Model ↔ Specific Tool) | N-to-M (Any Model ↔ Any MCP Server) |
| **Format** | Dictated by the LLM vendor (Google, OpenAI) | Standard, agnostic JSON-RPC 2.0 |
| **Discovery** | Developer injects tools into the prompt | Host discovers tools dynamically |
| **Portability** | None. Migrating LLMs requires refactoring. | Total. You write the MCP server once. |

### Building an MCP Server: A Real Example

To illustrate why this changes the game for operations and backend engineers, let's imagine we want to expose a Supabase table (e.g., critical component inventory) to our LLM.

With a traditional CrewAI or Langchain approach, we would write a custom tool bound to that framework. With MCP, we write a universal Python server using the official SDK:

```python
from mcp.server.fastmcp import FastMCP
import supabase

# Initialize the MCP server
mcp = FastMCP("Supabase_Inventory_Server")
db = supabase.create_client(URL, KEY)

@mcp.tool()
def get_critical_stock(part_number: str) -> str:
    """Fetches the stock level of a specific component."""
    response = db.table("inventory").select("stock").eq("pn", part_number).execute()
    
    if not response.data:
        return "Component not found."
    
    stock = response.data[0]['stock']
    return f"The current stock for {part_number} is {stock} units."

if __name__ == "__main__":
    # The server starts and listens for requests over stdio (JSON-RPC)
    mcp.run()
```

That code block is all you need. Once running, *any* MCP-compatible application (including Claude's official interface) can connect to this server, read the function's description (docstring), and decide when to call `get_critical_stock` with the correct arguments.

### Opinion: Will MCP Be the Definitive Standard?

The history of software is littered with "universal standards" that only managed to add one more standard to the list of competing standards. Will MCP survive?

It has two massive advantages in its favor. The first is that **it solves a real, acute pain point** for corporate developers, who are sick of rewriting integrations every time a new model comes out. The second is the **local-first approach**. Standard MCP communication uses `stdio` (standard input/output), which means the MCP server runs locally on your machine or private network. This is a wet dream for industrial cybersecurity because the data never leaves your infrastructure until the LLM explicitly and authorizedly requests it.

However, MCP's success will depend on adoption by the dominant duopoly: Google and OpenAI. If Anthropic manages to create a large enough open-source ecosystem (like Kubernetes once did against proprietary clouds), the other giants will be forced to support it natively.

If you are designing the [architecture for an Agentic Project Management Office](/en/posts/proj_ops_part2_agentic_pmo/) or any system where you need to connect AI agents with legacy ERPs, PLMs, or document repositories, my recommendation is to bet on isolating your connectors. Today it might be through independent Python functions, and tomorrow, probably, wrapping those same functions in an MCP Server.

Just as USB killed hundreds of proprietary connectors, MCP has the potential to finally democratize LLM access to the "muscle" of enterprise data.

---

#### Sources of Interest:
* [**Model Context Protocol**: Official Site and Documentation](https://modelcontextprotocol.io/)
* [**Anthropic**: Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
* [**GitHub**: Open Source MCP Servers Directory](https://github.com/modelcontextprotocol/servers)
* [**Datalaria**: The Agentic Radar: Why LLMs Won't Save Your Supply Chain (And Tool Calling Will)](/en/posts/obs_part5_radar_agent/)
* [**Datalaria**: Project Operations Engineering Part 2: The Agentic PMO](/en/posts/proj_ops_part2_agentic_pmo/)
