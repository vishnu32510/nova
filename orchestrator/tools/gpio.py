try:
    from gpiozero import LED
    _gpio_supported = True
except Exception:
    _gpio_supported = False

_LEDS = {}

def gpio_write(pin: int, state: str = "off"):
    if not _gpio_supported:
        return {"ok": True, "note": "GPIO not available on this host"}
    led = _LEDS.get(pin) or LED(pin)
    _LEDS[pin] = led
    (led.on() if state.lower() in ("on", "high", "1", "true") else led.off())
    return {"pin": pin, "state": state}

def gpio_read(pin: int):
    if not _gpio_supported:
        return {"ok": True, "note": "GPIO not available on this host"}
    led = _LEDS.get(pin)
    return {"pin": pin, "is_lit": bool(led and led.is_lit)}

