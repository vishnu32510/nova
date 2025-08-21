TOOLS_SCHEMA = [
  {
    "type": "function",
    "function": {
      "name": "set_alarm",
      "description": "Set an alarm at a specific ISO8601 time",
      "parameters": {
        "type": "object",
        "properties": {
          "time_iso": {"type": "string", "description": "ISO8601 datetime"},
          "label": {"type": "string"}
        },
        "required": ["time_iso"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "gpio_write",
      "description": "Toggle a GPIO pin on/off",
      "parameters": {
        "type": "object",
        "properties": {
          "pin": {"type": "integer"},
          "state": {"type": "string", "enum": ["on", "off"]}
        },
        "required": ["pin", "state"]
      }
    }
  }
]

