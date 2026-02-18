'use client';

import { useState, useRef, useEffect } from 'react';

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_' + Math.random().toString(36).substr(2, 9));
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;

    // Add user message
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: input,
          user_id: userId
        })
      });

      const data = await response.json();

      // Add assistant message
      const assistantMessage = {
        role: 'assistant',
        content: data.answer,
        agents: data.agents_used,
        time: data.execution_time
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request.',
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = async () => {
    try {
      await fetch(`http://localhost:8000/history/${userId}`, {
        method: 'DELETE'
      });
      setMessages([]);
    } catch (error) {
      console.error('Error clearing history:', error);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">CampaignBrain</h1>
            <p className="text-sm text-gray-400">Multi-Agent AI Assistant</p>
          </div>
          <button
            onClick={clearHistory}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm transition-colors"
          >
            Clear History
          </button>
        </div>
      </header>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        <div className="max-w-4xl mx-auto space-y-4">
          
          {/* Welcome Message */}
          {messages.length === 0 && (
            <div className="text-center py-12">
              <h2 className="text-3xl font-bold text-white mb-4">
                Welcome to CampaignBrain 🧠
              </h2>
              <p className="text-gray-400 mb-8">
                Your AI-powered marketing & finance assistant
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                <button
                  onClick={() => setInput("What was our Q4 revenue?")}
                  className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-left transition-colors border border-gray-700"
                >
                  <div className="text-sm font-semibold text-blue-400 mb-1">💰 Finance</div>
                  <div className="text-white">What was our Q4 revenue?</div>
                </button>
                <button
                  onClick={() => setInput("How did our Facebook campaign perform?")}
                  className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-left transition-colors border border-gray-700"
                >
                  <div className="text-sm font-semibold text-green-400 mb-1">📊 Marketing</div>
                  <div className="text-white">How did Facebook perform?</div>
                </button>
                <button
                  onClick={() => setInput("Can we afford to increase marketing spend?")}
                  className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-left transition-colors border border-gray-700"
                >
                  <div className="text-sm font-semibold text-purple-400 mb-1">🤝 Multi-Agent</div>
                  <div className="text-white">Can we afford more marketing?</div>
                </button>
                <button
                  onClick={() => setInput("Compare Facebook vs Instagram performance")}
                  className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-left transition-colors border border-gray-700"
                >
                  <div className="text-sm font-semibold text-orange-400 mb-1">⚖️ Analysis</div>
                  <div className="text-white">Compare channels</div>
                </button>
              </div>
            </div>
          )}

          {/* Messages */}
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-6 py-4 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : message.error
                    ? 'bg-red-900 text-white border border-red-700'
                    : 'bg-gray-800 text-white border border-gray-700'
                }`}
              >
                {message.role === 'assistant' && message.agents && (
                  <div className="flex items-center gap-2 mb-2 text-xs">
                    <span className="text-gray-400">Agents:</span>
                    {message.agents.map((agent, i) => (
                      <span
                        key={i}
                        className={`px-2 py-1 rounded-full ${
                          agent.toLowerCase() === 'cfo'
                            ? 'bg-blue-900 text-blue-300'
                            : 'bg-green-900 text-green-300'
                        }`}
                      >
                        {agent.toUpperCase()}
                      </span>
                    ))}
                    {message.time && (
                      <span className="text-gray-500">
                        {message.time.toFixed(2)}s
                      </span>
                    )}
                  </div>
                )}
                <div className="whitespace-pre-wrap">{message.content}</div>
              </div>
            </div>
          ))}

          {/* Loading Indicator */}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 border border-gray-700 rounded-2xl px-6 py-4">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-gray-400 text-sm">Thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-gray-800 border-t border-gray-700 px-6 py-4">
        <form onSubmit={sendMessage} className="max-w-4xl mx-auto">
          <div className="flex gap-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about revenue, campaigns, or anything else..."
              className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition-colors"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}