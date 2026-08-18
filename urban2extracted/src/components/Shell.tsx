import { useState } from 'react';
import { navItems, PageId } from './navItems';
import { UrbanEyeLogo, SwachhBharatLogo } from './Logos';
import { Menu, X, LogIn } from 'lucide-react';

interface Props {
  active: PageId;
  onNavigate: (p: PageId) => void;
  children: React.ReactNode;
}

export function Shell({ active, onNavigate, children }: Props) {
  const [open, setOpen] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const activeLabel = navItems.find((n) => n.id === active)?.label ?? '';

  const LoginModal = () => (
    <div className="fixed inset-0 z-[60] grid place-items-center p-4">
      <div className="absolute inset-0 bg-slate-900/50" onClick={() => setShowLogin(false)} />
      <div className="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-soft">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2"><LogIn className="h-5 w-5 text-primary" /><span className="font-semibold text-slate-800">Citizen Login</span></div>
          <button onClick={() => setShowLogin(false)} className="text-slate-400 hover:text-slate-600"><X className="h-5 w-5" /></button>
        </div>
        <p className="mt-1 text-xs text-slate-400">Track your complaints and get resolution updates.</p>
        <form onSubmit={(e) => { e.preventDefault(); setShowLogin(false); }} className="mt-4 space-y-3">
          <div>
            <label className="text-xs font-medium text-slate-600">Email or mobile number</label>
            <input type="text" required placeholder="you@example.com" className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-600">Password</label>
            <input type="password" required placeholder="•••••••" className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
          </div>
          <button type="submit" className="w-full rounded-xl bg-primary py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary-dark">Login</button>
          <p className="text-center text-xs text-slate-400">New here? <span className="font-semibold text-primary">Create an account</span></p>
        </form>
      </div>
    </div>
  );

  const NavList = () => (
    <nav className="flex flex-col gap-1 px-3">
      {navItems.map((n) => {
        const Icon = n.icon;
        const isActive = n.id === active;
        return (
          <button
            key={n.id}
            onClick={() => { onNavigate(n.id); setOpen(false); }}
            className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all ${
              isActive
                ? 'bg-white/15 text-white shadow-sm'
                : 'text-white/70 hover:bg-white/10 hover:text-white'
            }`}
          >
            <Icon className={`h-[18px] w-[18px] ${isActive ? 'text-accent' : ''}`} />
            {n.label}
          </button>
        );
      })}
    </nav>
  );

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Sidebar - desktop */}
      <aside className="hidden lg:flex w-64 flex-col bg-sidebar text-white shrink-0">
        <div className="flex items-center gap-3 px-5 py-5 border-b border-white/10">
          <UrbanEyeLogo className="h-10 w-10" />
          <div>
            <div className="font-semibold leading-tight">UrbanEye</div>
            <div className="text-[11px] text-white/60">AI Urban Monitoring</div>
          </div>
        </div>
        <div className="flex-1 overflow-y-auto py-4"><NavList /></div>
        <div className="px-4 py-4 border-t border-white/10">
          <div className="flex items-center gap-3 rounded-xl bg-white/95 p-3">
            <SwachhBharatLogo className="h-11 w-11" />
            <div className="leading-tight">
              <div className="text-[12px] font-bold text-primary">Swachh Bharat</div>
              <div className="text-[10px] text-slate-500">Urban Mission</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Mobile header */}
      <div className="lg:hidden fixed top-0 inset-x-0 z-40 flex items-center justify-between bg-sidebar px-4 py-3 text-white">
        <div className="flex items-center gap-2">
          <UrbanEyeLogo className="h-8 w-8" />
          <span className="font-semibold">UrbanEye</span>
        </div>
        <button onClick={() => setOpen(true)} className="p-1.5 rounded-lg hover:bg-white/10"><Menu className="h-5 w-5" /></button>
        <button onClick={() => setShowLogin(true)} className="inline-flex items-center gap-1.5 rounded-lg bg-white/10 px-2.5 py-1.5 text-xs font-semibold text-white hover:bg-white/20"><LogIn className="h-4 w-4" /> Login</button>
      </div>

      {/* Mobile drawer */}
      {open && (
        <div className="lg:hidden fixed inset-0 z-50 flex">
          <div className="absolute inset-0 bg-black/50" onClick={() => setOpen(false)} />
          <aside className="relative w-72 bg-sidebar text-white flex flex-col">
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
              <div className="flex items-center gap-2">
                <UrbanEyeLogo className="h-8 w-8" />
                <span className="font-semibold">UrbanEye</span>
              </div>
              <button onClick={() => setOpen(false)} className="p-1.5 rounded-lg hover:bg-white/10"><X className="h-5 w-5" /></button>
            </div>
            <div className="flex-1 overflow-y-auto py-4"><NavList /></div>
            <div className="px-4 py-4 border-t border-white/10">
              <div className="flex items-center gap-3 rounded-xl bg-white/95 p-3">
                <SwachhBharatLogo className="h-11 w-11" />
                <div className="leading-tight">
                  <div className="text-[12px] font-bold text-primary">Swachh Bharat</div>
                  <div className="text-[10px] text-slate-500">Urban Mission</div>
                </div>
              </div>
            </div>
          </aside>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 min-w-0 flex flex-col">
        <header className="hidden lg:flex items-center justify-between border-b bg-white px-8 py-4">
          <div>
            <h1 className="text-lg font-semibold text-slate-800">{activeLabel}</h1>
            <p className="text-xs text-slate-400">Smart City Command Center · Indore Pilot</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2 text-xs text-slate-500">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              System Online
            </div>
            <button onClick={() => setShowLogin(true)} className="inline-flex items-center gap-2 rounded-xl border border-primary/30 bg-primary/10 px-3 py-1.5 text-sm font-semibold text-primary transition-colors hover:bg-primary hover:text-white">
              <LogIn className="h-4 w-4" /> Login
            </button>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-4 lg:p-8 pt-20 lg:pt-8">{children}</main>
      </div>
      {showLogin && <LoginModal />}
    </div>
  );
}
