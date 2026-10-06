from fastapi import FastAPI 
from pydantic import BaseModel 
from database import init_db 
from ai_agent import ask_agent 

app = FastAPI(
    title="Medical Clinic MCP Server", version="1.0.0"
)

##Request Model 
class ChatRequest(BaseModel):
    message: str 

## startup the db 
@app.on_event("startup")
def startup():
    init_db() 

##Route 
@app.get("/")
def root():
    return{
        "message": "Clinic AI Assitant is running..."
    }

##Chat 
@app.post("/chat") 
async def chat(request: ChatRequest):
    result = await ask_agent(request.message) 
    return result 