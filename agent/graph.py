import os
from typing import TypedDict, Annotated, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import json

# --- State Definition ---
class AgentState(TypedDict):
    messages: List[BaseMessage]
    research_data: Optional[str]
    analyst_report: Optional[str]
    business_strategy: Optional[str]

# --- Config & LLM Setup ---
# We assume GOOGLE_API_KEY is in environment or passed via .env
# For safety, we default to a placeholder if not set, but the agent will fail gracefully.
# Check if API key exists, otherwise use a dummy key to prevent Pydantic validation error on init
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = "dummy_key_for_init"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# --- Nodes ---

async def researcher_node(state: AgentState):
    """
    Connects to the local MCP server to search for data.
    """
    print("--- RESEARCHER NODE ---")
    query = "Vet market 2020-2025 data"

    # Connect to the MCP Server
    # Note: In a real deployment, the server path would be dynamic or an env var.
    server_params = StdioServerParameters(
        command="python",
        args=["server/mcp_server.py"],
        env=os.environ.copy() # Pass current env to child
    )

    research_content = ""

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize connection
                await session.initialize()

                # List tools to verify (optional)
                tools = await session.list_tools()
                # print(f"Available tools: {tools}")

                # Call the tool
                result = await session.call_tool("search_vet_market_data", arguments={"query": query})

                # Extract text content from result
                # Result is typically a CallToolResult object containing 'content' list
                if result.content:
                    for content_block in result.content:
                        if content_block.type == 'text':
                            research_content += content_block.text
                else:
                    research_content = "No data found."

    except Exception as e:
        research_content = f"Error connecting to MCP Server: {str(e)}"
        print(f"Researcher Error: {e}")

    return {"research_data": research_content}

async def analyst_node(state: AgentState):
    """
    Analyzes the research data and creates a report.
    """
    print("--- ANALYST NODE ---")
    data = state.get("research_data", "")

    prompt = f"""
    You are an Expert Data Analyst.
    Analyze the following data about the Veterinary Market (2020-2025).
    Summarize the key findings into a clean, professional report.
    Format the output with Markdown.

    Data:
    {data}
    """

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"analyst_report": response.content}

async def strategist_node(state: AgentState):
    """
    Creates a business model based on the analyst report.
    """
    print("--- STRATEGIST NODE ---")
    report = state.get("analyst_report", "")

    prompt = f"""
    You are a Senior Business Strategist.
    Based on the following market analysis report, define a high-level Business Model Canvas
    for a new startup entering this space.

    Focus on:
    1. Value Propositions
    2. Customer Segments
    3. Revenue Streams
    4. Key Activities

    Format the output with Markdown.

    Report:
    {report}
    """

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"business_strategy": response.content}

# --- Graph Construction ---
workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("strategist", strategist_node)

# Linear flow
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "strategist")
workflow.add_edge("strategist", END)

app_graph = workflow.compile()

# --- Helper for running the graph ---
async def run_agent_workflow():
    inputs = {"messages": [HumanMessage(content="Start research")]}
    # We await the invocation
    result = await app_graph.ainvoke(inputs)
    return result

if __name__ == "__main__":
    # Test run
    import asyncio
    try:
        res = asyncio.run(run_agent_workflow())
        print("Final Result Keys:", res.keys())
        print("Analyst Report Preview:", res['analyst_report'][:100])
    except Exception as e:
        print(f"Execution failed: {e}")
