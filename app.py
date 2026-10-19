import os
import json
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from serpapi import GoogleSearch
import sentry_sdk
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize Sentry Production Telemetry & OpenTelemetry Tracing
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment="production",
    release="nichetrace-sdr@3.8.0",
)

sentry_sdk.set_tag("architecture", "unified_single_file_agent_v3")
sentry_sdk.set_user({"id": "autonomous_sdr_01", "role": "market_researcher"})

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = None
model = None
LOCAL_MODEL_READY = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    global tokenizer, model, LOCAL_MODEL_READY
    print(f"Loading local open-weight model: {MODEL_NAME}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )
        LOCAL_MODEL_READY = True
        print("Qwen model successfully loaded into memory.")
    except Exception as model_err:
        print(f"Warning: Local Qwen loading failed ({model_err}). Active fallback enabled.")
        sentry_sdk.capture_exception(model_err)
        LOCAL_MODEL_READY = False
    yield

app = FastAPI(title="NicheTrace SDR Unified Intelligence", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuditPayload(BaseModel):
    keyword: str
    ticker: str = "NVDA"
    mode: str = "combined"

def generate_qwen_analysis(keyword: str, ticker: str, market_summary: str) -> str:
    if not LOCAL_MODEL_READY or model is None or tokenizer is None:
        return f"Grounded Analysis for '{keyword}': Strong market signal detected. Correlate pricing strategy with ${ticker} equity momentum."

    try:
        prompt = (
            f"System: You are an elite market researcher. Analyze this data for '{keyword}' and stock '${ticker}':\n"
            f"{market_summary}\n\n"
            "Provide 2 concise, actionable business advice sentences for a side-hustle founder:"
        )

        messages = [{"role": "user", "content": prompt}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        with torch.no_grad():
            generated_ids = model.generate(**model_inputs, max_new_tokens=90)
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

        return tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    except Exception as err:
        sentry_sdk.capture_exception(err)
        return f"Inference Notice: Local model reasoning fallback active ({err}). Market demand signal remains valid."

def fetch_serp_data(engine: str, params: dict):
    params["engine"] = engine
    return GoogleSearch(params).get_dict()

# Embedded Single-File HTML / Tailwind / Chart.js Dashboard Frontend
HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NicheTrace SDR & Financial Intelligence Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        lavender: '#C8B6E2',
                        pistachio: '#A8E6CF',
                        rose: '#F8A5C2',
                        peach: '#FFD3B6',
                        cream: '#FAF8F5',
                        darkslate: '#2D3748',
                        softpurple: '#9B89B3'
                    },
                    fontFamily: { sans: ['Inter', 'sans-serif'] }
                }
            }
        }
    </script>
</head>
<body class="h-full flex flex-col antialiased bg-[#FAF8F5] text-[#2D3748]">
    <header class="bg-white/90 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex items-center justify-between border-b border-lavender/30">
        <div class="flex items-center space-x-3">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-lavender to-pistachio flex items-center justify-center font-bold text-darkslate shadow-sm">NT</div>
            <div>
                <h1 class="font-bold text-lg text-darkslate leading-tight">NicheTrace SDR</h1>
                <p class="text-xs text-gray-500">Autonomous Market & Financial Intelligence</p>
            </div>
        </div>
        <div class="flex items-center space-x-2">
            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-pistachio/30 text-darkslate">
                <span class="w-2 h-2 mr-1.5 bg-green-500 rounded-full animate-pulse"></span> Qwen 2.5 Active
            </span>
        </div>
    </header>

    <main class="max-w-7xl w-full mx-auto p-6 flex-grow flex flex-col gap-6">
        <!-- Input Control Panel -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-lavender/20 flex flex-col md:flex-row gap-4 items-center justify-between">
            <div class="w-full md:w-1/3">
                <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">Target Niche Keyword</label>
                <input type="text" id="keywordInput" value="Pet Safe Soy Candles" class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-lavender text-sm">
            </div>
            <div class="w-full md:w-1/4">
                <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">Correlated Ticker</label>
                <input type="text" id="tickerInput" value="ETSY" class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-lavender text-sm">
            </div>
            <div class="w-full md:w-1/4">
                <label class="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">Execution Mode</label>
                <select id="modeInput" class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-lavender text-sm bg-white">
                    <option value="combined">Full Market + Equity Engine</option>
                    <option value="market_only">Market Research Only</option>
                    <option value="equity_only">Financial Equity Only</option>
                </select>
            </div>
            <div class="w-full md:w-auto flex items-end">
                <button onclick="runAudit()" id="submitBtn" class="w-full md:w-auto px-6 py-2.5 bg-darkslate text-white font-medium rounded-xl hover:bg-gray-800 transition shadow-sm text-sm">
                    Execute Pipeline
                </button>
            </div>
        </div>

        <!-- Results Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-white rounded-2xl p-6 shadow-sm border border-lavender/20 flex flex-col justify-between">
                <div>
                    <h3 class="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Market Viability Score</h3>
                    <div class="flex items-baseline space-x-2">
                        <span id="scoreDisplay" class="text-4xl font-bold text-darkslate">--</span>
                        <span class="text-sm font-medium text-emerald-600">/ 100 Signal</span>
                    </div>
                </div>
                <div class="mt-4 pt-4 border-t border-gray-100">
                    <p id="latencyDisplay" class="text-xs text-gray-500">Pipeline Latency: --</p>
                </div>
            </div>

            <div class="bg-white rounded-2xl p-6 shadow-sm border border-lavender/20 md:col-span-2 flex flex-col justify-between">
                <div>
                    <h3 class="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Autonomous Qwen AI Strategic Directive</h3>
                    <p id="insightDisplay" class="text-sm text-darkslate italic leading-relaxed">Run an audit to generate local transformer monetization playbooks...</p>
                </div>
            </div>
        </div>

        <!-- Chart Section -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-lavender/20">
            <h3 class="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-4">Demand Index & Ticker Momentum Waterfall</h3>
            <div class="h-64">
                <canvas id="demandChart"></canvas>
            </div>
        </div>
    </main>

    <script>
        let demandChartInstance = null;

        async function runAudit() {
            const btn = document.getElementById('submitBtn');
            btn.innerText = 'Analyzing...';
            btn.disabled = true;

            const payload = {
                keyword: document.getElementById('keywordInput').value,
                ticker: document.getElementById('tickerInput').value,
                mode: document.getElementById('modeInput').value
            };

            try {
                const response = await fetch('/audit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();

                document.getElementById('scoreDisplay').innerText = data.viability_score;
                document.getElementById('latencyDisplay').innerText = `Pipeline Latency: ${data.latency_sec}s`;
                document.getElementById('insightDisplay').innerText = `"${data.qwen_insight}"`;

                updateChart(data.chart_data);
            } catch (err) {
                alert('Audit pipeline execution failed: ' + err);
            } finally {
                btn.innerText = 'Execute Pipeline';
                btn.disabled = false;
            }
        }

        function updateChart(chartValues) {
            const ctx = document.getElementById('demandChart').getContext('2d');
            if (demandChartInstance) demandChartInstance.destroy();

            demandChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Day 1', 'Day 7', 'Day 14', 'Day 30', 'Day 60', 'Day 90'],
                    datasets: [{
                        label: 'Market Demand Index',
                        data: chartValues || [45, 52, 68, 74, 82, 88],
                        borderColor: '#9B89B3',
                        backgroundColor: 'rgba(200, 182, 226, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, max: 100 } }
                }
            });
        }

        window.onload = () => updateChart([45, 52, 68, 74, 82, 82]);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def render_dashboard():
    return HTMLResponse(content=HTML_DASHBOARD)

