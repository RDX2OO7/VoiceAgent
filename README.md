# ADK Voice Agent

A real-time, bi-directional voice assistant built with **Google ADK** (Agent Development Kit), the **Gemini Live API** (`gemini-3.1-flash-live-preview`), **FastAPI**, and **WebSockets**.

---

## Features

- **Real-Time Audio Streaming**: Low-latency PCM 16kHz bi-directional audio streaming via WebSockets.
- **Function Tools**: Integrated tools (e.g., hotel searching & room finding) with voice feedback.
- **Interruption & Transcription**: Supports user interruption and real-time speech-to-text transcriptions for both user and agent.
- **Interactive Web Interface**: Built-in browser web app (`static/index.html`) for testing microphone input and audio playback.

---

## Prerequisites

- **Python**: 3.11 – 3.13
- **Package Manager**: [`uv`](https://docs.astral.sh/uv/) installed
- **API Key**: [Google AI Studio API Key](https://aistudio.google.com/app/apikey)

---

## Quick Start

### 1. Configure Environment

Copy `.env.example` to `.env` and add your Gemini API key:

```bash
cp .env.example .env
```

Set in `.env`:
```env
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL=gemini-3.6-flash
LIVE_MODEL=gemini-3.1-flash-live-preview
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Run Preflight Check

```bash
uv run python scripts/preflight.py
```

---

## Running the Agent

### Option A: Custom FastAPI + WebSocket Server (Recommended)

```bash
uv run uvicorn server:app --reload --port 8001
```

Open **[http://localhost:8001](http://localhost:8001)** in a Chromium browser, click **Connect Microphone**, and start talking.

### Option B: ADK Development Web UI

```bash
uv run adk web
```

Open the printed URL, select `hotel_agent`, and click the microphone button.

---

## Project Structure

```text
.
├── agent.py          # Root ADK agent & instructions
├── server.py         # FastAPI WebSocket server & LiveRequestQueue handler
├── src/              # Python source code & custom tools (search_hotels, find_rooms)
├── static/           # Frontend Web UI (HTML, CSS, Web Audio PCM stream logic)
├── scripts/          # Preflight & helper scripts
└── checkpoints/      # Workshop step-by-step progression stages
```

---

## Troubleshooting

- **Microphone issues**: Open via `http://localhost:8001` (browsers require HTTPS or `localhost` for audio permissions).
- **SSL Certificate Errors (macOS)**: Run `export SSL_CERT_FILE="$(uv run python -m certifi)"`.
- **API Key Error**: Verify `GEMINI_API_KEY` is active and `GOOGLE_GENAI_USE_VERTEXAI=FALSE`.
