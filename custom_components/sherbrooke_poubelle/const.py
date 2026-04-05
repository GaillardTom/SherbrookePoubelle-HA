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

# Update interval (every week should be sufficient since the schedule doesn't change often)
UPDATE_INTERVAL = 7 * 24 * 60 * 60  # seconds

# Waste types
WASTE_TYPE_GARBAGE = "waste"      # Black bin
WASTE_TYPE_RECYCLING = "recycling"  # Green bin 
WASTE_TYPE_COMPOST = "compost"      # Brown bin 

# Mapping of terms to waste types
WASTE_TYPE_MAPPING = {
    #Francais
    "ordures": WASTE_TYPE_GARBAGE,
    "résidus alimentaires": WASTE_TYPE_COMPOST,
    "compost": WASTE_TYPE_COMPOST,
    "organique": WASTE_TYPE_COMPOST,
    "récupération": WASTE_TYPE_RECYCLING,
    "matières recyclables": WASTE_TYPE_RECYCLING,
    "recyclage": WASTE_TYPE_RECYCLING,

    #Anglais
    "waste": WASTE_TYPE_GARBAGE,
    "recycling": WASTE_TYPE_RECYCLING,
    "compost": WASTE_TYPE_COMPOST,
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
    WASTE_TYPE_GARBAGE: "Déchets",
    WASTE_TYPE_RECYCLING: "Recyclage",
    WASTE_TYPE_COMPOST: "Compost",
}

# Notification settings
DEFAULT_NOTIFICATION_TIME = "19:00"  # 7 PM the day before
NOTIFICATION_DAYS_BEFORE = 1  # Notify day before collection
