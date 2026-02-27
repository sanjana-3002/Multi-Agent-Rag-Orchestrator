'use client';
import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState<Array<{role: string, content: string, agents?: string[]}>>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setLoading(true);

    try {
      console.log('🚀 Sending to Railway...');
      
      const response = await fetch('https://aware-trust-production-734d.up.railway.app/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage, user_id: 'demo' })
      });

      console.log('✅ Response:', response.status);

      const data = await response.json();
      console.log('📦 Data:', data);
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.answer || 'No response',
        agents: data.agents_used || []
      }]);
    } catch (err: any) {
      console.error('❌ Error:', err);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `Error: ${err.message}\n\nBackend: https://aware-trust-production-734d.up.railway.app`
      }]);
    }
    
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            🧠 CampaignBrain
          </h1>
          <p className="text-gray-400">Multi-Agent AI Assistant</p>
        </div>
        
        <div className="bg-gray-800/50 backdrop-blur rounded-2xl p-6 mb-4 min-h-[500px] border border-gray-700">
          {messages.length === 0 && (
            <div className="text-center py-20 text-gray-400">
              <div className="text-6xl mb-4">👋</div>
              <p className="text-lg">Ask me anything about revenue, campaigns, or marketing!</p>
              <p className="text-sm mt-2 opacity-50">Try: "What was our Q4 revenue?"</p>
            </div>
          )}
          
          {messages.map((msg, i) => (
            <div key={i} className={`mb-4 p-5 rounded-xl ${
              msg.role === 'user' 
                ? 'bg-blue-600 ml-auto max-w-[85%]' 
                : 'bg-gray-700/80 mr-auto max-w-[85%]'
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

        <div className="mt-4 text-center text-xs text-gray-500">
          Backend: https://aware-trust-production-734d.up.railway.app
        </div>
      </div>
    </main>
  );
}
