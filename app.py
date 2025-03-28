import streamlit as st
from typing import List, Dict, Any
import json
from datetime import datetime
from prompts import TravelPreferences, INITIAL_SYSTEM_PROMPT, REFINEMENT_SYSTEM_PROMPT
from utils import (
    get_ai_response,
    generate_travel_suggestions,
    create_itinerary,
    validate_dates
)
from supabase_utils import (
    save_trip,
    get_trip_history,
    get_trip_by_id,
    update_trip,
    delete_trip
)
from images import (
    PLANE_ICON,
    CALENDAR_ICON,
    LOCATION_ICON,
    CHECK_ICON,
    get_icon_html
)

# Set page config
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "preferences" not in st.session_state:
    st.session_state.preferences = None
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "approved_suggestions" not in st.session_state:
    st.session_state.approved_suggestions = []
if "current_trip_id" not in st.session_state:
    st.session_state.current_trip_id = None
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None

def add_navigation_buttons():
    """Add navigation buttons to the bottom of the page."""
    st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
    
    # Use equal column widths for even spacing
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.session_state.step > 1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step -= 1
                st.rerun()
    
    with col2:
        if st.button("🔄 Start Over", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    with col3:
        if st.session_state.step == 3:
            if st.button("Next →", use_container_width=True):
                if not st.session_state.approved_suggestions:
                    st.warning("Please select at least one activity before generating the itinerary!")
                else:
                    st.session_state.step += 1
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_progress():
    """Show progress bar for the current step."""
    steps = ["Preferences", "Refinement", "Activities", "Itinerary"]
    current_step = st.session_state.step - 1
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    for i, step in enumerate(steps):
        step_class = "progress-step active" if i <= current_step else "progress-step"
        check_icon = get_icon_html(CHECK_ICON, "#2563eb") if i <= current_step else f"{i + 1}"
        st.markdown(
            f'''
            <div class="{step_class}">
                <div class="step-number">{check_icon}</div>
                <div class="step-label">{step}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

def show_trip_history():
    """Show trip history in the sidebar."""
    st.sidebar.title("Trip History")
    
    try:
        trips = get_trip_history()
        if trips:
            for trip in trips:
                with st.sidebar.expander(f"Trip to {trip['preferences']['destination']}"):
                    st.write(f"Created: {datetime.fromisoformat(trip['created_at']).strftime('%Y-%m-%d %H:%M')}")
                    if st.button("Load Trip", key=f"load_{trip['id']}"):
                        load_trip(trip)
                    if st.button("Delete Trip", key=f"delete_{trip['id']}"):
                        delete_trip(trip['id'])
                        st.rerun()
        else:
            st.sidebar.info("No trips saved yet.")
    except Exception as e:
        st.sidebar.error(f"Error loading trip history: {str(e)}")

def load_trip(trip_data: Dict[str, Any]):
    """Load a trip from history."""
    st.session_state.preferences = TravelPreferences(**trip_data['preferences'])
    st.session_state.approved_suggestions = trip_data['approved_suggestions']
    st.session_state.itinerary = trip_data['itinerary']
    st.session_state.current_trip_id = trip_data['id']
    st.session_state.step = 4
    st.rerun()

def get_index_safely(value: str, options: List[str]) -> int:
    """Safely get the index of a value in a list of options."""
    try:
        return options.index(value)
    except (ValueError, AttributeError):
        return 0

def main():
    # Load custom CSS
    load_css()
    
    # Main header with gradient background
    st.markdown(
        """
        <div class="main-header">
            <div class="header-content">
                <div class="header-title">
                    <h1>✈️ AI Travel Planner</h1>
                    <p>Let's create your perfect travel itinerary!</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Show progress
    show_progress()
    
    # Container for main content
    with st.container():
        # Show trip history in sidebar
        show_trip_history()

        # Step 1: Initial Preferences
        if st.session_state.step == 1:
            st.header("Tell us about your travel preferences")
            
            with st.form("initial_preferences"):
                st.markdown('<div class="form-container">', unsafe_allow_html=True)
                
                budget = st.selectbox(
                    "What's your budget range?",
                    ["budget", "moderate", "luxury"],
                    index=get_index_safely(st.session_state.preferences.budget if st.session_state.preferences else None, ["budget", "moderate", "luxury"])
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input(
                        "Start Date",
                        value=st.session_state.preferences.duration.split(" to ")[0] if st.session_state.preferences else None
                    )
                with col2:
                    end_date = st.date_input(
                        "End Date",
                        value=st.session_state.preferences.duration.split(" to ")[1] if st.session_state.preferences else None
                    )
                
                destination = st.text_input(
                    "Destination",
                    value=st.session_state.preferences.destination if st.session_state.preferences else ""
                )
                starting_location = st.text_input(
                    "Starting Location",
                    value=st.session_state.preferences.starting_location if st.session_state.preferences else ""
                )
                purpose = st.selectbox(
                    "Purpose of Travel",
                    ["leisure", "business", "adventure", "cultural", "other"],
                    index=get_index_safely(st.session_state.preferences.purpose if st.session_state.preferences else None, ["leisure", "business", "adventure", "cultural", "other"])
                )
                
                preferences = st.multiselect(
                    "What are your interests?",
                    ["culture", "nature", "food", "shopping", "adventure", "relaxation", "history"],
                    default=st.session_state.preferences.preferences if st.session_state.preferences else []
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Form submit button that also handles navigation
                if st.form_submit_button("Next →", use_container_width=True):
                    if not validate_dates(str(start_date), str(end_date)):
                        st.error("End date must be after start date!")
                    elif not destination or not starting_location:
                        st.error("Please fill in all required fields!")
                    else:
                        st.session_state.preferences = TravelPreferences(
                            budget=budget,
                            duration=f"{start_date} to {end_date}",
                            destination=destination,
                            starting_location=starting_location,
                            purpose=purpose,
                            preferences=preferences
                        )
                        st.session_state.step += 1
                        st.rerun()

        # Step 2: Refinement
        elif st.session_state.step == 2:
            st.header("Let's refine your preferences")
            
            with st.form("refinement"):
                st.markdown('<div class="form-container">', unsafe_allow_html=True)
                
                dietary_preferences = st.multiselect(
                    "Any dietary preferences?",
                    ["vegetarian", "vegan", "halal", "kosher", "none"],
                    default=st.session_state.preferences.dietary_preferences.split(", ") if st.session_state.preferences and st.session_state.preferences.dietary_preferences else []
                )
                
                mobility_concerns = st.selectbox(
                    "Any mobility concerns?",
                    ["none", "limited walking", "wheelchair accessible", "other"],
                    index=get_index_safely(st.session_state.preferences.mobility_concerns if st.session_state.preferences else None, ["none", "limited walking", "wheelchair accessible", "other"])
                )
                
                accommodation_preferences = st.multiselect(
                    "Accommodation preferences",
                    ["budget", "central location", "luxury", "quiet", "family-friendly"],
                    default=st.session_state.preferences.accommodation_preferences.split(", ") if st.session_state.preferences and st.session_state.preferences.accommodation_preferences else []
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Form submit button that also handles navigation
                if st.form_submit_button("Next →", use_container_width=True):
                    st.session_state.preferences.dietary_preferences = ", ".join(dietary_preferences)
                    st.session_state.preferences.mobility_concerns = mobility_concerns
                    st.session_state.preferences.accommodation_preferences = ", ".join(accommodation_preferences)
                    
                    st.session_state.suggestions = generate_travel_suggestions(st.session_state.preferences)
                    st.session_state.step += 1
                    st.rerun()

        # Step 3: Activity Selection
        elif st.session_state.step == 3:
            st.header("Select activities for your itinerary")
            
            st.write("Here are some suggested activities based on your preferences:")
            
            for idx, suggestion in enumerate(st.session_state.suggestions):
                with st.expander(suggestion["name"]):
                    st.write(suggestion["description"])
                    if st.button("Add to Itinerary", key=f"add_{idx}_{suggestion['name']}"):
                        if suggestion not in st.session_state.approved_suggestions:
                            st.session_state.approved_suggestions.append(suggestion)
                            st.success(f"Added {suggestion['name']} to your itinerary!")

        # Step 4: Final Itinerary
        elif st.session_state.step == 4:
            st.header("Your Personalized Travel Itinerary")
            
            if not st.session_state.itinerary:
                with st.spinner("Generating your detailed itinerary..."):
                    st.session_state.itinerary = create_itinerary(
                        st.session_state.preferences,
                        st.session_state.approved_suggestions
                    )
            
            st.markdown(
                f'<div class="itinerary-container">{st.session_state.itinerary}</div>',
                unsafe_allow_html=True
            )
            
            # Save or Update Trip
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.current_trip_id:
                    if st.button("Update Trip", use_container_width=True):
                        update_trip(
                            st.session_state.current_trip_id,
                            st.session_state.preferences,
                            st.session_state.approved_suggestions,
                            st.session_state.itinerary
                        )
                        st.success("Trip updated successfully!")
                else:
                    if st.button("Save Trip", use_container_width=True):
                        trip_id = save_trip(
                            st.session_state.preferences,
                            st.session_state.approved_suggestions,
                            st.session_state.itinerary
                        )
                        st.session_state.current_trip_id = trip_id
                        st.success("Trip saved successfully!")
            
            # Add buttons to modify specific aspects
            st.markdown(
                '''
                <div class="modification-section">
                    <h3>Want to modify something?</h3>
                    <div class="modification-buttons">
                ''',
                unsafe_allow_html=True
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Modify Basic Preferences", use_container_width=True):
                    st.session_state.step = 1
                    st.rerun()
            with col2:
                if st.button("Modify Additional Preferences", use_container_width=True):
                    st.session_state.step = 2
                    st.rerun()
            with col3:
                if st.button("Modify Activities", use_container_width=True):
                    st.session_state.step = 3
                    st.rerun()
            
            st.markdown('</div></div>', unsafe_allow_html=True)

    # Add navigation buttons at the bottom of the page
    add_navigation_buttons()

if __name__ == "__main__":
    main() 