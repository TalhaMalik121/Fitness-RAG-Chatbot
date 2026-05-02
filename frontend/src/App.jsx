import React, { useState } from 'react'
import ChatBox from './components/ChatBox'
import { Dumbbell, History, Plus, Settings, Info } from 'lucide-react'

function App() {
  const [history] = useState([
    "How to build muscle?",
    "Best fat loss foods",
    "Rest day frequency"
  ])

  return (
    <div className="flex h-screen bg-black text-gray-200 overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-sidebar border-r border-white/5 flex flex-col shrink-0 hidden md:flex">
        <div className="p-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-accent rounded-xl flex items-center justify-center text-black shadow-[0_0_20px_rgba(0,245,212,0.3)]">
              <Dumbbell size={24} />
            </div>
            <div>
              <h1 className="font-condensed font-black tracking-tight text-2xl leading-none text-accent">NEXT REP</h1>
              <span className="text-[10px] uppercase tracking-[0.2em] text-gray-500 font-bold">Coach AI</span>
            </div>
          </div>
        </div>

        <div className="flex-1 px-4 py-2 space-y-8 overflow-y-auto custom-scrollbar">
          <button className="w-full bg-accent text-black font-bold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-accent/90 transition-all shadow-[0_0_15px_rgba(0,245,212,0.2)] mb-4">
            <Plus size={18} />
            New Session
          </button>

          <div>
            <h3 className="px-2 text-[11px] uppercase tracking-widest text-gray-500 font-bold mb-4 flex items-center gap-2">
              <History size={14} />
              Recent History
            </h3>
            <div className="space-y-1">
              {history.map((item, i) => (
                <button key={i} className="w-full text-left px-3 py-2 text-sm text-gray-400 hover:text-accent hover:bg-white/5 rounded-lg transition-all truncate">
                  {item}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-white/5 space-y-1">
          <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-500 hover:text-gray-300 transition-all">
            <Settings size={16} />
            Settings
          </button>
          <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-500 hover:text-gray-300 transition-all">
            <Info size={16} />
            Help & Support
          </button>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative">
        {/* Mobile Header */}
        <header className="md:hidden h-16 border-b border-white/5 flex items-center px-6 bg-sidebar shrink-0">
          <h1 className="font-condensed font-bold tracking-tighter text-xl text-accent">NEXT REP</h1>
        </header>

        <ChatBox />
      </main>
    </div>
  )
}

export default App
