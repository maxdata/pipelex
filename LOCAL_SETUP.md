# Running Pipelex Fully Local - No Cloud APIs Required

Pipelex **does NOT require the Pipelex API server** and can run completely locally. Here are your options:

## Option 1: Ollama (Recommended - 100% Local & Free)

**Ollama** runs AI models entirely on your machine with no internet required.

### Setup Ollama:

1. **Install Ollama:**
   - macOS: `brew install ollama` or download from https://ollama.ai
   - Linux: `curl -fsSL https://ollama.ai/install.sh | sh`
   - Windows: Download from https://ollama.ai

2. **Pull a model:**
   ```bash
   ollama pull llama3.2       # Fast, 3B parameters
   ollama pull llama3         # Better quality, 8B parameters
   ollama pull mistral        # Good alternative
   ```

3. **Start Ollama (runs automatically on macOS/Windows):**
   ```bash
   ollama serve  # Usually not needed, starts automatically
   ```

4. **Enable in Pipelex:**
   The Ollama backend is already enabled in `.pipelex/inference/backends.toml`:
   ```toml
   [ollama]
   enabled = true
   endpoint = "http://localhost:11434/v1"
   ```

5. **Use Ollama models in your pipelines:**
   ```toml
   [pipe.my_local_pipe]
   type = "PipeLLM"
   description = "Use local Ollama model"
   output = "Text"
   model = { model = "llama3", temperature = 0.7 }
   prompt = "Write a haiku about coding"
   ```

### Available Ollama Models:
- `llama3.2` - Fast, good for simple tasks
- `llama3` - Better quality, general purpose
- `mistral` - Good for technical tasks
- `codellama` - Optimized for code generation
- `phi3` - Small and fast
- See full list: https://ollama.ai/library

---

## Option 2: Other Local Inference Servers

### LM Studio
- GUI application for running local models
- Download: https://lmstudio.ai
- Default endpoint: `http://localhost:1234/v1`

### vLLM
- High-performance inference server
- Install: `pip install vllm`
- Run: `vllm serve <model-name>`

### llama.cpp server
- Lightweight C++ inference
- Compile and run with `server` command

**Configure custom endpoint:**
```toml
[custom_local]
enabled = true
endpoint = "http://localhost:YOUR_PORT/v1"
```

---

## Option 3: Bring Your Own API Keys (Not Local, but Private)

If you want to use commercial APIs but run Pipelex locally:

1. **OpenAI** - Add `OPENAI_API_KEY` to `.env`
2. **Anthropic/Claude** - Add `ANTHROPIC_API_KEY` to `.env`
3. **Google** - Add `GOOGLE_API_KEY` to `.env`

**You control your data** - Pipelex runs on your machine and only sends requests to the APIs you configure.

---

## Option 4: Internal Backend (No AI)

For testing pipeline structure without AI:

```bash
# The internal backend is already enabled
pipelex validate your_pipeline.plx
```

This validates your pipeline logic without making any API calls.

---

## Quick Test with Ollama

Once Ollama is installed and running:

1. **Create a simple pipeline:**
   ```bash
   cat > test_local.plx << 'EOF'
   domain = "local_test"
   description = "Test local Ollama execution"

   [pipe.hello_local]
   type = "PipeLLM"
   description = "Generate text locally"
   output = "Text"
   model = { model = "llama3.2", temperature = 0.7 }
   prompt = "Write a short greeting for a developer testing Pipelex locally."
   EOF
   ```

2. **Validate it:**
   ```bash
   source .venv/bin/activate
   pipelex validate test_local.plx
   ```

3. **Run it:**
   ```bash
   pipelex run test_local.plx
   ```

---

## Summary

**You have full control:**
- ✅ Run 100% locally with Ollama (no internet needed after model download)
- ✅ Use any OpenAI-compatible API (LM Studio, vLLM, etc.)
- ✅ Bring your own API keys from any provider
- ✅ Mix and match: local models for some tasks, cloud APIs for others

**The Pipelex inference API is completely optional** - it's just one of many backend options.
