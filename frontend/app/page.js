'use client';
import { useState } from 'react';

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
      console.log('🔗 Fetching from Railway...');
      
      const response = await fetch('https://aware-trust-production-734d.up.railway.app/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage, user_id: 'demo' })
      });

      console.log('✅ Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Data received:', data);
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.answer,
        agents: data.agents_used
      }]);
    } catch (err) {
      console.error('❌ Error:', err);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `❌ Error: ${err.message}\n\nBackend URL: https://aware-trust-production-734d.up.railway.app`
      }]);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">🧠 CampaignBrain</h1>
        
        <div className="bg-slate-800 rounded-lg p-6 mb-4 min-h-[400px]">
          {messages.map((msg, i) => (
            <div key={i} className={`mb-4 p-4 rounded ${
              msg.role === 'user' ? 'bg-blue-600' : 'bg-slate-700'
            }`}>
              <div className="font-bold mb-2">
                {msg.role === 'user' ? '👤 You' : '🤖 Assistant'}
              </div>
              <div className="whitespace-pre-wrap">{msg.content}</div>
              {msg.agents && (
                <div className="mt-2 text-sm text-slate-300">
                  Agents: {msg.agents.join(', ')}
                </div>
              )}
            </div>
          ))}
          {loading && <div className="text-center">⏳ Thinking...</div>}
        </div>

        <form onSubmit={sendMessage} className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about revenue, campaigns, etc..."
            className="flex-1 bg-slate-800 border border-slate-700 rounded px-4 py-3 text-white"
          />
          <button 
            type="submit" 
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 px-6 py-3 rounded font-semibold"
          >
            {loading ? '...' : 'Send'}
          </button>
        </form>

        <div className="mt-4 text-sm text-slate-400">
          Backend: https://aware-trust-production-734d.up.railway.app
        </div>
      </div>
    </div>
  );
}