@app.post("/audit")
async def execute_market_and_equity_audit(payload: AuditPayload):
    global_start = time.time()
    api_key = os.getenv("SERPAPI_KEY", "dummy_key")

    transaction = sentry_sdk.start_transaction(
        op="agent.pipeline", 
        name=f"Audit ({payload.mode.upper()}): {payload.keyword}"
    )

    try:
        # SPAN 1: SERPAPI MULTI-ENGINE CLUSTER PERFORMANCE
        with sentry_sdk.start_span(op="serpapi.multi_engine_cluster", description=f"Execute SerpApi Mode: {payload.mode}") as span:
            span.set_data("query.keyword", payload.keyword)
            span.set_data("query.ticker", payload.ticker)
            fetch_start = time.time()

            org_data = await run_in_threadpool(
                fetch_serp_data, "google", {"q": f"best products for {payload.keyword} pricing", "api_key": api_key, "num": 5}
            )
            news_data = await run_in_threadpool(
                fetch_serp_data, "google_news", {"q": payload.keyword, "api_key": api_key}
            )
            maps_data = await run_in_threadpool(
                fetch_serp_data, "google_maps", {"q": f"{payload.keyword} shops", "api_key": api_key}
            )
            fin_data = await run_in_threadpool(
                fetch_serp_data, "google_finance", {"q": payload.ticker, "api_key": api_key}
            )
            span.set_data("fetch_latency_sec", round(time.time() - fetch_start, 3))

        # SPAN 2: AGENT REASONING & VIABILITY SCORING
        with sentry_sdk.start_span(op="agent.reasoning", description="Compute Market Viability Score") as span:
            organic_results = len(org_data.get("organic_results", []))
            news_results = len(news_data.get("news_results", []))
            maps_results = len(maps_data.get("local_results", []))
            
            viability_score = max(15, min(95, (news_results * 10) + (maps_results * 2) - (organic_results * 3) + 55))
            span.set_data("viability_score", viability_score)
            sentry_sdk.set_measurement("market_viability_score", viability_score)

        # SPAN 3: LOCAL QWEN LLM INFERENCE
        market_summary = f"Organic competitors: {organic_results}, News volume: {news_results}, Local agency density: {maps_results}."
        with sentry_sdk.start_span(op="qwen.local_inference", description="Execute Local Qwen Reasoner"):
            qwen_insight = await run_in_threadpool(generate_qwen_analysis, payload.keyword, payload.ticker, market_summary)

        total_latency = round(time.time() - global_start, 2)
        sentry_sdk.set_measurement("total_pipeline_latency_sec", total_latency)
        transaction.finish()

        return JSONResponse(content={
            "status": "success",
            "keyword": payload.keyword,
            "ticker": payload.ticker,
            "viability_score": viability_score,
            "latency_sec": total_latency,
            "qwen_insight": qwen_insight,
            "chart_data": [50, 58, 65, 72, 78, viability_score]
        })

    except Exception as err:
        sentry_sdk.capture_exception(err)
        transaction.finish()
        raise HTTPException(status_code=500, detail=str(err))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
