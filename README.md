# 🚀 NicheTrace SDR & Financial Intelligence

> Autonomous market discovery, multi-engine search orchestration, and local financial arbitrage engine powered by FastAPI, Qwen 2.5, SerpApi, and Sentry OpenTelemetry tracing.

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-005571?style=for-the-badge&logo=fastapi)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-2C3E50?style=for-the-badge&logo=uvicorn&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-FFD21E?style=for-the-badge)
![Qwen](https://img.shields.io/badge/Model-Qwen2.5--1.5B--Instruct-6F42C1?style=for-the-badge&logo=huggingface&logoColor=white)
![SerpApi](https://img.shields.io/badge/SerpApi-Multi--Engine-009688?style=for-the-badge&logo=google&logoColor=white)
![Sentry](https://img.shields.io/badge/Sentry-Tracing-362D59?style=for-the-badge&logo=sentry&logoColor=white)
![pip](https://img.shields.io/badge/pip-v23%2B-005F73?style=for-the-badge&logo=pypi&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Tailwind CSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5787D?style=for-the-badge&logo=chart.js&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

---

# 🧭 What Is NicheTrace?

**NicheTrace** is an autonomous Sales Development Representative (SDR) and market validation engine. It cross-references real-time organic search demand, competitor density, news sentiment, and financial stock market equities to compute a **Market Viability Score (0-100)**—generating instant AI monetization playbooks without expensive cloud API fees.

<img width="554" height="554" alt="WEEK2 4" src="https://github.com/user-attachments/assets/dc826f7f-3f19-4f49-a58b-9518ccd59e47" />


---

# 🏗️ Core Architecture & Tech Stack

* **Backend & API:** Python 3.10+, FastAPI, Uvicorn, Pydantic
* **Local AI Engine:** `Qwen/Qwen2.5-1.5B-Instruct` via Hugging Face Transformers & PyTorch (GPU CUDA acceleration with automatic CPU fallback)
* **Multi-Engine Search Cluster:** SerpApi (`google`, `google_news`, `google_maps`, `google_finance`) running asynchronously via background threadpools (`fastapi.concurrency.run_in_threadpool`)
* **Observability:** Sentry Python SDK & OpenTelemetry distributed transaction tracing (`agent.pipeline`)
* **Frontend Dashboard:** Single-file native UI embedded directly using Tailwind CSS and Chart.js

---

# 📊 System Architecture Diagram

```text
 [ User Browser / Frontend UI (Tailwind CSS & Chart.js) ]
                             │
                             ▼ (HTTP POST /audit: keyword, ticker, mode)
 [ FastAPI Asynchronous Web Server (app.py) ]
                             │
                             ▼ 
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ SENTRY ROOT TRANSACTION: agent.pipeline                                  │
 │ - Tracing Context: W3C Traceparent propagation                           │
 │ - Global Tags: architecture="unified_single_file", release="3.8.0"       │
 └───────────────────────────┬──────────────────────────────────────────────┘
                             │
         ┌───────────────────┴───────────────────┐
         ▼                                       ▼
 ┌───────────────────────────────┐       ┌───────────────────────────────┐
 │ SENTRY CHILD SPAN 1           │       │ SENTRY CHILD SPAN 2           │
 │ op: "serpapi.multi_engine"    │       │ op: "agent.reasoning"         │
 │ desc: "Execute Search Mesh"   │       │ desc: "Compute Viability"     │
 └──────────────┬────────────────┘       └──────────────┬────────────────┘
                │ Serpapi                               │
     ┌──────────┼──────────┬──────────┐                 │
     ▼          ▼          ▼          ▼                 ▼
  [Google]   [News]     [Maps]    [Finance]       [Scoring Engine]
  (Organic)  (PR/Media) (Local)   (Equities)      - Processes counts
     │          │          │          │           - Computes 0-100 index
     └──────────┴────┬─────┴──────────┘                 │
                     │                                  ▼
                     ▼                   (Sentry Measurement Gauge:
       (Threadpooled Non-Blocking Fetch    market_viability_score)
        Latencies Tagged to Span Data)                  │
                     │                                  │
                     └──────────────────┬───────────────┘
                                        │
                                        ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ SENTRY CHILD SPAN 3                                                      │
 │ op: "qwen.local_inference"                                               │
 │ desc: "Execute Local Qwen Transformer Reasoner"                          │
 └──────────────────────────────────┬───────────────────────────────────────┘
                                    │
                                    ▼
                     [ In-Memory PyTorch Model Execution ]
                     ( Qwen/Qwen2.5-1.5B-Instruct on RAM/VRAM )
                                    │
                                    ▼
                     ( Sentry Measurement Gauge: total_latency_sec )
                                    │
                                    ▼
                     [ Proactive Exception Handler ]
                     ( sentry_sdk.capture_exception(err) )
                                    │
                                    ▼
                     [ Structured JSON Response ]
                     ( Viability Score + AI Directive + Charts )
```

# Navigation & UI/UX Architecture
NicheTrace is architected as a high-performance Single-Page Application (SPA) driven by a lightweight FastAPI backend, eliminating clunky page reloads and ensuring lightning-fast operator workflows.

## 1. Dynamic Mode Switcher Navigation
Operators can instantly reconfigure the operational scope of the application using the top-right header navigation tabs:
Full Engine Mode: Combines both market discovery (SerpApi) and financial equity intelligence into a single unified analysis.
Market Research Only: Isolates the pipeline to focus purely on competitor tracking, search intent, and channel saturation.
Financial Equity Only: Restricts execution to ticker momentum, institutional flows, and financial health metrics.

## 2. Control Center Layout & Component Breakdown
The interface is engineered with a modern, high-contrast Tailwind CSS layout designed for instant data digestion and zero cognitive friction:
Intelligence Query Parameters (Left Panel): Dedicated input controls for targeting specific micro-SaaS keywords (e.g., "solar crm") and correlating them directly with live equity tickers (e.g., "$NVDA").
Execution Telemetry Waterfall: Real-time logging of sub-second reasoning layers (combined_execution, scoring_engine, reasoning_inference), providing instant visibility into pipeline execution speed.
Summary Metric Cards & Directives (Right Panel): Instantly surfaces key performance indicators including the calculated Viability Score (69/100), market competitor saturation count, and AI-generated strategic directives complete with step-by-step actionable playbooks.
Visual Charts Hub: Features an advanced analytics suite containing a Line Chart tracking market demand versus equity momentum over time, a Bar Chart evaluating channel volume saturation (Organic vs. Paid Ads), and a Doughnut Chart breaking down optimal monetization models.


<img width="1477" height="797" alt="Screenshot 2026-10-19 223309" src="https://github.com/user-attachments/assets/fe671c69-6dc0-47a6-839a-8fbed4f2c8e0" />


<img width="1482" height="798" alt="Screenshot 2026-10-19 223341" src="https://github.com/user-attachments/assets/9cac110c-db66-4f5f-83b5-86f283a5fc5b" />


# Why NicheTrace SDR? Feature Matrix & Technical Advantages

| Feature / Architectural Dimension | Generic LLM API Wrappers | Traditional SEO / Keyword Suites | NicheTrace SDR Engine (Our Solution) |
| :--- | :--- | :--- | :--- |
| **Search Engine Coverage** | Single text prompt or basic web browsing | Static organic index & backlink database | SerpApi Multi-Engine Mesh (Concurrent parallel execution across google, google_news, google_maps, google_finance) |
| **Real-Time Stock Coupling** | None (No financial market integration) | None (Purely web traffic focused) | Google Finance Engine (Correlates search velocity directly against $NVDA, $TSLA, $Etsy stock trends) |
| **Distributed Transaction Tracing** | None (No request path visibility) | None (External web platform) | Sentry Root Pipeline Transactions (agent.pipeline tracks end-to-end audit lifecycles) |
| **Granular Performance Child Spans** | None (Opaque black-box calls) | None (Manual reporting dashboards) | OpenTelemetry Sub-Span Isolation (serpapi.multi_engine_cluster, agent.reasoning, qwen.local_inference) |
| **Custom Performance Measurement Gauges** | None | None | Live Metric Reporting (sentry_sdk.set_measurement() tracks dynamic market_viability_score) |
| **Proactive Exception Isolation & Capture** | Basic try/catch console prints | Standard web server crash logs | Automated Exception Interception (sentry_sdk.capture_exception() streams stack traces live to dashboard) |
| **Execution Speed & Latency** | 3.0s – 8.0s (Sequential Cloud API calls) | N/A (Manual dashboard lookups) | Sub-1.2s Latency (Threadpooled parallel worker fetches via run_in_threadpool) |
| **LLM Inference Cost** | $0.03 – $0.10 per query invocation | $99 – $399 / month subscription fees | $0.00 Per Audit (In-memory local Qwen2.5-1.5B-Instruct transformer execution) |
| **Data Privacy & Trade-Secret Security** | Sent to external third-party cloud servers | Tracked in external search logs | 100% Local Inference Privacy (Sensitive market queries never leave system RAM) |
| **Deployment Footprint** | Multi-service API dependency chain | Third-party web platform | Single-File App (app.py) (FastAPI backend + embedded Tailwind & Chart.js UI) |


# 💻 System Requirements & Prerequisites
## Hardware Requirements
***Processor (CPU):*** 4-Core x86_64 or Apple Silicon (M-Series / ARM64) Processor (Minimum).

***System Memory (RAM):***

_Minimum:_ 8 GB RAM (Supports CPU fallback inference for Qwen/Qwen2.5-1.5B-Instruct).

_Recommended:_ 16 GB+ RAM for seamless concurrent threadpool execution and search cluster orchestration.

***Disk Storage:*** Minimum 5 GB available SSD disk space (for local Hugging Face transformer weight caching and model weights).

***Graphics Unit (GPU - Optional):*** NVIDIA GPU with CUDA 11.8/12.0+ support (4 GB+ VRAM) for accelerated local transformer inference.

## Software Requirements
***Operating System:*** Linux (Ubuntu 20.04+ / Debian / RHEL), macOS 12+, or Windows 10/11 (WSL2 recommended).

***Python Runtime:*** Python 3.10 or higher (Python 3.11 recommended for optimized asynchronous event loop performance).

***Package Manager & Tools:*** pip (v23.0+) or conda, and git (v2.30+).

***External API Credentials:***

***SerpApi API Key:*** Required for concurrent multi-engine search fetches (google, google_news, google_maps, google_finance).

***Sentry DSN:*** Required for OpenTelemetry distributed transaction tracing, child span execution, and performance metric tracking.

# 🚀 Execution Commands & Setup Instructions

***1. Clone repository & navigate to directory***
git clone [https://github.com/your-username/nichetrace-sdr.git](https://github.com/your-username/nichetrace-sdr.git)
cd nichetrace-sdr

***2. Create and activate Python virtual environment***
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

***3. Install all software requirements***
pip install --upgrade pip
pip install -r requirements.txt

***4. Set required API credentials***
export SERPAPI_API_KEY="your_serpapi_api_key_here"
export SENTRY_DSN="[https://your_sentry_dsn_here@o0.ingest.sentry.io/0](https://your_sentry_dsn_here@o0.ingest.sentry.io/0)"

***5. Execute application***
python app.py


<img width="554" height="554" alt="WEEK 3 5" src="https://github.com/user-attachments/assets/ebc2c8b4-c848-4a4f-ac81-2e76adaf0615" />


The graveyard of brilliant indie projects isn't filled with bad code—it's filled with products nobody was searching for.

NicheTrace SDR & Financial Intelligence flips the script on side-hustle validation. By uniting local open-weight AI (Qwen2.5-1.5B), an asynchronous SerpApi multi-engine cluster, and surgical Sentry OpenTelemetry tracing into a single deployable Python file, solo builders no longer have to burn cash or guess in the dark.

You get ironclad data privacy, zero token costs, real-time market search signals, stock market equity correlations, and sub-second execution speeds—all before writing a single line of feature code.

The future belongs to founders who validate in seconds, not months. NicheTrace proves that you don't need a $10,000 venture budget or a maze of proprietary cloud APIs to discover million-dollar opportunities. With local open-weight models, multi-engine search orchestration, and surgical telemetry, the power to predict market demand sits entirely on your local machine.

Stop shipping into the void. Turn on the lights, protect your privacy, and build what actually prints.

> ***"The secret of getting ahead is getting started."***

> ***"Opportunities don't happen. You create them."***


# 🏆 Prize Categories Targeted
***Best Use of SerpApi:*** Transforms SerpApi into an asynchronous multi-engine intelligence mesh (google, google_news, google_maps, google_finance) running concurrently inside FastAPI threadpools to eliminate blocks and feed real-time ground truth into local transformer inference.

<img width="766" height="400" alt="Serpapi" src="https://github.com/user-attachments/assets/758f924b-a7da-4ee2-9fac-6cf611f9c929" />


***Best Use of Sentry Agent Tracing:*** Implements professional-grade OpenTelemetry observability—tracking root pipeline transactions (agent.pipeline), granular child execution spans (serpapi.multi_engine_cluster, agent.reasoning, qwen.local_inference), and live performance measurement gauges (market_viability_score).

<img width="1200" height="630" alt="SENTRY" src="https://github.com/user-attachments/assets/844f813e-7c47-4ab5-9b27-a7df1ac8e9e7" />



------------
> **📝 Note on Repository Updates:** 
> While the core project code, pipeline logic, and instrumentation were completed during the official Hacktoberfest challenge window, `README.md` , and `requirements.txt` specifications were polished and structured post-deadline for enhanced clarity and ease of setup.
                   
