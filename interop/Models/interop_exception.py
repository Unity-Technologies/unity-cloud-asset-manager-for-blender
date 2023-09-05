from .interop_model_base import Interop_Model_Base

class Interop_Exception(Interop_Model_Base, Exception):
    def __init__(self):
        self.ExceptionType = None
        self.Message = None
        self.StackTraceString = None

    def load_from_json(self, exception_json: dict):
        self.ExceptionType = exception_json.get("ClassName")
        self.Message = exception_json.get("Message")
        self.StackTraceString = exception_json.get("StackTraceString")
        super().__init__(self.Message)
        
    def __str__(self):
        return f"ExceptionType: {self.ExceptionType} \n Message: {self.Message} \n StackTraceString: {self.StackTraceString}"
