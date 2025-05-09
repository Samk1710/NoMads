from .base_agent import BaseAgent
from services.serpapi_service import SerpAPIClient
from typing import Dict, List
import os
from datetime import datetime

class HotelAgent(BaseAgent):
    def execute(self, params: Dict) -> List[Dict]:
        """
        params: {
            "destination": "Vilnius",
            "checkin": "2025-04-26",
            "checkout": "2025-05-03",
            "adults": 1,
            "rooms": 1,
            "price_range": "mid-range"
        }
        """
        try:
            client = SerpAPIClient()
            results = client.get_hotels({
                "engine": "google_hotels",
                "q": f"Hotels in {params['destination']}",
                "checkin_date": params["checkin"],
                "checkout_date": params["checkout"],
                "currency": "INR",
                "adults": params["adults"],
                "rooms": params["rooms"],
                "price": self._map_price_range(params.get("price_range", "mid-range"))
            })
            
            return self._parse_hotels(results.get("properties", []))
        
        except Exception as e:
            return self.handle_error(e, params)

    def _map_price_range(self, range: str) -> str:
        ranges = {
            "budget": "10,5000",
            "mid-range": "5001,15000",
            "luxury": "15001,100000"
        }
        return ranges.get(range.lower(), "5001,15000")

    def _parse_hotels(self, hotels: List) -> List[Dict]:
        parsed = []
        for hotel in hotels[:5]:  # Top 5 options
            details = {
                "name": hotel["name"],
                "price": hotel.get("price", "N/A"),
                "rating": hotel.get("rating", "N/A"),
                "reviews": hotel.get("reviews", "N/A"),
                "amenities": ", ".join(hotel.get("amenities", [])[:5]),
                "thumbnail": hotel.get("thumbnail"),
                "link": hotel.get("link")
            }
            parsed.append(details)
        return parsed