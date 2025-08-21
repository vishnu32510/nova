import json
import os, httpx
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mcp_host import TOOL_REGISTRY, call_tool
from llm import run_llm

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

LLAMA_HEALTH = os.getenv("LLAMA_HEALTH", "http://127.0.0.1:8080/health")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/llm")
async def llm_health():
    try:
        async with httpx.AsyncClient(timeout=3) as c:
            r = await c.get(LLAMA_HEALTH)
            return {"ok": r.status_code == 200}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            msg = json.loads(raw)
            t = msg.get("type")

            if t == "user_text":
                user_text = msg["text"].strip()
                # 1) send transcript final
                await ws.send_text(json.dumps({"type": "stt_final", "text": user_text}))
                # 2) ask LLM for action or answer
                out = await run_llm(user_text)
                if isinstance(out, dict) and out.get("tool"):
                    await ws.send_text(json.dumps({"type":"tool_call", **out}))
                    result = await call_tool(out["tool"], out.get("arguments", {}))
                    await ws.send_text(json.dumps({"type":"tool_result", "tool": out["tool"], "result": result}))
                    # Optional: ask LLM to summarize result for user; for now, template it
                    await ws.send_text(json.dumps({"type":"assistant_text", "text": f"Done: {out['tool']}"}))
                else:
                    await ws.send_text(json.dumps({"type":"assistant_text", "text": str(out)}))
            elif t == "alarm_action":
                result = await call_tool("alarm_action", msg)
                await ws.send_text(json.dumps({"type":"tool_result", "tool":"alarm_action", "result": result}))
            else:
                await ws.send_text(json.dumps({"type":"error", "message": f"unknown type: {t}"}))
    except Exception as e:
        await ws.close()