import os
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from prompts import TravelPreferences, INITIAL_SYSTEM_PROMPT, REFINEMENT_SYSTEM_PROMPT, ACTIVITY_SUGGESTION_PROMPT, ITINERARY_GENERATION_PROMPT

# Load environment variables
load_dotenv()

# Set Azure OpenAI environment variables
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_API_VERSION"] = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize clients
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Initialize LangChain with Azure OpenAI
llm = AzureChatOpenAI(
    deployment_name=model_name,
    temperature=0.7,
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def format_preferences(preferences: TravelPreferences) -> str:
    """Format travel preferences into a structured string for prompts."""
    return f"""
Travel Preferences:
- Budget: {preferences.budget}
- Duration: {preferences.duration}
- Destination: {preferences.destination}
- Starting Location: {preferences.starting_location}
- Purpose: {preferences.purpose}
- General Preferences: {', '.join(preferences.preferences)}
- Dietary Preferences: {preferences.dietary_preferences or 'Not specified'}
- Mobility Concerns: {preferences.mobility_concerns or 'Not specified'}
- Accommodation Preferences: {preferences.accommodation_preferences or 'Not specified'}
"""

def search_travel_info(query: str) -> List[Dict[str, Any]]:
    """Search for travel-related information using Tavily."""
    search_result = tavily_client.search(
        query=query,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        max_results=5
    )
    return search_result.get("results", [])

def get_ai_response(system_prompt: str, user_input: str) -> str:
    """Get AI response using LangChain."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.invoke({"input": user_input})
    return response["text"]

def validate_dates(start_date: str, end_date: str) -> bool:
    """Validate travel dates."""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    except ValueError:
        return False

def format_budget_range(budget: str) -> Dict[str, float]:
    """Convert budget description to numerical range."""
    budget_ranges = {
        "budget": {"min": 0, "max": 100},
        "moderate": {"min": 100, "max": 300},
        "luxury": {"min": 300, "max": float("inf")}
    }
    return budget_ranges.get(budget.lower(), {"min": 0, "max": float("inf")})

def generate_travel_suggestions(preferences: TravelPreferences) -> List[Dict[str, Any]]:
    """Generate travel suggestions based on preferences."""
    # Search for destination information
    destination_query = f"top attractions and activities in {preferences.destination}"
    search_results = search_travel_info(destination_query)
    
    # Filter and format suggestions based on preferences
    suggestions = []
    for result in search_results:
        suggestion = {
            "name": result.get("title", ""),
            "description": result.get("content", ""),
            "source": result.get("url", ""),
            "relevance_score": 0.0  # Can be implemented with more sophisticated scoring
        }
        suggestions.append(suggestion)
    
    return suggestions

def create_itinerary(preferences: TravelPreferences, approved_suggestions: List[Dict[str, Any]]) -> str:
    """Create a detailed itinerary based on preferences and approved suggestions."""
    # Format preferences for the prompt
    preferences_str = format_preferences(preferences)
    suggestions_str = "\n".join([f"- {s['name']}: {s['description']}" for s in approved_suggestions])
    
    # Generate itinerary using AI
    prompt_input = f"""
{preferences_str}

Approved Activities:
{suggestions_str}

Please create a detailed day-by-day itinerary based on the above information.
"""
    
    return get_ai_response(ITINERARY_GENERATION_PROMPT, prompt_input)

def get_index_safely(value: str, options: List[str]) -> int:
    """Safely get the index of a value in a list of options."""
    try:
        return options.index(value)
    except (ValueError, AttributeError):
        return 0 