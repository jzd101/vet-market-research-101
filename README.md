# AI Vet Market Research Team (LangGraph + MCP POC)

This project is a Proof of Concept (POC) demonstrating how to build a multi-agent AI system using **LangGraph** and the **Model Context Protocol (MCP)**.

The system simulates a team of AI agents working together to research the Veterinary Market and propose a business strategy.

## 🏗 Architecture

The project consists of three main components:

1.  **MCP Server (`server/mcp_server.py`):**
    *   A standalone server implementing the Model Context Protocol.
    *   Exposes a tool: `search_vet_market_data`.
    *   In a real-world scenario, this would connect to external APIs (Google, Tavily). Here, it serves mock data for reliable testing.

2.  **LangGraph Agent (`agent/graph.py`):**
    *   **Researcher Node:** Acts as an MCP Client. It spins up the MCP server, connects to it, and asks for data.
    *   **Analyst Node:** Uses Google Gemini (LLM) to summarize the raw data into a readable report.
    *   **Strategist Node:** Uses Google Gemini to translate the report into a Business Model Canvas.

3.  **Web UI (`app/main.py`):**
    *   Built with **Streamlit**.
    *   Provides a user-friendly interface to trigger the workflow and view the results.

## 🚀 How to Run

### Prerequisites

*   Python 3.10 or higher.
*   A **Google Gemini API Key** (Free tier available). [Get it here](https://aistudio.google.com/app/apikey).

### 1. Installation

Clone the repository (or download the files) and install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Setup API Key

You can create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

Or you can enter the key directly in the Web UI when you run the app.

### 3. Run the Application

Start the Streamlit web server:

```bash
streamlit run app/main.py
```

Open your browser at the URL shown (usually `http://localhost:8501`).

Click **"🚀 Start Research Workflow"** to see the agents in action!

## 🔧 How to Maintain & Extend

*   **Modify Data:** Edit `server/mcp_server.py` to change the mock data or replace it with a real API call.
*   **Adjust Prompts:** Edit `agent/graph.py` to change how the Analyst or Strategist processes information.
*   **Add Agents:** You can add more nodes to the graph in `agent/graph.py` (e.g., a "Marketing Expert" node).

## 💡 Challenges & Suggestions

*   **MCP Complexity:** Connecting a client to a server adds overhead. For simple apps, standard LangChain tools are easier. However, MCP is powerful because it allows tools to be hosted anywhere (remote servers, local processes) and shared across different AI apps (Claude Desktop, etc.).
*   **Async/Sync:** LangGraph is asynchronous. Streamlit is synchronous. We use `asyncio.run()` to bridge them, but for heavy workloads, a proper backend (FastAPI) + frontend (React) might be more robust.
*   **LLM Rate Limits:** If using the free Gemini tier, you might hit rate limits if you run the agents very frequently.

---
*Created by Jules (AI Assistant)*
