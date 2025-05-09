from .base_agent import BaseAgent
from services.serpapi_service import SerpAPIClient
from typing import Dict, List
import os
from datetime import datetime

class FlightAgent(BaseAgent):
    def execute(self, params: Dict) -> List[Dict]:
        """
        params: {
            "origin": "BLR",
            "destination": "VNO",
            "departure_date": "2025-04-26",
            "return_date": "2025-05-03",
            "adults": 1,
            "class": "economy"
        }
        """
        try:
            client = SerpAPIClient()
            results = client.get_flights({
                "engine": "google_flights",
                "departure_id": params["origin"],
                "arrival_id": params["destination"],
                "outbound_date": params["departure_date"],
                "return_date": params.get("return_date"),
                "currency": "INR",
                "hl": "en",
                "adults": params.get("adults", 1),
                "travel_class": params.get("class", "economy")
            })
            
            return self._parse_flights(results.get("best_flights", []))
        
        except Exception as e:
            return self.handle_error(e, params)

    def _parse_flights(self, flights: List) -> List[Dict]:
        parsed = []
        for flight in flights[:3]:  # Top 3 options
            details = {
                "airlines": " ➔ ".join([s["airline"] for s in flight["steps"]]),
                "price": flight["price"],
                "duration": flight["duration"],
                "stops": flight["stops"],
                "carbon_emissions": flight.get("carbon_emissions", "N/A"),
                "departure_time": flight["departure_airport"]["time"],
                "arrival_time": flight["arrival_airport"]["time"]
            }
            parsed.append(details)
        return parsed