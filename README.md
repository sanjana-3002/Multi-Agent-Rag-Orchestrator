
## CampaignBrain - Multi-Agent RAG System with Tool Use & Orchestration

- CampaignBrain is a production-style multi-agent AI system that answers complex business questions by coordinating specialized agents instead of relying on a single LLM call.
- It demonstrates task decomposition, tool-augmented reasoning, conversational memory, and modular agent design — built with FastAPI, Next.js, and OpenAI.


## What It Does

Instead of responding like a chatbot, the system:
	•	Classifies intent via an intelligent router
	•	Decomposes complex queries
	•	Delegates work to specialized agents
	•	Uses structured tools via function calling
	•	Synthesizes final recommendations
	•	Maintains conversational context

Think: an AI leadership team (CFO + CRO) working together.

##  Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js Frontend                        │
│              (React, Tailwind, Real-time Chat)              │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                        │
│                    (API Gateway + CORS)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   Multi-Agent Orchestrator                  │
│              (Task Decomposition + Synthesis)               │
└───────────────┬────────────────────────┬────────────────────┘
                │                        │
        ┌───────┴────────┐      ┌────────┴────────┐
        ↓                ↓      ↓                 ↓
   ┌─────────┐      ┌─────────┐      ┌──────────────┐
   │   CFO   │      │   CRO   │      │  Router      │
   │  Agent  │      │  Agent  │      │  (GPT-3.5)   │
   └────┬────┘      └────┬────┘      └──────────────┘
        │                │
        ↓                ↓
   ┌─────────────────────────┐
   │   Tool Registry         │
   │   (7 Domain Tools)      │
   └─────────────────────────┘
```

## Agents
	•	CFO Agent – Revenue, forecasting, budget checks
	•	CRO Agent – Campaign analysis, ROAS, performance comparison
	•	Router – GPT-based intent classification (95%+ accuracy)
	•	Orchestrator – Multi-agent coordination & synthesis
	•	Memory Layer – Context-aware follow-ups

## Key Features

### 🤖 Specialized Agents
- **CFO Agent**: Financial analysis, revenue tracking, expense management, forecasting
- **CRO Agent**: Marketing campaign analysis, ROAS calculation, channel comparison
- **Intelligent Router**: 95%+ accuracy in query classification using GPT-3.5

### 🎯 Core Capabilities
- Single-agent queries (financial or marketing)
- Multi-agent coordination for complex analysis
- Context-aware conversations with memory
- Real-time response streaming
- Beautiful, responsive UI

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Success Rate** | 95%+ across all test scenarios |
| **Response Time** | 2.3s average (includes multi-agent coordination) |
| **Cost per Query** | $0.002 (with orchestration) |
| **Routing Accuracy** | 95%+ |
| **Test Coverage** | 100% on core workflows |


## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.11+
python --version

# Node.js 18+
node --version

# OpenAI API Key
export OPENAI_API_KEY="sk-..."
```

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/campaignbrain.git
cd campaignbrain

# Backend setup
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env

# Frontend setup (in new terminal)
cd frontend
npm install
```

### Running Locally
```bash
# Terminal 1: Start backend
cd backend
python main.py
# Server runs on http://localhost:8000

# Terminal 2: Start frontend
cd frontend
npm run dev
# UI available at http://localhost:3000
```

### Docker Deployment (Optional)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:3000
```

## 📁 Project Structure
```
Multi-Agent-Rag-Orchestrator/
├── backend/                  # FastAPI backend
│   ├── main.py              # API server
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
│
├── frontend/                # Next.js frontend
│   ├── app/
│   │   ├── page.js         # Main chat interface
│   │   ├── layout.js       # App layout
│   │   └── globals.css     # Styles + animations
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
│
├── Day8/                    # CFO Agent implementation
│   ├── cfo_agent.py        # CFO agent with tools
│   └── tools.py            # Financial tools
│
├── Day9/                    # CRO Agent + Router
│   ├── cro_agent.py        # CRO agent with tools
│   └── agent_router.py     # Intelligent routing
│
├── Day10/                   # Multi-Agent Orchestration
│   ├── orchestrator.py     # Task decomposition
│   └── workflows.py        # Pre-defined workflows
│
├── Day12/                   # Memory & Context
│   ├── conversation_memory.py    # Memory system
│   └── smart_orchestrator.py    # Context-aware orchestrator
│
├── Day14/                   # Evaluation & Testing
│   ├── agent_evaluator.py       # Comprehensive tests
│   └── evaluation_report.txt    # Performance results
│
└── README.md               # This file
```

## 🛠️ Technology Stack

**Backend:**
- FastAPI (REST API framework)
- OpenAI API (GPT-3.5-turbo for reasoning)
- Pydantic (Data validation)
- Python 3.11+

**Frontend:**
- Next.js 14 (React framework)
- Tailwind CSS (Styling)
- Modern animations & transitions

**Architecture Patterns:**
- ReAct (Reasoning + Acting)
- Function calling (Tool use)
- Hub-and-spoke orchestration
- Persistent memory storage

## 💡 Usage Examples

### Simple Financial Query
```
User: "What was our Q4 revenue?"
→ CFO Agent
→ $15M, up 25% from Q3
```

### Marketing Analysis
```
User: "How did our Facebook campaign perform?"
→ CRO Agent
→ 2.0x ROAS, 2,500 conversions, $250K spend
```

### Multi-Agent Coordination
```
User: "Can we afford to double marketing spend?"
→ Orchestrator decomposes task
→ CFO: Checks budget ($4.5M available)
→ CRO: Analyzes ROI (2.5x ROAS)
→ Synthesis: "Yes, recommend increasing by $500K"
```

### Follow-up Questions (Context-Aware)
```
User: "How did Facebook perform?"
Agent: "2.0x ROAS..."

User: "What about Instagram?"
Agent: "Instagram also 2.0x ROAS..." (understands context!)
```

## 🧪 Testing
```bash
# Run evaluation suite
python Day14/agent_evaluator.py

# Run specific tests
python Day10/test_coordination.py
python Day12/test_memory.py

# Expected output: 95%+ success rate
```

**Future Enhancements:**
- [ ] Additional agents (HR, Product, Sales)
- [ ] Voice interface (Whisper API)
- [ ] Analytics dashboard
- [ ] Slack/Teams integration
- [ ] Real-time collaboration

## 🎯 Use Cases

- **Marketing Agencies**: Campaign analysis, ROI tracking, budget optimization
- **Finance Teams**: Revenue forecasting, expense management, P&L analysis
- **Business Intelligence**: Cross-functional insights, strategic planning
- **Customer Success**: Data-driven recommendations, performance tracking

## 🔐 Security & Privacy

- API keys stored in environment variables
- No user data logged
- CORS configured for specific origins
- Per-user conversation isolation
- Optional authentication layer

## 📊 Cost Analysis

**Development Cost:** ~$14 total
- Week 1 (RAG): $4.10
- Week 2 (Agents): $10.00

**Production Cost:** ~$0.002 per query
- 1,000 queries/day: $60/month
- 10,000 queries/day: $600/month
- Highly scalable with caching

## ## Author

Sanjana Waghray
AI Systems | Multi-Agent Architectures | Applied ML

GitHub: https://github.com/sanjana-3002
LinkedIn: https://www.linkedin.com/in/sanjana-waghray-63905b1b8/
Portfolio: https://sanjanawaghray.com/

