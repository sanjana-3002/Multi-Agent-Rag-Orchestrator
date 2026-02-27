'use client';
import { useState } from 'react';

// FORCE REBUILD - v2.0
export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setLoading(true);

    try {
      console.log('🚀 Sending to Railway backend...');
      
      // HARDCODED RAILWAY URL - NO ENVIRONMENT VARIABLE
      const response = await fetch('https://aware-trust-production-734d.up.railway.app/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage, user_id: 'demo' })
      });

      console.log('📡 Response status:', response.status);

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Data received:', data);
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.answer,
        agents: data.agents_used
      }]);
    } catch (err) {
      console.error('❌ Fetch error:', err);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `Error: ${err.message}\n\nTrying to reach: https://aware-trust-production-734d.up.railway.app/query\n\nCheck browser console for details.`
      }]);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">🧠 CampaignBrain v2.0</h1>
          <p className="text-slate-400 text-sm">Backend: https://aware-trust-production-734d.up.railway.app</p>
        </div>
        
        <div className="bg-slate-800 rounded-lg p-6 mb-4 min-h-[500px]">
          {messages.length === 0 && (
            <div className="text-center text-slate-400 py-20">
              <div className="text-6xl mb-4">👋</div>
              <p>Ask me anything about revenue or campaigns!</p>
            </div>
          )}
          
          {messages.map((msg, i) => (
            <div key={i} className={`mb-4 p-4 rounded-lg ${
              msg.role === 'user' ? 'bg-blue-600 ml-auto max-w-[80%]' : 'bg-slate-700 mr-auto max-w-[80%]'
            }`}>
              <div className="font-bold text-sm mb-2">
                {msg.role === 'user' ? '👤 You' : '🤖 Assistant'}
              </div>
              <div className="whitespace-pre-wrap text-sm">{msg.content}</div>
              {msg.agents && (
                <div className="mt-2 flex gap-2">
                  {msg.agents.map((agent, idx) => (
                    <span key={idx} className="px-2 py-1 bg-blue-500/30 rounded text-xs">
                      {agent}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
          
          {loading && (
            <div className="text-center text-slate-400 py-4">
              <div className="inline-block animate-pulse">⏳ Thinking...</div>
            </div>
          )}
        </div>

        <form onSubmit={sendMessage} className="flex gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="What was our Q4 revenue?"
            disabled={loading}
            className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 px-8 py-3 rounded-lg font-semibold transition-colors"
          >
            {loading ? '...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
}
