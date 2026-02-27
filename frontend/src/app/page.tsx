'use client';
import { useState } from 'react';

export default function Home() {
  const [showDemo, setShowDemo] = useState(false);
  const [messages, setMessages] = useState<Array<{role: string, content: string, agents?: string[]}>>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const exampleQueries = [
    {
      icon: '💰',
      title: 'Financial Analysis',
      query: 'What was our Q4 revenue?',
      description: 'Get detailed revenue breakdowns and growth metrics',
      gradient: 'from-blue-600 to-cyan-500'
    },
    {
      icon: '📊',
      title: 'Campaign Performance',
      query: 'How did our Facebook campaign perform?',
      description: 'Analyze ROAS, conversions, and ROI metrics',
      gradient: 'from-purple-600 to-pink-500'
    },
    {
      icon: '⚖️',
      title: 'Budget Planning',
      query: 'Can we afford to increase marketing spend?',
      description: 'Multi-agent coordination for strategic decisions',
      gradient: 'from-orange-600 to-red-500'
    },
    {
      icon: '🔍',
      title: 'Channel Comparison',
      query: 'Compare Facebook vs Instagram performance',
      description: 'Side-by-side analysis of marketing channels',
      gradient: 'from-green-600 to-teal-500'
    }
  ];

  const features = [
    { icon: '🤖', title: 'Multi-Agent AI', desc: 'CFO + CRO agents working together' },
    { icon: '⚡', title: 'Real-Time', desc: 'Instant analysis and insights' },
    { icon: '📈', title: 'Data-Driven', desc: 'Powered by real financial APIs' },
    { icon: '🎯', title: 'Context-Aware', desc: 'Remembers conversation history' }
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('https://aware-trust-production-734d.up.railway.app/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage, user_id: 'demo' })
      });

      const data = await response.json();
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.answer || 'No response',
        agents: data.agents_used || []
      }]);
    } catch (err: any) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Error: ' + err.message
      }]);
    }
    
    setLoading(false);
  };

  const tryExample = (query: string) => {
    setShowDemo(true);
    setInput(query);
    setTimeout(() => {
      const event = new Event('submit', { bubbles: true, cancelable: true });
      document.querySelector('form')?.dispatchEvent(event);
    }, 100);
  };

  if (!showDemo) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white overflow-hidden">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-20 w-72 h-72 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
        </div>

        <div className="relative z-10 container mx-auto px-6 pt-20 pb-16">
          <div className="text-center mb-16">
            <div className="inline-block mb-6">
              <div className="text-7xl mb-4">🧠</div>
            </div>
            <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              CampaignBrain
            </h1>
            <p className="text-2xl md:text-3xl text-slate-300 mb-4">
              Multi-Agent AI Assistant
            </p>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-8">
              Specialized AI agents working together to provide financial analysis and marketing insights. 
              Built with FastAPI, Next.js, and OpenAI GPT-4.
            </p>
            
            <div className="flex gap-4 justify-center mb-12">
              <button
                onClick={() => setShowDemo(true)}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 rounded-xl font-bold text-lg transition-all transform hover:scale-105 shadow-lg"
              >
                Try Live Demo →
              </button>
              <button
                onClick={() => window.open('https://github.com/sanjana-3002/Multi-Agent-Rag-Orchestrator', '_blank')}
                className="px-8 py-4 bg-slate-800/50 hover:bg-slate-700/50 border border-slate-600 rounded-xl font-bold text-lg transition-all"
              >
                View on GitHub
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {features.map((feature, idx) => (
              <div key={idx} className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-2xl p-6 hover:border-blue-500 transition-all">
                <div className="text-4xl mb-3">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-slate-400 text-sm">{feature.desc}</p>
              </div>
            ))}
          </div>

          <div className="mb-16">
            <h2 className="text-3xl font-bold text-center mb-8">Try These Examples</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
              {exampleQueries.map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => tryExample(example.query)}
                  className={`group relative bg-gradient-to-br ${example.gradient} p-[2px] rounded-2xl overflow-hidden transition-all transform hover:scale-105`}
                >
                  <div className="bg-slate-900 rounded-2xl p-6 h-full">
                    <div className="flex items-start gap-4">
                      <div className="text-5xl">{example.icon}</div>
                      <div className="flex-1 text-left">
                        <h3 className="text-xl font-bold mb-2">{example.title}</h3>
                        <p className="text-sm text-slate-400 mb-3">{example.description}</p>
                        <p className="text-sm text-blue-300 font-mono">{example.query}</p>
                      </div>
                      <div className="text-slate-400 group-hover:text-white transition-colors">→</div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div className="text-center max-w-4xl mx-auto">
            <h3 className="text-xl font-bold mb-4 text-slate-400">Built With</h3>
            <div className="flex flex-wrap justify-center gap-4">
              {['Next.js', 'FastAPI', 'OpenAI GPT-4', 'TypeScript', 'Tailwind CSS', 'Railway', 'Vercel'].map(tech => (
                <span key={tech} className="px-4 py-2 bg-slate-800/50 border border-slate-700 rounded-lg text-sm">
                  {tech}
                </span>
              ))}
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <div className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              🧠 CampaignBrain
            </h1>
            <p className="text-gray-400">Multi-Agent AI Assistant</p>
          </div>
          <button
            onClick={() => { setShowDemo(false); setMessages([]); }}
            className="px-6 py-3 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded-xl transition-all"
          >
            ← Back to Home
          </button>
        </div>

        <div className="bg-gray-800/50 backdrop-blur rounded-2xl p-6 mb-4 min-h-[500px] border border-gray-700">
          {messages.length === 0 && (
            <div className="text-center py-20 text-gray-400">
              <div className="text-6xl mb-4">👋</div>
              <p className="text-lg">Ask me anything about revenue, campaigns, or marketing!</p>
            </div>
          )}
          
          {messages.map((msg, i) => (
            <div key={i} className={`mb-4 p-5 rounded-xl ${
              msg.role === 'user' ? 'bg-blue-600 ml-auto max-w-[85%]' : 'bg-gray-700/80 mr-auto max-w-[85%]'
            }`}>
              <div className="font-bold text-sm mb-2 opacity-75">
                {msg.role === 'user' ? '👤 You' : '🤖 Assistant'}
              </div>
              <div className="whitespace-pre-wrap">{msg.content}</div>
              {msg.agents && msg.agents.length > 0 && (
                <div className="mt-3 flex gap-2">
                  {msg.agents.map((agent, idx) => (
                    <span key={idx} className="px-3 py-1 bg-blue-500/30 rounded-full text-xs font-semibold">
                      {agent.toUpperCase()}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
          
          {loading && (
            <div className="text-center py-4">
              <div className="inline-flex items-center gap-2 text-gray-400">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                <span className="ml-2">Thinking...</span>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about revenue, campaigns, or marketing insights..."
            disabled={loading}
            className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-5 py-4 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
          />
          <button 
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-gray-700 disabled:to-gray-700 px-10 py-4 rounded-xl font-bold transition-all disabled:cursor-not-allowed"
          >
            {loading ? '...' : 'Send'}
          </button>
        </form>
      </div>
    </main>
  );
}
