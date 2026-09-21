# Build an AI Agent with Google ADK - Video 2: MCP Integration

This repository contains the code for the second video in the series "Build an AI Agent with Google ADK". In this video, we extend the basic blogger agent by connecting it to a live Google Trends MCP server.

## Project Structure

- `blogger/agent.py`: The main agent application with MCP integration.
- `blogger/server.py`: The minimal MCP server exposing the `trends` tool.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables (API key).
- `index.lab.md`: The step-by-step codelab.

## Setup Instructions

### 1. Navigate to the Project Directory
```bash
cd build_mcp_agent_google_adk
```

### 2. Install Dependencies
```bash
python -m venv myenv
.\myenv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install google-adk

pip show google-adk

adk --version

pip install -r requirements.txt
```

### 3. Setup Environment Variables
Update your `.env` file with a Hugging Face access token:
```text
MODEL=meta-llama/Llama-3.1-8B-Instruct
HF_TOKEN=hf_your_token
```

The agent sends chat requests through Hugging Face's OpenAI-compatible router
using ADK's LiteLLM adapter. Choose a Hugging Face model that supports chat
completion and tool calling.

## Running the Agent

Run the following command to start the ADK Web UI:
```bash
python -c "from google.adk.cli.cli_tools_click import main; main()" web . --no-reload
```

Open your browser and navigate to `http://127.0.0.1:8000` to interact with the agent!

*Note: The MCP server starts automatically when the agent needs it. You do not need to run it separately.*

### If the UI shows `POST /run_sse 404`

This means the browser is reusing a session that no longer exists, usually after
restarting `adk web`, or the project directory is not a valid Python identifier.
Stop and restart the server from `build_mcp_agent_google_adk`, then open
`http://127.0.0.1:8000` in a new tab, and create a new session. Do not reuse a
URL containing an old `session=` value.

### If the agent shows HTTP 402 from Hugging Face

An error such as `You have depleted your monthly included credits` comes from
Hugging Face Inference Providers. It cannot be fixed by changing ADK or MCP
code. Add prepaid credits or upgrade the Hugging Face account, then restart
`adk web` and create a new session. A different Hugging Face model still uses
the same account credits.

For a no-cost local alternative, run a tool-calling model with Ollama and
configure LiteLLM for that local endpoint instead of the Hugging Face router.

## Key Learnings & Troubleshooting

- **Handling Rate Limits**: Google Trends (via `pytrends`) often returns `429 Too Many Requests`. The `trends_server.py` is designed with a multi-layer fallback strategy (Related Queries -> Daily Trending -> Realtime Trending -> Keyword Echo) to ensure the agent remains robust even when the external API fails.
- **Timeout Bug**: A previous version encountered `requests.api.get() got multiple values for keyword argument 'timeout'`. This was fixed by removing the explicit `requests_args` in `TrendReq` initialization.
