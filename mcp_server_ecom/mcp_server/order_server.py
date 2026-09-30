from fastmcp import FastMCP 
from datetime import datetime 

mcp = FastMCP("Order Management Server") 

ORDERS_DB = {
    "ORD1001": {
        "customer":"Rahul Sharma",
        "item": "Wireless Earbuds",
        "status": "Shipped",
        "order_date": "2026-07-28",
        "amount": 1999
    },
    "ORD1002": {
        "customer":"Priya Verma",
        "item": "Leptop Stand",
        "status": "Delivered",
        "order_date": "2026-07-22",
        "amount": 899
    },
}

@mcp.tool()
def get_order_status(order_id:str):
    order = ORDERS_DB.get(order_id.upper()) 
    if not order:
        return{"error":f"Order {order_id} not found...."} 
    return order 

@mcp.tool()
def check_refund_eligibility(order_id:str):
    order = ORDERS_DB.get(order_id.upper()) 
    if not order:
            return{"error":f"Order {order_id} not found...."} 
    order_date =  datetime.strptime(order['order_date'], "%Y-%m-%d")
    days_passed = (datetime(2026,9,30) - order_date).days 
    eligible = order['status'] == "Delivered" and days_passed <=7 
    return{
         "order_id":order_id.upper(),
         "eligible":eligible,
         "days_since_order":days_passed,
         "reason": "Delivered with in 7 days" if eligible else "Not eligible" 
    }

if __name__ =="__main__":
     mcp.run(transport="http", host="0.0.0.0" , port=8001) 