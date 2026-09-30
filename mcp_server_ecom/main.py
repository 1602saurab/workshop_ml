from fastapi import FastAPI 
from fastmcp import Client 
app = FastAPI(title="E-commerce Supprt Agent API") 

## URL OF REMOTE MCP SERVER 
MCP_SERVER_URL = "http://127.0.0.1:8001/mcp" 

@app.get("/order/{order_id}")
async def order_status(order_id:str):
    async with Client(MCP_SERVER_URL) as client:
        result = await client.call_tool("get_order_status" , {"order_id":order_id})
        return result.data if hasattr(result , "data") else result 

@app.get("/order/{order_id}/refund-check")
async def refund_check(order_id:str):
    async with Client(MCP_SERVER_URL) as client:
        result = await client.call_tool("check_refund_eligibility" , {"order_id":order_id}) 
        return result.data if hasattr(result , "data") else result 