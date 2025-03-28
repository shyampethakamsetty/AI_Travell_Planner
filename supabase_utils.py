import os
from typing import List, Dict, Any
from datetime import datetime
from supabase import create_client, Client
from prompts import TravelPreferences
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")

def save_trip(preferences: TravelPreferences, approved_suggestions: List[Dict[str, Any]], itinerary: str) -> str:
    """Save a trip to Supabase."""
    try:
        # Convert Pydantic model to dict and ensure all data is JSON serializable
        preferences_dict = preferences.dict()
        
        # Convert datetime to ISO format string
        created_at = datetime.utcnow().isoformat()
        
        # Prepare trip data with explicit type handling
        trip_data = {
            "created_at": created_at,
            "preferences": json.loads(json.dumps(preferences_dict)),  # Ensure JSON serialization
            "approved_suggestions": json.loads(json.dumps(approved_suggestions)),  # Ensure JSON serialization
            "itinerary": str(itinerary),  # Ensure string type
            "status": "active"
        }
        
        # Print the data being sent for debugging
        print("Sending data to Supabase:", json.dumps(trip_data, indent=2))
        
        # Insert data into Supabase
        result = supabase.table("trips").insert(trip_data).execute()
        
        if not result.data:
            raise Exception("No data returned from insert operation")
            
        return result.data[0]["id"]
        
    except json.JSONDecodeError as e:
        print(f"JSON serialization error: {str(e)}")
        raise
    except Exception as e:
        print(f"Error saving trip: {str(e)}")
        if hasattr(e, '_raw_error'):
            print(f"Raw error: {e._raw_error}")
        if hasattr(e, 'message'):
            print(f"Error message: {e.message}")
        if hasattr(e, 'code'):
            print(f"Error code: {e.code}")
        if hasattr(e, 'hint'):
            print(f"Error hint: {e.hint}")
        if hasattr(e, 'details'):
            print(f"Error details: {e.details}")
        raise

def get_trip_history() -> List[Dict[str, Any]]:
    """Get all trips from Supabase."""
    try:
        result = supabase.table("trips").select("*").order("created_at", desc=True).execute()
        return result.data
    except Exception as e:
        print(f"Error getting trip history: {str(e)}")
        if hasattr(e, '_raw_error'):
            print(f"Raw error: {e._raw_error}")
        raise

def get_trip_by_id(trip_id: str) -> Dict[str, Any]:
    """Get a specific trip by ID."""
    try:
        result = supabase.table("trips").select("*").eq("id", trip_id).single().execute()
        return result.data
    except Exception as e:
        print(f"Error getting trip by ID: {str(e)}")
        if hasattr(e, '_raw_error'):
            print(f"Raw error: {e._raw_error}")
        raise

def update_trip(trip_id: str, preferences: TravelPreferences, approved_suggestions: List[Dict[str, Any]], itinerary: str) -> None:
    """Update an existing trip."""
    try:
        # Convert Pydantic model to dict and ensure all data is JSON serializable
        preferences_dict = preferences.dict()
        
        trip_data = {
            "preferences": json.loads(json.dumps(preferences_dict)),  # Ensure JSON serialization
            "approved_suggestions": json.loads(json.dumps(approved_suggestions)),  # Ensure JSON serialization
            "itinerary": str(itinerary),  # Ensure string type
            "updated_at": datetime.utcnow().isoformat()
        }
        
        supabase.table("trips").update(trip_data).eq("id", trip_id).execute()
    except Exception as e:
        print(f"Error updating trip: {str(e)}")
        if hasattr(e, '_raw_error'):
            print(f"Raw error: {e._raw_error}")
        raise

def delete_trip(trip_id: str) -> None:
    """Delete a trip."""
    try:
        supabase.table("trips").delete().eq("id", trip_id).execute()
    except Exception as e:
        print(f"Error deleting trip: {str(e)}")
        if hasattr(e, '_raw_error'):
            print(f"Raw error: {e._raw_error}")
        raise 