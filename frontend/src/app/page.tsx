'use client';

import { useState, useRef, useEffect } from 'react';

// ── Types ──────────────────────────────────────────────────────
type Message = {
  role: 'user' | 'assistant';
  content: string;
  agents?: string[];
  executionTime?: number;
  needsCoordination?: boolean;
};

// ── Constants ──────────────────────────────────────────────────
const BACKEND = 'https://aware-trust-production-734d.up.railway.app';

const STATS = [
  { value: '87%',    label: 'Search Precision@3' },
  { value: '<2s',    label: 'Avg Response Time'   },
  { value: '$0.002', label: 'Cost Per Query'       },
  { value: '95%',    label: 'Routing Accuracy'     },
];

const SUGGESTED = [
  { icon: '💰', label: 'Q4 Revenue',       query: 'What was our Q4 2024 revenue?' },
  { icon: '📊', label: 'Campaign ROAS',    query: 'Compare ROAS across Facebook, Instagram, and Google' },
  { icon: '💡', label: 'Budget Strategy',  query: 'Should we increase marketing spend given our current financial position?' },
  { icon: '🎯', label: 'CAC Analysis',     query: 'What is our customer acquisition cost on Facebook?' },
];

const PIPELINE = [
  { label: 'User Query',         sub: null,            icon: '💬', g: 'from-blue-500 to-cyan-500'      },
  { label: 'Smart Router',       sub: 'GPT-3.5 Turbo', icon: '⚡', g: 'from-indigo-500 to-indigo-600'  },
  { label: 'Specialist Agents',  sub: 'CFO + CRO',     icon: '🤖', g: 'from-violet-500 to-purple-600'  },
  { label: 'RAG Pipeline',       sub: 'Qdrant + BM25', icon: '🔍', g: 'from-cyan-500 to-blue-600'      },
  { label: 'Final Answer',       sub: null,            icon: '✨', g: 'from-emerald-500 to-teal-600'   },
];

const TECH = [
  { name: 'GPT-4 Turbo',            cat: 'AI Agents',       cls: 'text-emerald-400 border-emerald-400/30 bg-emerald-400/5'  },
  { name: 'GPT-3.5 Turbo',          cat: 'Router & Synth',  cls: 'text-green-400   border-green-400/30   bg-green-400/5'    },
  { name: 'text-embedding-3-small', cat: 'Embeddings',      cls: 'text-blue-400    border-blue-400/30    bg-blue-400/5'     },
  { name: 'Qdrant',                 cat: 'Vector DB',        cls: 'text-violet-400  border-violet-400/30  bg-violet-400/5'   },
  { name: 'FastAPI',                cat: 'Backend',          cls: 'text-orange-400  border-orange-400/30  bg-orange-400/5'   },
  { name: 'Next.js 15',             cat: 'Frontend',         cls: 'text-slate-300   border-slate-400/30   bg-slate-400/5'    },
  { name: 'BM25 Hybrid',            cat: 'Keyword Search',   cls: 'text-purple-400  border-purple-400/30  bg-purple-400/5'   },
  { name: 'Railway + Vercel',       cat: 'Deployment',       cls: 'text-pink-400    border-pink-400/30    bg-pink-400/5'     },
];

