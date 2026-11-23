# AI Agent Harness Explained — Build One with Python & Ollama

A beginner-friendly **TechXOps** hands-on project showing how a small AI agent harness works using **Python**, **Ollama**, and the **Qwen3 4B** open-weight model.

This project collects pricing information from three official websites, sends relevant text to an AI model, checks extracted results against the supplied source text, and generates reports.

> **What you'll learn:** The model helps extract information; Python manages the workflow, tools, retries, validation, and logging. This is a **Python-controlled harness**, not a fully autonomous agent that chooses its own tools.

## How it works

```text
User's task
    |
    v
Python harness
    |-- Retrieve official pricing pages
    |-- Clean and shorten webpage text
    |-- Ask Ollama/Qwen3 to extract plans as JSON
    |-- Validate response and supporting source quotes
    |-- Retry failed extraction where appropriate
    `-- Save CSV + Markdown + JSON + execution trace
```

## What you need

- **Python 3.10 or later** — https://www.python.org/downloads/
- **VS Code** (recommended) — https://code.visualstudio.com/
- **Ollama** — https://ollama.com/download
- Internet access for installation and **live website retrieval**
- Enough RAM to run `qwen3:4b`; performance depends on your computer

No paid AI API key is required when using Ollama. An optional OpenAI provider is supported.

## 1. Install and check the AI model

Install Ollama, open it, then run in **PowerShell**:

```powershell
ollama --version
ollama pull qwen3:4b
ollama list
ollama run qwen3:4b "Reply with the word ready. /no_think"
```

The first model download is several gigabytes. If the Ollama service is not running, open the Ollama desktop application. `ollama serve` can start the service manually if the port is free.

## 2. Set up the Python project (Windows)

Open this repository folder in VS Code. In the terminal, run:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks environment activation, switch the VS Code terminal profile to Command Prompt and run `.venv\Scripts\activate.bat`.

Open `.env` and check that these settings are present:

```dotenv
MODEL_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:4b
```

**Never commit an `.env` file containing API keys.** `.gitignore` excludes it.

## 3. Run live research

```powershell
python main.py --mode live
```

The code currently checks the official pricing pages of **Notion, Asana, and ClickUp**. The company configuration is in the `COMPETITORS` dictionary in `main.py`.

The program does not depend on DuckDuckGo search; it starts with known official pricing URLs. Some websites may reject automated requests or load prices using JavaScript. The project records unavailable information rather than inventing prices.

### Slow local model? Try a shorter input

```powershell
python main.py --mode live --max-chars 3500 --timeout 420
```

This reduces the amount of text sent to the model, but it may also omit some pricing details. A longer timeout is not a substitute for enough available memory.

## 4. Optional offline practice mode

```powershell
python main.py --mode fixture
```

This mode uses local text files in `fixtures/` to test the extraction flow without visiting live websites. **Every fixture price is invented for demonstration and must not be presented as a current vendor price.** Ollama still needs to be running in fixture mode.

## 5. Output files

After running, inspect `output/live/` or `output/fixture/`:

| File | Purpose |
| --- | --- |
| `pricing.csv` | Extracted plan names, prices, currency, period, billing, and evidence |
| `summary.md` | Readable comparison generated from validated data |
| `findings.json` | Structured extraction results and run details |
| `trace.json` | Events, warnings, retries, and execution stages |

Even a report with validated source quotes can contain mistakes (for example, an incorrect region, billing toggle or plan association). **Always verify purchasing decisions against the official pricing pages.**

## 6. Optional OpenAI provider

The same workflow can use an OpenAI API model. In `.env`, set:

```dotenv
MODEL_PROVIDER=openai
OPENAI_API_KEY=your_actual_key
OPENAI_MODEL=gpt-4.1-mini
```

Choose a model available in your account. OpenAI API usage may cost money. Keep the API key private and never share it in a screen recording.

## Project structure

```text
.
├── main.py               # Retrieval, extraction, validation, reports and CLI
├── requirements.txt      # Python dependencies
├── .env.example          # Non-secret configuration template
├── .gitignore            # Excludes local files, keys, generated outputs
├── fixtures/             # Clearly fictional offline sample data
│   ├── notion.txt
│   ├── asana.txt
│   └── clickup.txt
└── README.md
```

The `output/` directory is created when you run the program and is not committed to Git.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Ollama connection error | Open Ollama and confirm `http://localhost:11434` is reachable |
| Model not found | Run `ollama pull qwen3:4b` and `ollama list` |
| Model request timed out | Try `--max-chars 3500 --timeout 420`; check available RAM |
| Website unavailable | The site may block requests or redirect; use another approved source, or explain the missing result |
| `0/3 companies` | Review `output/live/trace.json` to see which stages failed |
| PowerShell activation error | Switch to Command Prompt and run `.venv\Scripts\activate.bat` |

## Limitations

- This is an **educational prototype**, not production-grade scraping or purchasing advice.
- Tool execution follows a **predefined Python sequence**; it does not autonomously choose tools.
- Some pricing pages use client-side JavaScript or anti-automation protections.
- Evidence validation checks whether the model's quoted phrase appears in retrieved text; it does **not** prove the extracted price is correct.
- Run responsibly; do not use this script for bulk crawling.

## Video tutorial

Watch the TechXOps walkthrough: https://youtu.be/5MpGMmR6_3c

Follow **TechXOps** for beginner-friendly, practical AI, AI agents and generative AI projects.

## License

No license has been assigned yet. Add a `LICENSE` file if you intend to grant others permission to reuse, modify or distribute the code (for example, the MIT License, if suitable).
