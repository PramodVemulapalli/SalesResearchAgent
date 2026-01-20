import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from saviynt import saviyntHooks

async def main():
    # Register the Agent Identity in Saviynt
    agent_identity = saviyntHooks.create_identity(agentName='sales-research-agent')

    # Add Salesforce tools to the agent and get the Saviynt gateway URL
    saviynt_gateway_url = saviyntHooks.add_tools_to_agent(
        agent=agent_identity,
        tools=["salesforce_reports_tool"]
    )

    # Connect to MCP Server via Saviynt gateway
    client = MultiServerMCPClient(
        {
            "my_mcp_server": {
                "transport": "http",
                "url": saviynt_gateway_url,
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
