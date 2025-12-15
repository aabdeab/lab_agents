import asyncio
import sys

# 1. Imports
# We use ChatOllama instead of ChatOpenAI
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

async def run_agent():
    print("🤖 Initializing Ollama Agent (Llama 3.2)...")
    
    # 2. Setup the LLM (Ollama)
    # We use 'llama3.2' which supports tool calling natively
    llm = ChatOllama(
        model="llama3.2", 
        temperature=0
    )

    # 3. Connect to the Budget Server
    # Ensure budget_mcp_server.py is running in another terminal!
    client = MultiServerMCPClient({
        "budget": {
            "url": "http://localhost:3333/sse",
            "transport": "sse",
        }
    })

    print("🔗 Connecting to Budget Server...")
    try:
        tools = await client.get_tools()
        print(f"✅ Connected! Found tools: {[t.name for t in tools]}")
    except Exception as e:
        print(f"❌ Connection Failed. Is budget_mcp_server.py running? Error: {e}")
        return

    # 4. Create the Agent
    agent_executor = create_react_agent(llm, tools)

    # 5. Define the User Query
    query = "Plan a 5-day trip to Barcelona with an estimated budget."
    print(f"\n📩 User Request: '{query}'\n")

    # 6. Run the Agent
    print("⏳ Thinking... (Local models can be slightly slower than cloud)")
    try:
        async for event in agent_executor.astream({"messages": [HumanMessage(content=query)]}, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()
    except Exception as e:
        print(f"⚠️ Error during execution: {e}")
        print("Tip: Ensure you ran 'ollama pull llama3.2' successfully.")

    # Cleanup
    await client.__aexit__(None, None, None)

if __name__ == "__main__":
    # Fix for Windows asyncio loop issues
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(run_agent())