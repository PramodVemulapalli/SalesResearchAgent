import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from saviynt import saviyntHooks

async def main():

    # Register the Agent in Saviynt
    agent_identity = saviyntHooks.create_identity(agentName = 'sales-research-agent')

    // connect to an MCP Server
    client = MultiServerMCPClient(
        {
            "my_mcp_server": {
                "transport": "http",
                "url": "http://localhost:8000/mcp",  
            }
        }
    )
    
    # Load/convert MCP tools -> LangChain tools
    tools = await client.get_tools()
    
    # Create a LangChain agent that can call those tools
    agent = create_agent("openai:gpt-4.1", tools)
    
    # Run it
    result = await agent.ainvoke(
        {"messages": "Use the MCP tools to help me to generate a sales research report"}
    )
    print(result)

asyncio.run(main())
