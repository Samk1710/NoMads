from .base_agent import BaseAgent
from services.gemini_service import GeminiClient
from typing import Dict
import textwrap

class ItineraryAgent(BaseAgent):
    def execute(self, context: Dict) -> str:
        """
        context: {
            "flights": [...],
            "hotels": [...],
            "activities": {...},
            "params": {...}
        }
        """
        try:
            client = GeminiClient()
            prompt = self._create_prompt(context)
            response = client.generate_itinerary(prompt)
            return self._format_response(response)
        
        except Exception as e:
            return self.handle_error(e, context)

    def _create_prompt(self, context: Dict) -> str:
        return textwrap.dedent(f"""
        Generate a detailed travel itinerary with this structure:
        
        # Travel Plan to {context['params']['destination']}
        ## Trip Summary
        - **Duration:** {context['params']['days']} days
        - **Travelers:** {context['params'].get('adults', 1)} adults
        
        ## Flight Options
        {self._format_flights(context['flights'])}
        
        ## Hotel Options
        {self._format_hotels(context['hotels'])}
        
        ## Daily Itinerary
        Create {context['params']['days']} days with activities from these categories:
        {self._format_activities(context['activities'])}
        
        Include practical transportation info and safety tips. Use markdown formatting.
        """)

    def _format_flights(self, flights: List) -> str:
        return "\n".join([f"- {f['airlines']} ({f['duration']}) - ₹{f['price']}"
                        for f in flights])

    def _format_hotels(self, hotels: List) -> str:
        return "\n".join([f"- {h['name']} - ₹{h['price']}/night"
                        for h in hotels])

    def _format_activities(self, activities: Dict) -> str:
        return "\n".join([f"- {cat.capitalize()}: {len(items)} options"
                        for cat, items in activities.items()])

    def _format_response(self, text: str) -> str:
        return text.replace("•", "-")  # Standardize list markers