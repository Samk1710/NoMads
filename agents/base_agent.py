from agno import Agent
import logging
from typing import Dict, Any

class BaseAgent(Agent):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None):
        self.logger.error(f"Agent error: {str(error)}", extra=context)
        return {"error": str(error), "context": context}