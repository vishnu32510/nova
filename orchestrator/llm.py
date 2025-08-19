# For hackathon: start with a fake router that emits a tool call when it sees keywords.
# Replace with real gpt-oss call (vLLM/llama.cpp or hosted) returning either text or {tool, arguments}.
import asyncio, re

async def run_llm(text: str):
    if re.search(r"set .*alarm|alarm .* at|alarm .* for", text, re.I):
        return {
            "tool": "set_alarm",
            "arguments": {"time_iso": "2025-08-20T06:30:00", "label": "Alarm"}
        }
    return "(llm) " + text