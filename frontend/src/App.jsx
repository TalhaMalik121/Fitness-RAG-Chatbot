import React, { useState } from 'react'
import ChatBox from './components/ChatBox'
import { Dumbbell, History, Plus, Settings, Info } from 'lucide-react'

function App() {
  const [history] = useState([
    "Hypertrophy training basics",
    "Keto vs Paleo comparison",
    "Recovery for athletes"
  ])

  return (
    <div className="flex h-screen bg-[#020617] text-slate-200 overflow-hidden font-sans relative">
      {/* Background Decorative Glows */}
      <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-amber-500/10 rounded-full blur-[120px] bg-glow pointer-events-none"></div>
      <div className="absolute bottom-[-10%] left-[-10%] w-[400px] h-[400px] bg-blue-600/10 rounded-full blur-[100px] bg-glow pointer-events-none"></div>

      {/* Sidebar */}
      <aside className="w-72 glass-panel flex flex-col shrink-0 hidden md:flex relative z-10">
        <div className="p-8">
          <div className="flex items-center gap-4 group cursor-pointer">
            <div className="w-12 h-12 bg-gradient-to-br from-amber-400 to-amber-600 rounded-2xl flex items-center justify-center text-black shadow-[0_0_30px_rgba(245,158,11,0.3)] group-hover:scale-110 transition-transform duration-500">
              <Dumbbell size={28} />
            </div>
            <div>
              <h1 className="font-condensed font-black tracking-[0.1em] text-2xl leading-none text-white glow-text">FITNESS</h1>
              <span className="text-[11px] uppercase tracking-[0.3em] text-amber-500/80 font-bold">COACH AI</span>
            </div>
          </div>
        </div>

        <div className="flex-1 px-6 py-2 space-y-10 overflow-y-auto custom-scrollbar">
          <button className="w-full bg-white/5 hover:bg-white/10 text-white border border-white/10 font-semibold py-3.5 rounded-2xl flex items-center justify-center gap-3 transition-all duration-300 active:scale-95">
            <Plus size={20} className="text-amber-500" />
            New Session
          </button>

          <div>
            <h3 className="px-2 text-[10px] uppercase tracking-[0.2em] text-slate-500 font-bold mb-5 flex items-center gap-2">
              <History size={14} />
              Recent Consultations
            </h3>
            <div className="space-y-2">
              {history.map((item, i) => (
                <button key={i} className="w-full text-left px-4 py-3 text-sm text-slate-400 hover:text-white hover:bg-white/[0.03] border border-transparent hover:border-white/5 rounded-xl transition-all truncate">
                  {item}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="p-6 mt-auto space-y-4">
          {/* SaaS Usage Card */}
          <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-md">
            <div className="flex justify-between items-center mb-2">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Plan Usage</span>
              <span className="text-[10px] font-bold text-amber-500">80%</span>
            </div>
            <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
              <div className="w-[80%] h-full bg-gradient-to-r from-amber-500 to-orange-500 shadow-[0_0_10px_rgba(245,158,11,0.5)]"></div>
            </div>
            <p className="text-[9px] text-slate-500 mt-2">4/5 premium queries remaining</p>
          </div>

          <button className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-slate-500 hover:text-white transition-all group">
            <Settings size={18} className="group-hover:rotate-90 transition-transform duration-500" />
            Settings
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-slate-500 hover:text-white transition-all">
            <Info size={18} />
            Help & Support
          </button>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative z-10 overflow-hidden">
        {/* Mobile Header */}
        <header className="md:hidden h-20 border-b border-white/5 flex items-center px-8 glass-panel shrink-0">
          <h1 className="font-condensed font-bold tracking-tighter text-2xl text-amber-500 glow-text">FITNESS COACH</h1>
        </header>

        <ChatBox />
      </main>
    </div>
  )
}

export default App
