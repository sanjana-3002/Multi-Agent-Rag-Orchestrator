# 🧠 CampaignBrain - Multi-Agent AI System

**Live Demo:** https://multi-agent-rag-orchestrator.vercel.app

A production-grade multi-agent AI system for business intelligence, featuring specialized CFO and CRO agents that coordinate to provide financial and marketing insights.

## 🚀 Tech Stack

- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python
- **AI:** OpenAI GPT-3.5/GPT-4, Multi-agent orchestration
- **Deployment:** Vercel (frontend), Railway (backend)
- **Data:** Alpha Vantage, NewsAPI

## ✨ Features

- Multi-agent coordination (CFO + CRO agents)
- Smart orchestrator with task decomposition and synthesis
- Conversation memory for natural multi-turn queries
- Pre-defined workflows (budget check, channel optimization, ROI analysis)
- Real-time API communication
- Professional UI with agent visualization

## 📁 Project Structure

```
Multi-Agent-Rag-Orchestrator/
│
├── backend/                          # Production API (deployed on Railway)
│   ├── main.py                       # FastAPI entry point
│   ├── agents/
│   │   ├── cfo_agent.py              # Financial analysis agent (ReAct pattern)
│   │   └── cro_agent.py              # Marketing analysis agent
│   ├── orchestrator/
│   │   ├── agent_router.py           # GPT-3.5 query router (95%+ accuracy)
│   │   ├── orchestrator.py           # Task decomposition & result synthesis
│   │   ├── workflows.py              # Budget check, channel opt, ROI analysis
│   │   └── smart_orchestrator.py     # Orchestrator + conversation memory
│   ├── memory/
│   │   └── conversation_memory.py    # Short-term + persistent memory
│   └── tools/
│       ├── financial_tools.py        # Mock financial data (CFO tools)
│       ├── financial_data.py         # Alpha Vantage API integration
│       ├── news_data.py              # NewsAPI integration
│       └── social_data.py            # News-derived sentiment analysis
│
├── rag_pipeline/                     # RAG research pipeline (Days 1–6)
│   ├── embeddings/
│   │   ├── embeddings.py             # OpenAI text-embedding-3-small wrapper
│   │   └── semantic_search.py        # Cosine similarity search
│   ├── vector_db/
│   │   ├── embedding_cache.py        # JSON-based embedding cache
│   │   ├── qdrant_setup.py           # Qdrant vector DB setup
│   │   └── index_documents.py        # Document ingestion pipeline
│   ├── hybrid_search/
│   │   ├── bm25_search.py            # BM25 keyword search
│   │   └── hybrid_search.py          # BM25 + semantic fusion (alpha-weighted)
│   ├── query_optimizer/
│   │   ├── query_optimizer.py        # Query expansion & rewriting
│   │   ├── metadata_filter.py        # Structured metadata filtering
│   │   └── smart_search.py           # Unified search interface
│   ├── evaluation/
│   │   ├── metrics.py                # Precision@K, Recall@K, MRR
│   │   ├── evaluator.py              # RAG evaluation with LLM-as-judge
│   │   └── test_cases.json           # Ground-truth test dataset
│   └── cost_optimizer/
│       ├── cost_tracker.py           # Per-call API cost logging
│       └── model_router.py           # GPT-3.5 vs GPT-4 routing by complexity
│
├── agent_system/                     # Multi-agent research system (Days 7–11)
│   ├── cfo_agent/
│   │   ├── tools.py                  # Financial tool registry
│   │   └── cfo_agent.py              # CFO agent (ReAct loop, 4 tools)
│   ├── multi_agent/
│   │   ├── cro_agent.py              # CRO agent (marketing tools)
│   │   └── agent_router.py           # Query classifier (CFO / CRO / General)
│   ├── orchestration/
│   │   ├── orchestrator.py           # MultiAgentOrchestrator (decompose → execute → synthesize)
│   │   ├── workflows.py              # WorkflowLibrary (3 pre-defined workflows)
│   │   └── test_coordination.py      # Orchestration test suite
│   ├── memory/
│   │   ├── conversation_memory.py    # JSON-backed session + long-term memory
│   │   ├── context_aware_agent.py    # Agent wrapper with memory injection
│   │   ├── smart_orchestrator.py     # SmartOrchestrator (memory + orchestration)
│   │   └── test_memory.py            # Memory persistence & follow-up tests
│   └── evaluation/
│       ├── agent_evaluator.py        # Full system benchmark (12 test cases)
│       └── demo.py                   # Interactive + scripted demo
│
└── frontend/                         # Next.js chat UI (deployed on Vercel)
    └── src/app/
        ├── page.tsx                  # Landing page + chat interface
        └── layout.tsx
```

## 🔧 Setup

```bash
# Clone and install
git clone https://github.com/sanjana-3002/Multi-Agent-Rag-Orchestrator.git
cd Multi-Agent-Rag-Orchestrator

# Backend
cp .env.example .env             # Add your API keys
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

## 🎯 Try It

Visit: https://multi-agent-rag-orchestrator.vercel.app

Example queries:
- "What was our Q4 revenue?"
- "How did our Facebook campaign perform?"
- "Can we afford to increase marketing spend?"
- "Compare Facebook vs Instagram ROAS"
