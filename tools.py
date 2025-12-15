import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_tools():
    client = MultiServerMCPClient(
        {
            "budget": {
                "url": "http://localhost:3333/sse",
                "transport": "sse",
            }
        }
    )
    return await client.get_tools()

if __name__ == "__main__":
    tools = asyncio.run(get_tools())
    print(f"Loaded {len(tools)} tools")


