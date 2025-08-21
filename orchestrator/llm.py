import os, json, httpx
from llm_tools_schema import TOOLS_SCHEMA

LLAMA_URL = os.getenv("LLAMA_URL", "http://127.0.0.1:8080/v1/chat/completions")
MODEL_NAME = os.getenv("LLAMA_MODEL", "local-mistral7b")  # label for logs only

async def run_llm(user_text: str):
  payload = {
    "model": MODEL_NAME,
    "temperature": 0.2,
    "max_tokens": 256,
    "messages": [
        {
            "role": "system",
            "content": (
                "You are a **local AI assistant** running on-device. "
                "You **must always use the available tools** to take actions when the user requests them. "
                "Do not just explain. "
                "For example: if the user says 'set alarm at 5 pm', you must return a tool call to `set_alarm`. "
                "If no tool is relevant, only then reply in text."
            ),
        },
        {"role": "user", "content": user_text},
    ],
    "tools": TOOLS_SCHEMA,
    "tool_choice": "auto"  # ensures the model can trigger tools automatically
}



  async with httpx.AsyncClient(timeout=60) as client:
    r = await client.post(LLAMA_URL, json=payload)
    r.raise_for_status()
    data = r.json()

  msg = data["choices"][0]["message"]

  if "tool_calls" in msg and msg["tool_calls"]:
    tc = msg["tool_calls"][0]
    fn = tc["function"]["name"]
    args = tc["function"].get("arguments", {})
    if isinstance(args, str):
      try:
        args = json.loads(args)
      except Exception:
        args = {"_raw": args}
    return {"tool": fn, "arguments": args}

  content = msg.get("content", "").strip()
  return content or "(no content)"