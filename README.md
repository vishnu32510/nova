## Runbook

### LLM server (llama.cpp OpenAI-compatible)

```bash
python -m llama_cpp.server \
  --model '/Users/vishnu/garage/hackathons/open-model/nova/orchestrator/models/mistral7b/mistral-7b-instruct-v0.2.Q4_K_M.gguf' \
  --port 8080 \
  --n_ctx 4096 \
  --chat_format mistral-instruct
```

### Flutter app

```bash
flutter run Chrome
```

### Python FastAPI orchestrator

```bash
uvicorn main:app --host 127.0.0.2 --port 8000
```


# nova
