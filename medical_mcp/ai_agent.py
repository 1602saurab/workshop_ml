import json
import os

from dotenv import load_dotenv
from groq import Groq
from fastmcp import Client


# Load .env
load_dotenv()


# Configuration
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

MCP_SERVER_URL = os.getenv(
    "MCP_SERVER_URL",
    "http://127.0.0.1:8001/mcp"
)


# Groq client
groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ------------------------------------------------
# AI Agent
# ------------------------------------------------

async def ask_agent(question: str):

    # Connect to MCP server
    async with Client(MCP_SERVER_URL) as client:

        # Get available MCP tools
        tools = await client.list_tools()

        # Convert MCP tools to Groq format
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

        # Conversation
        messages = [
            {
                "role": "system",
                "content": """
You are a Clinic AI Assistant.

Use MCP tools when the user asks for
doctor or patient information.

Never invent database information.

If a tool can answer the question,
use that tool.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]

        # First Groq call
        response = groq.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tools=groq_tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # If no tool required
        if not message.tool_calls:

            return {
                "answer": message.content,
                "tools_used": []
            }

        # Add assistant tool-call message
        messages.append(
            message.model_dump(
                exclude_none=True
            )
        )

        tools_used = []

        # Execute MCP tools
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            tools_used.append(tool_name)

            # MCP tool execution
            result = await client.call_tool(
                tool_name,
                arguments
            )

            # Get tool result
            if hasattr(result, "data"):

                tool_result = result.data

            else:

                tool_result = str(result)

            # Send MCP result to Groq
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(
                        tool_result,
                        default=str
                    )
                }
            )

        # Final Groq call
        final_response = groq.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tool_choice="none"
        )

        return {
            "answer": final_response
            .choices[0]
            .message
            .content,

            "tools_used": tools_used
        }