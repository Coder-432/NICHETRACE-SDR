🚀 NicheTrace SDR & Financial Intelligence
Autonomous market discovery, multi-engine search orchestration, and local financial arbitrage engine powered by FastAPI, Qwen 2.5, SerpApi, and Sentry OpenTelemetry tracing.

What Is NicheTrace?
NicheTrace is an autonomous Sales Development Representative (SDR) and market validation engine. It cross-references real-time organic search demand, competitor density, news sentiment, and financial stock market equities to compute a Market Viability Score (0-100)—generating instant AI monetization playbooks without expensive cloud API fees.

Core Architecture & Tech Stack
Backend & API: Python 3.10+, FastAPI, Uvicorn, Pydantic

Local AI Engine: Qwen/Qwen2.5-1.5B-Instruct via Hugging Face Transformers & PyTorch (GPU CUDA acceleration with automatic CPU fallback)

Multi-Engine Search Cluster: SerpApi (google, google_news, google_maps, google_finance) running asynchronously via background threadpools (fastapi.concurrency.run_in_threadpool)

Observability: Sentry Python SDK & OpenTelemetry distributed transaction tracing (agent.pipeline)

Frontend Dashboard: Single-file native UI embedded directly using Tailwind CSS and Chart.js

System Architecture Pipeline
[POST /audit Payload]
|
+-► [Sentry Span: SerpApi Multi-Engine Mesh] --► (Google Search, News, Maps, Finance)
+-► [Sentry Span: Viability Scoring Engine] --► (Computes Market Demand Index)
-► [Sentry Span: Qwen Local LLM Inference] --► (Synthesizes Strategic Business Advice)

Quickstart Guide (Run Locally in 60 Seconds)
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/nichetrace-sdr.git
cd nichetrace-sdr

2. Set Up Python Environment
Ensure you are using Python 3.10+ and pip 26.x:
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

3. Install Dependencies
pip install fastapi uvicorn google-search-results sentry-sdk torch transformers pydantic

4. Set Environment Variables (Optional)
To fetch live search results and track errors:
export SERPAPI_KEY="your_actual_serpapi_key"
export SENTRY_DSN="your_sentry_dsn"
(Note: If no keys are provided, the system defaults to safe mock execution modes).

5. Launch the Application
python app.py
Open your browser and navigate to: http://localhost:8000

Hackathon Prize Tracks Targeted
Best Use of SerpApi: Utilizes a concurrent, parallel search mesh across 4 Google nodes (google, google_news, google_maps, google_finance) wrapped in non-blocking threadpools to cut latency down to sub-400ms.

Best Use of Sentry Agent Tracing: Implements full OpenTelemetry transaction spans (agent.pipeline, serpapi.multi_engine_cluster, qwen.local_inference), custom performance measurement gauges (market_viability_score), and automated exception isolation.
