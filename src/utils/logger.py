from logging import getLogger

class Logger:
    def __init__(self):
        self.log = getLogger("uvicorn")
    
    def info(self, message: str):
        self.log.info(message)
        
    def warn(self, message: str):
        self.log.warning(message)
        
    def error(self, message: str):
        self.log.error(message)