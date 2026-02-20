import asyncio
import sys
import os
from dotenv import load_dotenv
import helping as hp
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage
#from langchain.agents import create_openai_tools_agent
#from langchain.agents import AgentExecutor
#from langchain.prompts import ChatPromptTemplate

load_dotenv()

# MCP Server Config
SERVERS = {
    "Calculator Server": {
        "transport": "stdio",
        "command": sys.executable,
        "args": [r"D:\Expense_Trcaker_MCP_Server\main.py"],
    }
}

async def run_agent(prompt):
    # Connect to MCP
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()

    print("Loaded tools:")
  
    for tool in tools:
        print(tool.name)

    named_tools = {tool.name: tool for tool in tools}

    # Initialize Groq model
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )
    llm_withot_tools= llm
    llm_with_tools= llm.bind_tools(tools)
    prompt= prompt#" What is the multipcation of 2 and 8 calculator tools"
    reponse= await llm_with_tools.ainvoke(prompt)
    print("response ,",reponse.content)
    selected_tool_name, selected_tool_arg= hp.extract_tool_call(reponse.content)
    print(selected_tool_name, selected_tool_arg)
    if selected_tool_name:
        print("inside tool calling loops")
        result= await named_tools[selected_tool_name].ainvoke(selected_tool_arg)
        tools_result= str(result[0]['text'])

        tool_messages= ToolMessage(content=tools_result, tool_call_id= selected_tool_name)

        final_reponse= await llm_with_tools.ainvoke([prompt, reponse, tool_messages])
        print("final response ,", final_reponse.content)
        return final_reponse.content
    else:
        final_reponse= await llm_withot_tools.ainvoke(prompt)
        print("final response ,", final_reponse.content)
        return final_reponse.content

if __name__ == "__main__":
    asyncio.run(main())