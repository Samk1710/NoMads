import os
import requests

class SerpAPIClient:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")
        self.base_url = "https://serpapi.com/search"

    def _make_request(self, params):
        params["api_key"] = self.api_key
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_flights(self, params):
        return self._make_request(params)

    def get_hotels(self, params):
        return self._make_request(params)

    def get_activities(self, params):
        return self._make_request(params)
