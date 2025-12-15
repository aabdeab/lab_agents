import asyncio
import sys
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_agent_response(user_query: str):
    """
    Connects to the server, runs the agent, and returns the text response.
    """
    # 1. Setup Llama 3.2
    llm = ChatOllama(model="llama3.2:1b", temperature=0)

    # 2. Connect to Budget Server (Standard connection, no context manager)
    client = MultiServerMCPClient({
        "budget": {
            "url": "http://localhost:3333/sse",
            "transport": "sse",
        }
    })

    try:
        # 3. Get Tools & Create Agent
        tools = await client.get_tools()
        agent_executor = create_react_agent(llm, tools)

        # 4. Run Agent
        final_response = "Error: No response generated."
        
        # We stream the output to get the final message
        async for event in agent_executor.astream(
            {"messages": [HumanMessage(content=user_query)]}, 
            stream_mode="values"
        ):
            if "messages" in event:
                # Capture the content of the last message
                final_response = event["messages"][-1].content
        
        return final_response

    except Exception as e:
        return f"Error: {str(e)}"

# Keep this so you can still run 'python agent.py' to test locally
if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Test run
    print(asyncio.run(get_agent_response("Plan a trip to Paris")))