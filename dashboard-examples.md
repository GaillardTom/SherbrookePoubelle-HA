# Dashboard Card Examples

Beautiful dashboard cards for your Home Assistant waste collection display.

## Card 1: Simple Color-Coded Card

Shows the next collection with a dynamic color background based on bin type.

```yaml
type: conditional
conditions:
  - entity: sensor.sherbrooke_poubelle_next_collection
    state: "Recycling"
card:
  type: picture
  image: /local/images/green_bin.png
  aspect_ratio: "16:9"
  title: ♻️ Put Out the Green Bin
  tap_action:
    action: more-info
    entity: sensor.sherbrooke_poubelle_next_collection
```

## Card 2: Full Dashboard Card (Recommended)

A beautiful card showing all the information with conditional colors.

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      ## 🗑️ Waste Collection

  - type: entity
    entity: sensor.sherbrooke_poubelle_next_collection
    name: Next Collection
    state_color: true
    card_mod:
      style: |
        ha-card {
          {% if states('sensor.sherbrooke_poubelle_next_collection') == 'Recycling' %}
            background-color: #27ae60;
          {% elif states('sensor.sherbrooke_poubelle_next_collection') == 'Compost' %}
            background-color: #8B4513;
          {% else %}
            background-color: #2c3e50;
          {% endif %}
          color: white;
        }

  - type: gauge
    entity: sensor.sherbrooke_poubelle_collection_countdown
    name: Days Until Collection
    min: 0
    max: 7
    severity:
      green: 3
      yellow: 1
      red: 0
    card_mod:
      style: |
        ha-card {
          {% if states('sensor.sherbrooke_poubelle_next_collection') == 'Recycling' %}
            --primary-color: #27ae60;
          {% elif states('sensor.sherbrooke_poubelle_next_collection') == 'Compost' %}
            --primary-color: #8B4513;
          {% else %}
            --primary-color: #2c3e50;
          {% endif %}
        }

  - type: glance
    entities:
      - entity: sensor.sherbrooke_poubelle_next_collection
        name: Type
      - entity: sensor.sherbrooke_poubelle_collection_countdown
        name: Days
    show_state: true
    show_name: true
    state_color: true
```

## Card 3: Minimal Compact Card

Perfect for a busy dashboard or as a badge.

```yaml
type: entity-button
entity: sensor.sherbrooke_poubelle_next_collection
name: ""
icon: |
  {% if states('sensor.sherbrooke_poubelle_next_collection') == 'Recycling' %}
    mdi:recycle
  {% elif states('sensor.sherbrooke_poubelle_next_collection') == 'Compost' %}
    mdi:leaf
  {% else %}
    mdi:trash-can
  {% endif %}
show_name: true
show_state: true
show_icon: true
tap_action:
  action: more-info
entity_id: sensor.sherbrooke_poubelle_next_collection
card_mod:
  style: |
    ha-card {
      {% if states('sensor.sherbrooke_poubelle_next_collection') == 'Recycling' %}
        --icon-color: #27ae60;
        border-left: 4px solid #27ae60;
      {% elif states('sensor.sherbrooke_poubelle_next_collection') == 'Compost' %}
        --icon-color: #8B4513;
        border-left: 4px solid #8B4513;
      {% else %}
        --icon-color: #2c3e50;
        border-left: 4px solid #2c3e50;
      {% endif %}
    }
```

## Card 4: Notification-Style Card (For Lovelace)

Shows a prominent reminder when collection is tomorrow.

```yaml
type: conditional
conditions:
  - entity: sensor.sherbrooke_poubelle_collection_countdown
    state: "1"
card:
  type: vertical-stack
  cards:
    - type: markdown
      content: |
        ## ⚠️ Reminder: Waste Collection Tomorrow!
    - type: entity
      entity: sensor.sherbrooke_poubelle_next_collection
      name: Put out the
      icon: mdi:bell-ring
      card_mod:
        style: |
          ha-card {
            background-color: #f39c12;
            color: white;
            font-weight: bold;
            animation: pulse 2s infinite;
          }
          @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
          }
```

## Card 5: Grid View (All Bins)

Shows all three bin types with current status.

```yaml
type: grid
cards:
  - type: entity
    entity: sensor.sherbrooke_poubelle_next_collection
    name: Next Collection
    card_mod:
      style: |
        ha-card {
          {% if states('sensor.sherbrooke_poubelle_next_collection') == 'Recycling' %}
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
          {% elif states('sensor.sherbrooke_poubelle_next_collection') == 'Compost' %}
            background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
          {% else %}
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
          {% endif %}
          color: white;
        }
  - type: entity
    entity: sensor.sherbrooke_poubelle_collection_countdown
    name: Days Until
    icon: mdi:calendar-clock
    card_mod:
      style: |
        ha-card {
          background: #ecf0f1;
        }
columns: 2
```

## Required Dependencies

For the `card_mod` styling to work, install:

1. **card-mod** via HACS:
   ```
   Frontend -> card-mod
   ```

## Bin Images

Download or create these images and place in `config/www/images/`:

- `green_bin.png` - Green recycling bin
- `brown_bin.png` - Brown compost bin
- `black_bin.png` - Black garbage bin

Or use emojis instead:
- ♻️ Green/Recycling
- 🍂 Brown/Compost
- 🗑️ Black/Garbage

## Automation Example

Send a notification when it's time to put out the bin:

```yaml
automation:
  - alias: "Waste Collection Reminder"
    trigger:
      - platform: state
        entity_id: sensor.sherbrooke_poubelle_collection_countdown
        to: "1"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🗑️ Waste Collection Tomorrow"
          message: "Don't forget to put out the {{ states('sensor.sherbrooke_poubelle_next_collection') }} bin!"
          data:
            color: |
              {% if states('sensor.sherbrooke_poubelle_next_collection') == 'Recycling' %}
                #27ae60
              {% elif states('sensor.sherbrooke_poubelle_next_collection') == 'Compost' %}
                #8B4513
              {% else %}
                #2c3e50
              {% endif %}
```
