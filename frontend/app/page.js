'use client';
import { useState, useRef, useEffect } from 'react';

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    setMessages(prev => [...prev, { role: 'user', content: input }]);
    const query = input;
    setInput('');
    setLoading(true);

    try {
      const API_URL = 'https://aware-trust-production-734d.up.railway.app';
      
      console.log('🔗 Connecting to:', API_URL); // Debug log
      
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, user_id: 'demo' })
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
      }

      const data = await response.json(); // ✅ FIXED - was "res.json()"
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.answer, 
        agents: data.agents_used,
        time: data.execution_time
      }]);
    } catch (err) {
      console.error('❌ Error:', err);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `❌ Error: ${err.message}\n\nBackend URL: ${process.env.NEXT_PUBLIC_API_URL || 'Not Set'}\n\nMake sure NEXT_PUBLIC_API_URL environment variable is set in Vercel.`,
        error: true
      }]);
    }
    setLoading(false);
  };

  const exampleQueries = [
    { icon: '💰', category: 'Finance', color: 'blue', text: 'What was our Q4 revenue?' },
    { icon: '📊', category: 'Marketing', color: 'green', text: 'How did Facebook campaign perform?' },
    { icon: '🤝', category: 'Multi-Agent', color: 'purple', text: 'Can we afford to increase marketing spend?' },
    { icon: '⚖️', category: 'Analysis', color: 'orange', text: 'Compare Facebook vs Instagram performance' },
  ];

  const colorMap = {
    blue: 'from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400',
    green: 'from-green-600 to-green-500 hover:from-green-500 hover:to-green-400',
    purple: 'from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400',
    orange: 'from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400',
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      
      {/* Header */}
      <header className="bg-slate-800/80 backdrop-blur-xl border-b border-slate-700/50 px-6 py-5 shadow-2xl">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xl shadow-lg">
              🧠
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                CampaignBrain
              </h1>
              <p className="text-xs text-slate-400">Multi-Agent AI Assistant</p>
            </div>
          </div>
          <button 
            onClick={() => setMessages([])}
            className="px-4 py-2 bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 rounded-lg text-sm transition-all border border-slate-600/50"
          >
            Clear Chat
          </button>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-8">
        <div className="max-w-5xl mx-auto space-y-6">
          
          {/* Welcome Screen */}
          {messages.length === 0 && (
            <div className="text-center py-16 animate-fade-in">
              <div className="text-7xl mb-6 animate-bounce-slow">🚀</div>
              <h2 className="text-4xl font-bold text-white mb-3">
                Welcome to CampaignBrain
              </h2>
              <p className="text-slate-400 text-lg mb-12 max-w-2xl mx-auto">
                Your AI-powered business intelligence assistant. Ask about finances, 
                marketing campaigns, or get multi-agent analysis.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto">
                {exampleQueries.map((query, idx) => (
                  <button
                    key={idx}
                    onClick={() => setInput(query.text)}
                    className={`group p-6 bg-gradient-to-br ${colorMap[query.color]} rounded-2xl text-left transition-all transform hover:scale-105 hover:shadow-2xl border border-white/10`}
                  >
                    <div className="flex items-start gap-4">
                      <div className="text-4xl">{query.icon}</div>
                      <div className="flex-1">
                        <div className="text-sm font-bold text-white/80 mb-2">{query.category}</div>
                        <div className="text-white font-medium">{query.text}</div>
                      </div>
                      <div className="text-white/50 group-hover:text-white/80 transition-colors">→</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
            >
              <div
                className={`max-w-[85%] rounded-2xl px-6 py-4 shadow-lg ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-br from-blue-600 to-blue-500 text-white'
                    : msg.error
                    ? 'bg-gradient-to-br from-red-900/50 to-red-800/50 text-white border border-red-700/50'
                    : 'bg-gradient-to-br from-slate-800 to-slate-700 text-white border border-slate-600/50'
                }`}
              >
                {msg.role === 'assistant' && msg.agents && (
                  <div className="flex items-center gap-2 mb-3 pb-3 border-b border-white/10">
                    {msg.agents.map((agent, i) => (
                      <span
                        key={i}
                        className={`px-3 py-1 rounded-full text-xs font-bold ${
                          agent.toLowerCase() === 'cfo'
                            ? 'bg-blue-500/30 text-blue-200 border border-blue-400/30'
                            : 'bg-green-500/30 text-green-200 border border-green-400/30'
                        }`}
                      >
                        {agent.toUpperCase()}
                      </span>
                    ))}
                    {msg.time && (
                      <span className="ml-auto text-xs text-slate-400">
                        ⚡ {msg.time.toFixed(1)}s
                      </span>
                    )}
                  </div>
                )}
                <div className="text-[15px] leading-relaxed whitespace-pre-wrap">{msg.content}</div>
              </div>
            </div>
          ))}

          {/* Loading */}
          {loading && (
            <div className="flex justify-start animate-slide-up">
              <div className="bg-gradient-to-br from-slate-800 to-slate-700 border border-slate-600/50 rounded-2xl px-6 py-4 shadow-lg">
                <div className="flex items-center gap-3">
                  <div className="flex gap-1">
                    <div className="w-2.5 h-2.5 bg-blue-400 rounded-full animate-bounce"></div>
                    <div className="w-2.5 h-2.5 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2.5 h-2.5 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                  <span className="text-slate-300 text-sm font-medium">Analyzing...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-slate-800/80 backdrop-blur-xl border-t border-slate-700/50 px-6 py-5 shadow-2xl">
        <form onSubmit={sendMessage} className="max-w-5xl mx-auto">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about revenue, campaigns, or get strategic insights..."
              disabled={loading}
              className="flex-1 bg-slate-900/50 border border-slate-700/50 rounded-xl px-5 py-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white rounded-xl font-semibold transition-all shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
            >
              {loading ? '...' : 'Send'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}