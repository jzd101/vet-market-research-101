import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

# Add the project root to path so we can import agent.graph
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.graph import run_agent_workflow

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Vet Market Agent Team", layout="wide")

st.title("🐶 AI Vet Market Research Team")
st.markdown("""
This application demonstrates a **LangGraph** workflow integrated with an **MCP (Model Context Protocol)** server.
The team consists of three agents:
1.  **Researcher:** Connects to an MCP Tool to fetch market data.
2.  **Analyst:** Summarizes the findings.
3.  **Strategist:** Proposes a business model.
""")

# Check for API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.warning("⚠️ `GOOGLE_API_KEY` not found in environment variables.")
    user_key = st.text_input("Enter your Google Gemini API Key:", type="password")
    if user_key:
        os.environ["GOOGLE_API_KEY"] = user_key
        st.success("API Key set! You can now run the agents.")
    else:
        st.stop()

if st.button("🚀 Start Research Workflow"):
    with st.spinner("Agents are working... (Researcher -> Analyst -> Strategist)"):
        try:
            # Run the async graph in a sync streamlit app
            result = asyncio.run(run_agent_workflow())

            st.success("Workflow Complete!")

            # Use Tabs for different outputs
            tab1, tab2, tab3 = st.tabs(["📊 Analyst Report", "💡 Business Strategy", "🔍 Raw Research Data"])

            with tab1:
                st.header("Market Analysis Report")
                st.markdown(result.get("analyst_report", "No report generated."))

            with tab2:
                st.header("Business Strategy Model")
                st.markdown(result.get("business_strategy", "No strategy generated."))

            with tab3:
                st.subheader("Raw Data from MCP Server")
                st.text(result.get("research_data", "No data."))

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Check if the MCP server script is accessible and requirements are installed.")
