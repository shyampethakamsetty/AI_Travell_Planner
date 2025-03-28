# AI Travel Planner 🌍✈️

A sophisticated travel planning application powered by AI that helps users create personalized travel itineraries. Built with Streamlit and featuring a modern, elegant dark theme interface.

## Features

### 1. Interactive Travel Planning Process
- **Step-by-Step Guidance**: Four-stage planning process with visual progress tracking
- **Smart Form Validation**: Real-time validation of dates and required fields
- **Dynamic UI**: Responsive design that works on both desktop and mobile devices

### 2. Comprehensive Travel Preferences
- Budget range selection (budget/moderate/luxury)
- Travel dates with date picker
- Destination and starting location input
- Purpose of travel selection
- Multiple interest selection
  - Culture
  - Nature
  - Food
  - Shopping
  - Adventure
  - Relaxation
  - History

### 3. Advanced Preference Refinement
- Dietary preferences
- Mobility considerations
- Accommodation preferences
- Activity suggestions based on preferences

### 4. Trip Management
- Save and load trips
- View trip history
- Update existing trips
- Delete saved trips

### 5. Personalized Itinerary Generation
- AI-powered activity suggestions
- Custom itinerary creation
- Local customs and etiquette tips
- Emergency contact information
- Transportation recommendations
- Packing list suggestions

## Technical Features

### Modern UI Components
- Gradient backgrounds and animations
- Progress tracking with checkmarks
- Form validation and error handling
- Responsive navigation
- Custom scrollbars
- Loading indicators
- Success/error messages

### Dark Theme Design
- Premium dark color scheme
- High contrast text for readability
- Subtle hover effects
- Consistent styling across all components
- Elegant form inputs and buttons

## Dependencies

- Streamlit
- Python 3.x
- Supabase (for data storage)
- Custom utility modules:
  - prompts.py (AI prompts and preferences)
  - utils.py (Helper functions)
  - supabase_utils.py (Database operations)
  - images.py (Icon management)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd travel-planner
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file with:
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Initial Preferences**
   - Select your budget range
   - Choose travel dates
   - Enter destination and starting location
   - Select purpose and interests

2. **Preference Refinement**
   - Specify dietary requirements
   - Indicate mobility needs
   - Choose accommodation preferences

3. **Activity Selection**
   - Review AI-suggested activities
   - Select preferred activities
   - Customize your itinerary

4. **Final Itinerary**
   - View your personalized travel plan
   - Save or update your trip
   - Access emergency information
   - Get packing recommendations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your License Type] - See LICENSE file for details

## Acknowledgments

- Built with Streamlit
- Styled with custom CSS
- Icons from [source]
- AI capabilities powered by [AI service] 