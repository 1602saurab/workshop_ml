from fastmcp import FastMCP 
from database import get_doctor , get_patient 
# from src.logger import get_logger 
# logger = get_logger(__name__) 
# from src.exception import CustomException 
mcp = FastMCP("Sanjeevni Clinic MCP Server") 

##Tool-1: Doctor Schedule 
@mcp.tool() 
def doctor_details(name: str):
    doctor = get_doctor(name) 
    if not doctor:
        return{
            "success": False,
            "message": f"{name} not found..."
        }
    return{
        "success":True,
        "doctor": {
            "id": doctor[0],
            "name": doctor[1],
            "specialization": doctor[2],
            "timing": doctor[3] 
        }
    }


##Tool-2 ::: Patient Details 
@mcp.tool()
def patient_details(patient_id:int):
    patient = get_patient(patient_id) 
    if not patient:
        return{
            "success": False,
            "message": f"Patient {patient_id} not found..." 
        }
    return{
        "success": True,
        "patient": {
            "id": patient[0],
            "name": patient[1],
            "age": patient[2],
            "city": patient[3],
            "blood_group": patient[4] 
        }
    }
# print(logger.info("Tools setup for mcp server")) 

## Start mcp server 

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001) 