from .base_agent import BaseAgent
from services.serpapi_service import SerpAPIClient
from typing import Dict, List

class ActivityAgent(BaseAgent):
    def execute(self, params: Dict) -> Dict[str, List]:
        """
        params: {
            "destination": "Vilnius",
            "days": 7,
            "interests": ["historical", "cultural"]
        }
        """
        try:
            client = SerpAPIClient()
            results = client.get_activities({
                "engine": "google_events",
                "q": f"Things to do in {params['destination']}",
                "hl": "en",
                "gl": "lt"
            })
            
            return {
                "historical": self._filter_activities(results, "historical"),
                "cultural": self._filter_activities(results, "cultural"),
                "nature": self._filter_activities(results, "nature"),
                "all": results.get("events", [])
            }
        
        except Exception as e:
            return self.handle_error(e, params)

    def _filter_activities(self, data: Dict, category: str) -> List:
        return [item for item in data.get("events", [])
                if category in item.get("category", "").lower()]