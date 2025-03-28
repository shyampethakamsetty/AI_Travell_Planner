from typing import List, Dict, Any
from tavily import TavilyClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_travel_attractions(destination: str, preferences: List[str]) -> List[Dict[str, Any]]:
    """
    Search for travel attractions using Tavily API.
    """
    try:
        # Construct search query based on preferences
        query = f"Best {', '.join(preferences)} attractions in {destination}"
        
        # Perform search
        search_result = tavily_client.search(
            query=query,
            search_depth="advanced",
            include_answer=True,
            include_domains=["tripadvisor.com", "lonelyplanet.com", "travelandleisure.com"]
        )
        
        # Process and format results
        attractions = []
        for result in search_result.get("results", []):
            attraction = {
                "name": result.get("title", ""),
                "description": result.get("content", ""),
                "url": result.get("url", ""),
                "source": result.get("source", ""),
                "relevance_score": result.get("score", 0)
            }
            attractions.append(attraction)
        
        return attractions
    
    except Exception as e:
        print(f"Error searching travel attractions: {str(e)}")
        return []

def get_seasonal_info(destination: str, travel_dates: str) -> Dict[str, Any]:
    """
    Get seasonal information for the destination.
    """
    try:
        query = f"Best time to visit {destination}, weather, climate, and seasonal events"
        
        search_result = tavily_client.search(
            query=query,
            search_depth="advanced",
            include_answer=True,
            include_domains=["weather.com", "tripadvisor.com", "lonelyplanet.com"]
        )
        
        return {
            "weather_info": search_result.get("answer", ""),
            "seasonal_events": search_result.get("results", [])
        }
    
    except Exception as e:
        print(f"Error getting seasonal information: {str(e)}")
        return {} 