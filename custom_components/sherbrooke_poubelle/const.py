"""Constants for the Sherbrooke Waste Collection integration."""

DOMAIN = "sherbrooke_poubelle"

# API endpoints
API_SEARCH_URL = "https://www.sherbrooke.ca/api/content/waste-disposal-search/"

# Configuration keys
CONF_ADDRESS_NUMBER = "address_number"
CONF_STREET_NAME = "street_name"
CONF_SELECTED_ADDRESS = "selected_address"
CONF_CALENDAR_URL = "calendar_url"
CONF_SECTOR = "sector"
CONF_COLLECTION_DAY = "collection_day"
CONF_NOTIFICATION_TIME = "notification_time"

# Update interval (every 24 hours)
UPDATE_INTERVAL = 24 * 60 * 60  # seconds

# Waste types
WASTE_TYPE_GARBAGE = "garbage"      # Black bin
WASTE_TYPE_RECYCLING = "recycling"  # Green bin 
WASTE_TYPE_COMPOST = "compost"      # Brown bin 

# Mapping of French terms to waste types
WASTE_TYPE_MAPPING = {
    "ordures": WASTE_TYPE_GARBAGE,
    "résidus alimentaires": WASTE_TYPE_COMPOST,
    "compost": WASTE_TYPE_COMPOST,
    "organique": WASTE_TYPE_COMPOST,
    "recyclage": WASTE_TYPE_RECYCLING,
    "matières recyclables": WASTE_TYPE_RECYCLING,
}

# Icons for each waste type
ICONS = {
    WASTE_TYPE_GARBAGE: "mdi:trash-can",
    WASTE_TYPE_RECYCLING: "mdi:recycle",
    WASTE_TYPE_COMPOST: "mdi:leaf",
}

# Colors for each waste type
COLORS = {
    WASTE_TYPE_GARBAGE: "#2c3e50",   # Dark gray/black
    WASTE_TYPE_RECYCLING: "#27ae60", # Green 
    WASTE_TYPE_COMPOST: "#8B4513",   # Brown 
}

# Display names
WASTE_TYPE_NAMES = {
    WASTE_TYPE_GARBAGE: "Garbage",
    WASTE_TYPE_RECYCLING: "Recycling",
    WASTE_TYPE_COMPOST: "Compost",
}

# Notification settings
DEFAULT_NOTIFICATION_TIME = "19:00"  # 7 PM the day before
NOTIFICATION_DAYS_BEFORE = 1  # Notify day before collection
