import sys 
from src.logger import get_logger 
logger = get_logger(__name__) 

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info() 
    file_name = exc_tb.tb_frame.f_code.co_filename 
    line_number = exc_tb.tb_lineno 
    error_message = (
        f"Error occured in python script: [{file_name}]" 
        f"at line number: [{line_number}]" 
        f"with error message: [{str(error)}]" 
    )
    return error_message 

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message) 
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        logger.error(self.error_message) 

    def __str__(self):
        return self.error_message 