import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import { sendChatMessage } from '../api/chatApi';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);

    try {
      const data = await sendChatMessage(currentInput);
      const assistantMessage = { role: 'assistant', content: data.answer };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please check if the backend is running.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full">
      {/* Messages Area - Full width for scrollbar placement */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto custom-scrollbar"
      >
        <div className="max-w-4xl mx-auto p-4 space-y-6 w-full">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-64 text-center space-y-4 opacity-80 mt-20">
               <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center text-accent">
                  <Bot size={32} />
               </div>
               <h2 className="text-2xl font-bold font-condensed tracking-wider">NEXT REP</h2>
               <p className="max-w-sm text-gray-400 text-sm">
                 Your AI fitness coach. Ask me about training, nutrition, or recovery.
               </p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div 
              key={i}
              className={cn(
                "flex gap-4 animate-in fade-in slide-in-from-bottom-2 duration-300",
                msg.role === 'user' ? "justify-end" : "justify-start"
              )}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center text-accent shrink-0">
                  <Bot size={18} />
                </div>
              )}
              
              <div className={cn(
                "max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed",
                msg.role === 'user' 
                  ? "bg-card border border-white/10 text-accent rounded-br-none shadow-[0_4px_15px_rgba(0,245,212,0.05)]" 
                  : "text-gray-200 prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-li:my-1"
              )}>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center text-gray-400 shrink-0 border border-white/10">
                  <User size={18} />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-4 justify-start">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center text-accent shrink-0 animate-pulse">
                <Bot size={18} />
              </div>
              <div className="p-4 flex items-center gap-2 text-gray-500 italic text-sm">
                <Loader2 className="animate-spin" size={16} />
                Next Rep is thinking...
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input Area - Sticky at bottom */}
      <div className="p-4 bg-black/50 backdrop-blur-md border-t border-white/5 shrink-0">
        <div className="max-w-4xl mx-auto w-full">
          <form 
            onSubmit={handleSubmit}
            className="relative"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask Next Rep anything about fitness..."
              className="w-full bg-card border border-white/10 rounded-xl py-4 pl-4 pr-14 focus:outline-none focus:border-accent/50 focus:ring-1 focus:ring-accent/20 transition-all text-white"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-accent text-black rounded-lg hover:bg-accent/90 disabled:opacity-50 disabled:hover:bg-accent transition-all shadow-[0_0_15px_rgba(0,245,212,0.3)]"
            >
              <Send size={20} />
            </button>
          </form>
          <p className="text-center text-[10px] text-gray-600 mt-2">
            Next Rep provides general guidance. Consult a professional for medical advice.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
