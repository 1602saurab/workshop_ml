import json 
import os 
from dotenv import load_dotenv 
from groq import Groq 
from fastmcp import Client  

load_dotenv() 

##Configuation 
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b" 
)

MCP_SERVER_URL = os.getenv(

    "MCP_SERVER_URL",
    "http://127.0.0.1:8001/mcp"
)

# Groq Client 
groq = Groq(
    api_key = os.getenv("GROQ_API_KEY") 
)

# AI Agent 

async def ask_agent(question:str):
    async with Client(MCP_SERVER_URL) as client:
        tools = await client.list_tools() 

        ##Convert mcp tools to groq format 
        groq_tools = [] 
        for tool in tools:
            groq_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema
                    }
                }
            )

            ##Conversation 
            messages = [
                {
                    "role": "system",
                    "content": """
You are a clinic AI Assistant. 
use MCP tools when the user asks for doctor or patient information. 
If a tool can answer the question, use that tool. 
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ]

            ##groq llm calling 
            response = groq.chat.completions.create(
                model=GROQ_MODEL,
                messages = messages,
                tools = groq_tools,
                tool_choice = "auto"
            )

            message = response.choices[0].message 

            ## if not  toool required 
            if not message.tool_calls:
                return{
                    "answer": message.content,
                    "tols_used": []
                }

            ## Add assistant tool-call message 
            messages.append(
                message.model_dump(
                    exclude_none = True
                )
            )

            tools_used = [] 
            ## Execute our mcp tools 
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name 
                arguments = json.loads(
                    tool_call.function.arguments 
                )
                result  = await client.call_tool(
                    tool_name,
                    arguments
                )
                if hasattr(result , "data"):
                    tool_result = result.data
                else:
                    tool_result = str(result) 

                ### Send MCP result to Groq 
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": json.dumps(
                            tool_result,
                            default= str
                        )
                    }
                )

                ## Final Groq call 
                final_response = groq.chat.completions.create(
                    model = GROQ_MODEL,
                    messages = messages,
                    tool_choices = "none"
                )