import streamlit as st
import asyncio
import sys

# Import the function we just created
from agent import get_agent_response

# Fix for Windows Asyncio loop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 1. UI Layout
st.title("✈️ Agentic Travel Planner")
st.caption("Powered by Llama 3.2, LangGraph & MCP")

# 2. User Input
with st.form("trip_form"):
    text = st.text_area("Describe your trip:", "Plan a 5-day trip to Barcelona with a budget estimate.")
    submitted = st.form_submit_button("Plan My Trip")

# 3. Execution Logic
if submitted:
    with st.spinner("Agent is thinking... (Connecting to Budget Tools)"):
        # Run the async agent inside Streamlit
        response = asyncio.run(get_agent_response(text))
        
        # 4. Display Result
        st.success("Plan Ready!")
        st.markdown(response)