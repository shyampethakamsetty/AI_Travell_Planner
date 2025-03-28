import base64

# SVG Icons
PLANE_ICON = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M21 14L12.7243 18.3828C12.2691 18.6288 11.7309 18.6288 11.2757 18.3828L3 14M21 10L12.7243 5.61716C12.2691 5.37124 11.7309 5.37124 11.2757 5.61716L3 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

CALENDAR_ICON = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M8 7V3M16 7V3M7 11H17M5 21H19C20.1046 21 21 20.1046 21 19V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V19C3 20.1046 3.89543 21 5 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

LOCATION_ICON = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 13C13.6569 13 15 11.6569 15 10C15 8.34315 13.6569 7 12 7C10.3431 7 9 8.34315 9 10C9 11.6569 10.3431 13 12 13Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12 22C14 18 20 15.4183 20 10C20 5.58172 16.4183 2 12 2C7.58172 2 4 5.58172 4 10C4 15.4183 10 18 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

CHECK_ICON = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

def get_icon_html(icon: str, color: str = "currentColor") -> str:
    """Convert SVG icon to HTML with specified color."""
    return icon.replace('currentColor', color)

def get_background_image() -> str:
    """Get background image as base64 string."""
    # You would typically load an actual image file here
    # For now, returning a placeholder gradient
    return """
    background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
    """ 