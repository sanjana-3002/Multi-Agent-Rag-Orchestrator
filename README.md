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
backend/
├── main.py                      # FastAPI entry point
├── agents/
│   ├── cfo_agent.py             # Financial analysis agent (ReAct pattern)
│   └── cro_agent.py             # Marketing analysis agent
├── orchestrator/
│   ├── agent_router.py          # Routes queries to CFO or CRO
│   ├── orchestrator.py          # Multi-agent task decomposition & synthesis
│   ├── workflows.py             # Pre-defined business workflows
│   └── smart_orchestrator.py   # Orchestrator + conversation memory
├── memory/
│   └── conversation_memory.py  # Short-term + persistent memory
└── tools/
    ├── financial_tools.py       # Mock financial data (CFO tools)
    ├── financial_data.py        # Alpha Vantage API integration
    ├── news_data.py             # NewsAPI integration
    └── social_data.py           # News-derived sentiment analysis

frontend/
└── src/app/
    ├── page.tsx                 # Landing page + chat UI
    └── layout.tsx

Day1–Day11/                      # Learning journey — daily progress notes
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
