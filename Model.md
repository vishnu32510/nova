Perfect — let’s get you a **local 7–9B model** running via **llama.cpp’s OpenAI-compatible server**. I’ll show two good choices:

* **Mistral-7B-Instruct (easy, permissive license)** — great first pick
* **Llama-3.1-8B-Instruct (stronger, may be gated)** — needs HF login approval

Then we’ll start the server and plug it into your `run_llm()`.

---

# Option A — Mistral-7B-Instruct (recommended to start)

### 1) Make a models folder

```bash
mkdir -p ~/models/mistral7b
cd ~/models/mistral7b
```

### 2) Download a quantized **GGUF** file (works with llama.cpp)

Use TheBloke’s Q4\_K\_M (good quality/speed balance on CPU/Metal/Pi):

```bash
# Direct file download from the HF repo (GGUF quant)
curl -L -o mistral-7b-instruct-v0.2.Q4_K_M.gguf \
  https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

(Repo reference: Mistral-7B-Instruct v0.2 GGUF. ([Hugging Face][1]))

### 3) Install the OpenAI-compatible server

* **Mac (Apple Silicon)** – enable Metal for big speed-ups:

```bash
CMAKE_ARGS="-DGGML_METAL=on" pip install "llama-cpp-python[server]"
```

* **Pi 5 / Linux CPU (optional BLAS accel):**

```bash
CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS" \
  pip install "llama-cpp-python[server]"
```

(Docs for the server & build flags. ([Llama CPP Python][2], [GitHub][3]))

### 4) Start the server (OpenAI API compatible)

```bash
python -m llama_cpp.server \
  --model ~/models/mistral7b/mistral-7b-instruct-v0.2.Q4_K_M.gguf \
  --port 8080 \
  --n_ctx 4096 \
  --chat_format mistral-instruct
```

(“mistral-instruct” chat\_format is supported in recent releases. ([Llama CPP Python][4]))

### 5) Quick test (tool-calling ready)

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    "messages":[{"role":"user","content":"Say hello in one short sentence."}],
    "max_tokens":64
  }' | jq .
```

(Endpoint behavior: OpenAI-compatible chat API. ([Llama CPP Python][2], [Stack Overflow][5]))

---

# Option B — Llama-3.1-8B-Instruct (stronger, may be gated)

### 1) Request access on Hugging Face (once)

Open the model repo and accept terms (requires login). ([Hugging Face][6])

### 2) Download a GGUF (e.g., **Q6\_K\_L** high quality or **Q4\_K\_M** for speed)

```bash
pip install huggingface_hub
huggingface-cli login   # paste your HF token

# Example: download a single GGUF file into ~/models/llama3.1-8b
mkdir -p ~/models/llama3.1-8b && cd ~/models/llama3.1-8b
huggingface-cli download bartowski/Meta-Llama-3.1-8B-Instruct-GGUF \
  Meta-Llama-3.1-8B-Instruct-Q6_K_L.gguf --local-dir . --local-dir-use-symlinks False
```

(Example GGUF repo & sizes list. ([Hugging Face][7]))

### 3) Start server (chat template for Llama-3.x)

```bash
python -m llama_cpp.server \
  --model ~/models/llama3.1-8b/Meta-Llama-3.1-8B-Instruct-Q6_K_L.gguf \
  --port 8080 \
  --n_ctx 4096 \
  --chat_format llama-3
```

(Use the server’s **chat\_format** matching the model family. ([Llama CPP Python][8]))

---

# Plug into your project

In your `orchestrator/llm.py` replace the stub with the HTTP call you already set up earlier, and set env vars:

```bash
export LLAMA_URL="http://127.0.0.1:8080/v1/chat/completions"
export LLAMA_MODEL="local-gguf"
```

Now when you type “**set an alarm for 6:30 am called gym**” in your UI, the model will produce a **tool call** and your Python orchestrator will invoke `set_alarm`.

* llama.cpp’s server is **OpenAI-compatible** (so your existing JSON/tool flow works). ([Llama CPP Python][2])
* GGUF is the right file format for llama.cpp; HF has a nice primer if you’re curious. ([Hugging Face][9])

---

## Notes for Pi 5

* Prefer **Q4\_K\_M** quant for 7B/8B on Pi 5 (fits RAM; decent accuracy).
* Keep your Flutter UI as **Web (HTML renderer)** to save memory; the LLM is the heavy part.
* If you later want **gpt-oss-20B** for the hackathon demo, run it **hosted** (or on a desktop GPU) and just switch `LLAMA_URL` to that endpoint. Official gpt-oss pages + HF repo confirm model availability for hosted/self-hosted use. ([OpenAI][10], [Hugging Face][11])

If you tell me which model you want (Mistral-7B vs Llama-3.1-8B), I’ll paste the exact **one-liner** to download that specific **.gguf** and the precise **server command** you can copy-paste.

[1]: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF?utm_source=chatgpt.com "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
[2]: https://llama-cpp-python.readthedocs.io/en/latest/server/?utm_source=chatgpt.com "OpenAI Compatible Web Server - llama-cpp-python"
[3]: https://github.com/abetlen/llama-cpp-python?utm_source=chatgpt.com "Python bindings for llama.cpp"
[4]: https://llama-cpp-python.readthedocs.io/en/latest/changelog/?utm_source=chatgpt.com "Changelog - llama-cpp-python docs"
[5]: https://stackoverflow.com/questions/79597244/how-to-create-prompt-with-chat-endpoint-for-llama-cpp?utm_source=chatgpt.com "How to create prompt with /chat endpoint for llama.cpp?"
[6]: https://huggingface.co/QuantFactory/Meta-Llama-3.1-8B-Instruct-GGUF?utm_source=chatgpt.com "QuantFactory/Meta-Llama-3.1-8B-Instruct-GGUF"
[7]: https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF?utm_source=chatgpt.com "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF"
[8]: https://llama-cpp-python.readthedocs.io/?utm_source=chatgpt.com "Getting Started - llama-cpp-python"
[9]: https://huggingface.co/docs/hub/en/gguf-llamacpp?utm_source=chatgpt.com "GGUF usage with llama.cpp"
[10]: https://openai.com/index/introducing-gpt-oss/?utm_source=chatgpt.com "Introducing gpt-oss"
[11]: https://huggingface.co/openai/gpt-oss-20b?utm_source=chatgpt.com "openai/gpt-oss-20b"

