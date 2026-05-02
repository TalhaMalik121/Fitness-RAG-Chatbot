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

  const starterPrompts = [
    { title: "Building Muscle", desc: "Best routine for hypertrophy?", icon: "💪" },
    { title: "Fat Loss", desc: "How to stay in a calorie deficit?", icon: "🔥" },
    { title: "Recovery", desc: "Optimize sleep and rest days", icon: "🌙" },
    { title: "Nutrition", desc: "Top protein sources for vegans", icon: "🥦" },
  ];

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, [messages, isLoading]);

  const handleSubmit = async (e, customInput) => {
    if (e) e.preventDefault();
    const queryText = customInput || input;
    if (!queryText.trim() || isLoading) return;

    const userMessage = { role: 'user', content: queryText };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await sendChatMessage(queryText);
      const assistantMessage = { role: 'assistant', content: data.answer };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: '### Connection Issue\nI encountered an error connecting to the server. Please ensure the backend is active.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full relative">
      {/* Messages Area */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto custom-scrollbar px-4 pt-8 pb-32"
      >
        <div className="max-w-3xl mx-auto space-y-8 w-full">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center min-h-[60vh] text-center space-y-8 animate-in fade-in zoom-in duration-700">
               <div className="relative">
                 <div className="absolute inset-0 bg-amber-500/20 blur-3xl rounded-full"></div>
                 <div className="relative w-24 h-24 glass-panel rounded-3xl flex items-center justify-center text-amber-500 shadow-2xl animate-float">
                    <Bot size={48} />
                 </div>
               </div>
               
               <div className="space-y-2">
                 <h2 className="text-4xl font-black font-condensed tracking-[0.075em] text-white glow-text uppercase">How can I help?</h2>
                 <p className="max-w-sm text-slate-400 text-sm leading-relaxed">
                   Your elite AI fitness consultant. Select a topic or type your query below.
                 </p>
               </div>

               <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl mt-8">
                 {starterPrompts.map((p, i) => (
                   <button 
                    key={i}
                    onClick={() => handleSubmit(null, p.desc)}
                    className="premium-card p-5 rounded-2xl text-left group transition-all active:scale-[0.98]"
                   >
                     <span className="text-2xl mb-3 block">{p.icon}</span>
                     <h4 className="text-white font-bold text-sm group-hover:text-amber-500 transition-colors">{p.title}</h4>
                     <p className="text-slate-500 text-xs mt-1">{p.desc}</p>
                   </button>
                 ))}
               </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div 
              key={i}
              className={cn(
                "flex gap-4 group",
                msg.role === 'user' ? "justify-end" : "justify-start"
              )}
            >
              {msg.role === 'assistant' && (
                <div className="w-10 h-10 rounded-xl glass-panel flex items-center justify-center text-amber-500 shrink-0 mt-1 shadow-lg">
                  <Bot size={20} />
                </div>
              )}
              
              <div className={cn(
                "max-w-[85%] p-6 rounded-3xl text-sm leading-relaxed relative transition-all duration-500",
                msg.role === 'user' 
                  ? "bg-amber-600/10 backdrop-blur-xl border border-amber-500/20 text-amber-100 rounded-tr-none shadow-[0_10px_40px_rgba(245,158,11,0.1)]" 
                  : "bg-white/[0.02] backdrop-blur-2xl border border-white/10 text-slate-200 prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-strong:text-amber-400 prose-ul:list-disc rounded-tl-none shadow-[0_20px_50px_rgba(0,0,0,0.3)]"
              )}>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
                {msg.role === 'user' && (
                  <div className="absolute -right-2 top-0 w-2 h-2 bg-amber-600/20 border-r border-t border-amber-500/20 rounded-tr-sm"></div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-10 h-10 rounded-xl glass-panel flex items-center justify-center text-slate-400 shrink-0 mt-1 shadow-lg">
                  <User size={20} />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-4 justify-start animate-pulse">
              <div className="w-10 h-10 rounded-xl glass-panel flex items-center justify-center text-amber-500 shrink-0 shadow-lg">
                <Bot size={20} />
              </div>
              <div className="premium-card px-6 py-4 rounded-2xl rounded-tl-none flex items-center gap-3 text-slate-400 italic text-sm">
                <div className="flex gap-1">
                  <div className="w-1.5 h-1.5 bg-amber-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="w-1.5 h-1.5 bg-amber-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-1.5 h-1.5 bg-amber-500 rounded-full animate-bounce"></div>
                </div>
                Analysing data...
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-[#020617] via-[#020617]/95 to-transparent pb-10">
        <div className="max-w-3xl mx-auto w-full relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-amber-500/20 to-blue-500/20 rounded-2xl blur opacity-0 group-focus-within:opacity-100 transition duration-1000"></div>
          <form 
            onSubmit={handleSubmit}
            className="relative flex items-center gap-2"
          >
            <div className="relative flex-1">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Message Fitness Coach..."
                className="w-full glass-panel bg-white/[0.03] hover:bg-white/[0.05] rounded-2xl py-5 pl-6 pr-16 focus:outline-none focus:ring-2 focus:ring-amber-500/40 focus:border-amber-500/40 transition-all text-white placeholder-slate-500 shadow-2xl"
              />
              <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
                <button
                  type="submit"
                  disabled={!input.trim() || isLoading}
                  className="p-3 bg-amber-500 text-black rounded-xl hover:bg-amber-400 disabled:opacity-30 disabled:hover:bg-amber-500 transition-all shadow-[0_0_20px_rgba(245,158,11,0.4)] active:scale-90"
                >
                  <Send size={20} />
                </button>
              </div>
            </div>
          </form>
          <p className="text-center text-[10px] text-slate-600 mt-4 tracking-wide uppercase font-bold">
            Powered by Llama 3.1 & Next Rep Engine
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
