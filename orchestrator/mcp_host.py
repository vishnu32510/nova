from typing import Dict, Any
from tools.alarms import set_alarm, list_alarms, cancel_alarm, alarm_action
from tools.gpio import gpio_write, gpio_read

TOOL_REGISTRY = {
    "set_alarm": set_alarm,
    "list_alarms": list_alarms,
    "cancel_alarm": cancel_alarm,
    "alarm_action": alarm_action,
    "gpio_write": gpio_write,
    "gpio_read": gpio_read,
}

async def call_tool(name: str, args: Dict[str, Any]):
    fn = TOOL_REGISTRY.get(name)
    if not fn:
        return {"error": f"unknown tool {name}"}
    # allow async or sync tools
    if getattr(fn, "__await__", None):
        return await fn(**args)
    return fn(**args)