// ── Component ──────────────────────────────────────────────────
export default function Home() {
  const [view, setView]       = useState<'landing' | 'demo'>('landing');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput]     = useState('');
  const [loading, setLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const send = async (queryText?: string) => {
    const q = queryText ?? input;
    if (!q.trim() || loading) return;

    setMessages(p => [...p, { role: 'user', content: q }]);
    if (!queryText) setInput('');
    setLoading(true);

    try {
      const res  = await fetch(`${BACKEND}/query`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ query: q, user_id: 'demo' }),
      });
      const d = await res.json();
      setMessages(p => [...p, {
        role:              'assistant',
        content:           d.answer            || 'No response received.',
        agents:            d.agents_used       || [],
        executionTime:     d.execution_time,
        needsCoordination: d.needs_coordination,
      }]);
    } catch {
      setMessages(p => [...p, {
        role:    'assistant',
        content: '⚠️ Could not reach the backend. Make sure the service is running.',
      }]);
    }
    setLoading(false);
  };

  // ── DEMO VIEW ──────────────────────────────────────────────
  if (view === 'demo') {
    return (
      <div className="min-h-screen flex flex-col bg-[#070b14]">

        {/* Header */}
        <header className="sticky top-0 z-50 border-b border-white/[0.07] bg-[#070b14]/85 backdrop-blur-2xl">
          <div className="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={() => { setView('landing'); setMessages([]); }}
                className="flex items-center gap-1.5 text-slate-400 hover:text-white transition-colors group"
              >
                <svg className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24">
                  <path stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M19 12H5M12 19l-7-7 7-7"/>
                </svg>
                <span className="text-sm">Back</span>
              </button>
              <div className="w-px h-4 bg-white/15" />
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                <span className="font-semibold text-white text-sm">CampaignBrain</span>
                <span className="text-slate-500 text-sm">/ Live Demo</span>
              </div>
            </div>
            <span className="text-xs text-slate-500 bg-slate-800/60 border border-slate-700/50 rounded-full px-3 py-1">
              Powered by GPT-4
            </span>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 max-w-4xl mx-auto w-full px-6 py-8 flex flex-col gap-5">

          {/* Empty state */}
          {messages.length === 0 && (
            <div className="flex-1 flex flex-col items-center justify-center gap-10 py-16 animate-fade-up">
              <div className="text-center">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-2xl mx-auto mb-4 shadow-xl shadow-indigo-500/25">
                  🤖
                </div>
                <h2 className="text-2xl font-bold text-white">Ask CampaignBrain</h2>
                <p className="text-slate-400 mt-2 text-sm max-w-xs mx-auto leading-relaxed">
                  Financial analysis, campaign performance, budget strategy — all in one place.
                </p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl">
                {SUGGESTED.map(s => (
                  <button
                    key={s.label}
                    onClick={() => send(s.query)}
                    className="group flex items-start gap-3 p-4 rounded-xl bg-white/[0.04] border border-white/[0.08] hover:border-indigo-500/40 hover:bg-indigo-500/[0.08] text-left transition-all duration-200"
                  >
                    <span className="text-xl flex-shrink-0 mt-0.5">{s.icon}</span>
                    <div>
                      <div className="text-sm font-semibold text-white group-hover:text-indigo-300 transition-colors">{s.label}</div>
                      <div className="text-xs text-slate-500 mt-0.5 leading-relaxed line-clamp-2">{s.query}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex gap-3 animate-fade-up ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              style={{ animationDelay: `${i * 0.04}s` }}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-[11px] font-bold text-white flex-shrink-0 mt-0.5 shadow-lg shadow-indigo-500/25">
                  AI
                </div>
              )}
              <div className="flex flex-col gap-2 max-w-[78%]">
                <div className={`rounded-2xl px-5 py-3.5 text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white rounded-tr-sm shadow-lg shadow-indigo-600/20'
                    : 'bg-slate-800/70 border border-white/[0.08] text-slate-100 rounded-tl-sm'
                }`}>
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                </div>

                {/* Agent metadata */}
                {msg.role === 'assistant' && (msg.agents?.length || msg.executionTime) && (
                  <div className="flex flex-wrap items-center gap-2 px-1">
                    {msg.agents?.map(a => (
                      <span key={a} className="text-[11px] px-2.5 py-0.5 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/25 font-medium">
                        {a.toUpperCase()}
                      </span>
                    ))}
                    {msg.needsCoordination && (
                      <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-violet-500/15 text-violet-300 border border-violet-500/25">
                        Multi-Agent
                      </span>
                    )}
                    {msg.executionTime && (
                      <span className="text-[11px] text-slate-600 ml-auto">{msg.executionTime.toFixed(2)}s</span>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Thinking indicator */}
          {loading && (
            <div className="flex gap-3 animate-fade-up">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-[11px] font-bold text-white flex-shrink-0 mt-0.5 shadow-lg shadow-indigo-500/25">
                AI
              </div>
              <div className="bg-slate-800/70 border border-white/[0.08] rounded-2xl rounded-tl-sm px-5 py-4">
                <div className="flex gap-1.5 items-center">
                  {[0, 150, 300].map(d => (
                    <div
                      key={d}
                      className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"
                      style={{ animationDelay: `${d}ms` }}
                    />
                  ))}
                </div>
              </div>
            </div>
          )}

          <div ref={endRef} />
        </div>

        {/* Input bar */}
        <div className="sticky bottom-0 border-t border-white/[0.07] bg-[#070b14]/85 backdrop-blur-2xl">
          <div className="max-w-4xl mx-auto px-6 py-4">
            <form
              onSubmit={e => { e.preventDefault(); send(); }}
              className="flex gap-3"
            >
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Ask about revenue, campaigns, ROI, forecasts…"
                className="flex-1 bg-slate-800/50 border border-white/10 rounded-xl px-5 py-3.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 focus:bg-slate-800 transition-all"
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="px-6 py-3.5 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-600 disabled:border disabled:border-white/[0.06] text-white font-semibold rounded-xl text-sm transition-all"
              >
                Send →
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  // ── LANDING VIEW ──────────────────────────────────────────
  return (
    <div className="min-h-screen bg-[#070b14] text-white overflow-x-hidden">

      {/* Ambient background orbs */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div
          className="absolute -top-40 left-[12%] w-[650px] h-[650px] bg-indigo-600/[0.18] rounded-full blur-[130px] animate-float-slow"
        />
        <div
          className="absolute top-[38%] -right-20 w-[540px] h-[540px] bg-violet-600/[0.13] rounded-full blur-[140px] animate-float-slow"
          style={{ animationDelay: '2.5s' }}
        />
        <div
          className="absolute -bottom-28 left-[42%] w-[480px] h-[480px] bg-blue-600/[0.09] rounded-full blur-[110px] animate-float-slow"
          style={{ animationDelay: '5s' }}
        />
      </div>

      {/* ── Navbar ── */}
      <nav className="relative z-10 sticky top-0 border-b border-white/[0.05] bg-[#070b14]/70 backdrop-blur-2xl">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="font-bold text-[17px] tracking-tight">CampaignBrain</span>
            <span className="text-[11px] px-2 py-0.5 bg-indigo-500/20 text-indigo-300 border border-indigo-500/25 rounded-full font-medium">v2.0</span>
          </div>
          <div className="flex items-center gap-5">
            <a
              href="https://github.com/sanjana-3002/Multi-Agent-Rag-Orchestrator"
              target="_blank"
              className="text-sm text-slate-400 hover:text-white transition-colors hidden sm:block"
            >
              GitHub
            </a>
            <button
              onClick={() => setView('demo')}
              className="text-sm px-4 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-medium transition-all hover:shadow-[0_0_22px_rgba(99,102,241,0.45)]"
            >
              Live Demo →
            </button>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 pt-24 pb-20 text-center">

        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/[0.05] border border-white/10 text-sm text-slate-300 mb-10 backdrop-blur animate-fade-up">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          Powered by OpenAI GPT-4 · Multi-Agent RAG Orchestrator
        </div>

        {/* Headline */}
        <h1
          className="text-5xl md:text-[70px] font-bold tracking-tight leading-[1.08] mb-6 animate-fade-up"
          style={{ animationDelay: '0.1s' }}
        >
          AI-Powered{' '}
          <span className="bg-gradient-to-r from-indigo-400 via-violet-400 to-purple-400 bg-clip-text text-transparent animate-gradient-x inline-block">
            Business Intelligence
          </span>
          <br className="hidden md:block" />
          {' '}for Revenue Teams
        </h1>

        {/* Subheading */}
        <p
          className="text-xl text-slate-400 max-w-2xl mx-auto mb-12 leading-relaxed animate-fade-up"
          style={{ animationDelay: '0.2s' }}
        >
          Multi-agent orchestration with hybrid RAG search. CFO and CRO agents collaborate
          in real-time to deliver financial and marketing insights grounded in your data.
        </p>

        {/* CTAs */}
        <div
          className="flex flex-col sm:flex-row gap-4 justify-center mb-16 animate-fade-up"
          style={{ animationDelay: '0.3s' }}
        >
          <button
            onClick={() => setView('demo')}
            className="px-8 py-4 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold text-lg transition-all hover:shadow-[0_0_40px_rgba(99,102,241,0.45)] active:scale-[0.98]"
          >
            Try Live Demo →
          </button>
          <a
            href="https://github.com/sanjana-3002/Multi-Agent-Rag-Orchestrator"
            target="_blank"
            className="px-8 py-4 bg-white/[0.05] hover:bg-white/[0.08] border border-white/10 hover:border-white/20 rounded-xl font-semibold text-lg transition-all"
          >
            View on GitHub
          </a>
        </div>

        {/* Stats grid */}
        <div
          className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto animate-fade-up"
          style={{ animationDelay: '0.4s' }}
        >
          {STATS.map((s, i) => (
            <div
              key={s.label}
              className="group bg-white/[0.04] border border-white/[0.08] rounded-2xl p-5 hover:border-indigo-500/35 hover:bg-white/[0.06] transition-all duration-300"
              style={{ animationDelay: `${0.4 + i * 0.05}s` }}
            >
              <div className="text-3xl font-bold text-white mb-1 group-hover:text-indigo-300 transition-colors">{s.value}</div>
              <div className="text-xs text-slate-400 leading-snug">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Pipeline Architecture ── */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-20">
        <div className="text-center mb-14">
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-indigo-400 mb-3">Architecture</div>
          <h2 className="text-3xl md:text-4xl font-bold">Two-Pipeline Design</h2>
          <p className="text-slate-400 mt-3 max-w-lg mx-auto leading-relaxed text-[15px]">
            Hybrid retrieval combines semantic vector search with BM25 keyword matching,
            then routes to specialized AI agents for domain expertise.
          </p>
        </div>

        <div className="relative rounded-3xl border border-white/[0.08] bg-white/[0.02] p-8 overflow-hidden">
          {/* Subtle dot grid */}
          <div className="absolute inset-0 [background-image:radial-gradient(rgba(255,255,255,0.04)_1px,transparent_1px)] [background-size:28px_28px] pointer-events-none" />

          {/* Flow steps */}
          <div className="relative flex flex-col md:flex-row items-stretch gap-2 md:gap-0">
            {PIPELINE.map((step, i) => (
              <div key={step.label} className="flex md:flex-1 items-center w-full">
                {/* Card */}
                <div className="flex-1 relative overflow-hidden rounded-2xl border border-white/[0.08] hover:border-white/20 transition-all duration-300 cursor-default group">
                  <div className={`absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r ${step.g}`} />
                  <div className="p-5 text-center">
                    <div className="text-2xl mb-2">{step.icon}</div>
                    <div className="text-[13px] font-semibold text-white leading-tight">{step.label}</div>
                    {step.sub && (
                      <div className="text-[11px] text-slate-500 mt-1 font-mono">{step.sub}</div>
                    )}
                  </div>
                </div>
                {/* Arrow */}
                {i < PIPELINE.length - 1 && (
                  <div className="flex-shrink-0 text-slate-700 px-2 md:px-3 text-base hidden md:block select-none">→</div>
                )}
                {i < PIPELINE.length - 1 && (
                  <div className="flex-shrink-0 text-slate-700 py-1 text-base block md:hidden self-center select-none">↓</div>
                )}
              </div>
            ))}
          </div>

          {/* Detail cards */}
          <div className="mt-5 grid grid-cols-1 md:grid-cols-3 gap-3">
            {[
              { icon: '🧠', title: 'Semantic Search',  desc: 'text-embedding-3-small + Qdrant cosine similarity for concept-level retrieval' },
              { icon: '🔤', title: 'Keyword Search',   desc: 'BM25 sparse retrieval for exact term matching and high-recall search' },
              { icon: '💾', title: 'Agent Memory',     desc: 'Per-user conversation history enabling coherent multi-turn interactions' },
            ].map(d => (
              <div key={d.title} className="bg-white/[0.03] rounded-xl p-4 border border-white/[0.07]">
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="text-base">{d.icon}</span>
                  <span className="text-[13px] font-semibold text-white">{d.title}</span>
                </div>
                <p className="text-[12px] text-slate-500 leading-relaxed">{d.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Specialist Agents ── */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-12">
        <div className="text-center mb-14">
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-indigo-400 mb-3">Specialist Agents</div>
          <h2 className="text-3xl md:text-4xl font-bold">Domain Experts, Powered by GPT-4</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-6">

          {/* CFO Agent */}
          <div className="relative overflow-hidden rounded-3xl border border-white/[0.08] hover:border-blue-500/30 transition-all duration-300 bg-gradient-to-br from-blue-500/[0.05] via-transparent to-transparent">
            <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-blue-500/60 to-transparent" />
            <div className="p-8">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-14 h-14 rounded-2xl bg-blue-500/[0.15] border border-blue-500/25 flex items-center justify-center text-3xl shadow-xl shadow-blue-500/10">
                  💼
                </div>
                <div>
                  <h3 className="text-xl font-bold">CFO Agent</h3>
                  <p className="text-slate-400 text-sm mt-0.5">Financial Intelligence · GPT-4 Turbo</p>
                </div>
              </div>

              <div className="space-y-2.5 mb-7">
                {[
                  'Revenue & expense deep-dive analysis',
                  'Profit margin calculation & benchmarking',
                  'Multi-month revenue forecasting',
                  'Budget optimization recommendations',
                ].map(c => (
                  <div key={c} className="flex items-start gap-2.5 text-[13.5px] text-slate-300">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-400 flex-shrink-0 mt-1.5" />
                    {c}
                  </div>
                ))}
              </div>

              <div className="border-t border-white/[0.08] pt-5">
                <div className="text-[10.5px] text-slate-500 font-semibold uppercase tracking-wider mb-3">ReAct Tool Calls</div>
                <div className="flex flex-wrap gap-2">
                  {['query_revenue()', 'query_expenses()', 'calculate_profit_margin()', 'forecast_revenue()'].map(t => (
                    <span key={t} className="text-[11px] px-2.5 py-1 rounded-md bg-blue-500/10 text-blue-300 border border-blue-500/20 font-mono hover:bg-blue-500/20 transition-colors">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* CRO Agent */}
          <div className="relative overflow-hidden rounded-3xl border border-white/[0.08] hover:border-purple-500/30 transition-all duration-300 bg-gradient-to-br from-purple-500/[0.05] via-transparent to-transparent">
            <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-purple-500/60 to-transparent" />
            <div className="p-8">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-14 h-14 rounded-2xl bg-purple-500/[0.15] border border-purple-500/25 flex items-center justify-center text-3xl shadow-xl shadow-purple-500/10">
                  📈
                </div>
                <div>
                  <h3 className="text-xl font-bold">CRO Agent</h3>
                  <p className="text-slate-400 text-sm mt-0.5">Revenue Marketing · GPT-4 Turbo</p>
                </div>
              </div>

              <div className="space-y-2.5 mb-7">
                {[
                  'Campaign performance analysis by channel',
                  'ROAS comparison across Facebook, Instagram, Google',
                  'Customer acquisition cost (CAC) calculation',
                  'Marketing ROI & budget allocation strategy',
                ].map(c => (
                  <div key={c} className="flex items-start gap-2.5 text-[13.5px] text-slate-300">
                    <div className="w-1.5 h-1.5 rounded-full bg-purple-400 flex-shrink-0 mt-1.5" />
                    {c}
                  </div>
                ))}
              </div>

              <div className="border-t border-white/[0.08] pt-5">
                <div className="text-[10.5px] text-slate-500 font-semibold uppercase tracking-wider mb-3">ReAct Tool Calls</div>
                <div className="flex flex-wrap gap-2">
                  {['get_campaign_performance()', 'compare_channels()', 'calculate_cac()'].map(t => (
                    <span key={t} className="text-[11px] px-2.5 py-1 rounded-md bg-purple-500/10 text-purple-300 border border-purple-500/20 font-mono hover:bg-purple-500/20 transition-colors">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Tech Stack ── */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-16">
        <div className="text-center mb-10">
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-indigo-400 mb-3">Built With</div>
          <h2 className="text-3xl font-bold">Production-Grade Stack</h2>
        </div>
        <div className="flex flex-wrap gap-3 justify-center">
          {TECH.map(t => (
            <div
              key={t.name}
              className={`px-4 py-2.5 rounded-xl border text-[13px] font-medium flex flex-col items-center gap-0.5 hover:scale-105 transition-transform cursor-default ${t.cls}`}
            >
              <span>{t.name}</span>
              <span className="text-[10px] opacity-50">{t.cat}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 pb-24">
        <div className="relative overflow-hidden rounded-3xl border border-indigo-500/20 bg-gradient-to-br from-indigo-600/[0.14] to-violet-600/[0.07] p-14 text-center">
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-indigo-500/60 to-transparent" />
          <div className="absolute inset-0 [background-image:radial-gradient(circle_at_50%_0%,rgba(99,102,241,0.12),transparent_65%)] pointer-events-none" />
          <h2 className="text-3xl md:text-4xl font-bold mb-4 relative">See it in action</h2>
          <p className="text-slate-400 mb-8 max-w-md mx-auto relative text-[15px] leading-relaxed">
            Ask any financial or marketing question. Watch CFO and CRO agents collaborate
            in real-time with full reasoning traces.
          </p>
          <button
            onClick={() => setView('demo')}
            className="relative px-10 py-4 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold text-lg transition-all hover:shadow-[0_0_50px_rgba(99,102,241,0.5)] active:scale-[0.98]"
          >
            Launch Demo →
          </button>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="relative z-10 border-t border-white/[0.05] py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="text-sm text-slate-600">CampaignBrain — Multi-Agent RAG Orchestrator</div>
          <div className="text-sm text-slate-700">GPT-4 · FastAPI · Next.js · Qdrant · Railway + Vercel</div>
        </div>
      </footer>
    </div>
  );
}
