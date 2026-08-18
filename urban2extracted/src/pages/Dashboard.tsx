import { useMemo } from 'react';
import { Card, StatCard, Badge, SectionTitle, Button } from '@/components/ui';
import { MiniMap } from '@/components/MiniMap';
import { issues, issueTrend, categoryData } from '@/data/mockData';
import { severityColor, statusColor } from '@/utils/format';
import { PageId } from '@/components/navItems';
import { AlertTriangle, Camera, ScanLine, Activity, MapPin, Flame, CheckCircle2, FileBarChart, Gauge, ListChecks, ArrowRight, Clock3, MessageSquare, Leaf, Sparkles } from 'lucide-react';
import { AreaChart, Area, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid, PieChart, Pie, Cell } from 'recharts';

function ComplaintCard({ icon: Icon, label, value, detail, tone, onClick }: { icon: typeof MessageSquare; label: string; value: string; detail: string; tone: 'orange' | 'green' | 'gold'; onClick: () => void }) {
  const tones = { orange: 'bg-[#fff0e8] text-accent', green: 'bg-[#e8f7f1] text-primary', gold: 'bg-[#fff8df] text-[#b7791f]' };
  return (
    <button onClick={onClick} className="group flex items-center gap-3 rounded-2xl border border-slate-200/70 bg-white p-4 text-left shadow-card transition-all hover:-translate-y-0.5 hover:border-primary/30 hover:shadow-soft">
      <div className={`grid h-11 w-11 shrink-0 place-items-center rounded-xl ${tones[tone]}`}><Icon className="h-5 w-5" /></div>
      <div className="min-w-0 flex-1"><p className="text-xs font-medium text-slate-500">{label}</p><p className="mt-0.5 text-xl font-bold text-slate-800">{value}</p><p className="truncate text-[11px] text-slate-400">{detail}</p></div>
      <ArrowRight className="h-4 w-4 text-slate-300 transition-transform group-hover:translate-x-1 group-hover:text-primary" />
    </button>
  );
}

export function Dashboard({ onNavigate }: { onNavigate: (p: PageId) => void }) {
  const stats = useMemo(() => {
    const total = issues.length;
    const critical = issues.filter((i) => i.severity === 'Critical').length;
    const pending = issues.filter((i) => i.status === 'Pending').length;
    const resolved = issues.filter((i) => i.status === 'Resolved').length;
    return { total, critical, pending, resolved, ai: 1693, hot: 11 };
  }, []);

  const recent = issues.slice(0, 4);
  const activity = [
    { t: '2 min ago', text: 'AI flagged garbage pile on Palasia Main Road', tone: 'error' },
    { t: '9 min ago', text: 'Crew resolved open drain at MR 10', tone: 'success' },
    { t: '17 min ago', text: 'Citizen submitted waterlogging report', tone: 'info' },
    { t: '26 min ago', text: 'Issue UE-4816 assigned to Public Works', tone: 'warning' },
  ];

  return (
    <div className="space-y-6">
      <Card className="relative overflow-hidden border-0 bg-gradient-to-r from-sidebar via-primary to-[#6eaa47] text-white shadow-soft">
        <div className="absolute inset-y-0 right-0 hidden w-1/2 md:block">
          <img src="/images/Screenshot_2026-08-17_182903.png" alt="Clean city initiative" className="h-full w-full object-cover opacity-75 mix-blend-screen" />
          <div className="absolute inset-0 bg-gradient-to-r from-sidebar via-sidebar/45 to-transparent" />
        </div>
        <div className="relative max-w-xl p-6 md:p-8">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-[11px] font-semibold tracking-wide text-white/90"><Leaf className="h-3.5 w-3.5 text-[#ffd166]" /> SWACHH BHARAT MISSION</div>
          <h2 className="text-2xl font-bold leading-tight md:text-3xl">Together for a cleaner, smarter Cities</h2>
          <p className="mt-2 max-w-md text-sm leading-6 text-white/80">See it. Report it. Resolve it. UrbanEye turns every citizen observation into visible action.</p>
          <div className="mt-5 flex flex-wrap gap-2">
            <Button onClick={() => onNavigate('report')} className="!bg-[#f59e0b] !text-white hover:!bg-[#d97706]">Report an issue <ArrowRight className="h-4 w-4" /></Button>
            <Button variant="ghost" onClick={() => onNavigate('gis')} className="!text-white hover:!bg-white/15">Explore city map</Button>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ComplaintCard icon={MessageSquare} label="My Complaints" value="12" detail="All reports submitted by you" tone="orange" onClick={() => onNavigate('issues')} />
        <ComplaintCard icon={Clock3} label="Pending Complaints" value="04" detail="Updates waiting for action" tone="green" onClick={() => onNavigate('issues')} />
        <ComplaintCard icon={CheckCircle2} label="Issues Resolved" value="08" detail="Thank you for helping Indore" tone="gold" onClick={() => onNavigate('reports')} />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
        <StatCard icon={ListChecks} label="Total Issues" value={stats.total + 476} accent="bg-primary/10 text-primary" sub="+12 this week" />
        <StatCard icon={AlertTriangle} label="Critical" value={stats.critical + 26} accent="bg-error/10 text-error" sub="Needs action" />
        <StatCard icon={FileBarChart} label="Pending Reports" value={stats.pending + 70} accent="bg-warning/10 text-warning" sub="Awaiting assign" />
        <StatCard icon={CheckCircle2} label="Resolved" value={stats.resolved + 315} accent="bg-success/10 text-success" sub="94% this month" />
        <StatCard icon={ScanLine} label="AI Detections" value={stats.ai.toLocaleString()} accent="bg-info/10 text-info" sub="Today: 312" />
        <StatCard icon={Flame} label="Active Hotspots" value={stats.hot} accent="bg-accent/10 text-accent" sub="Across 6 wards" />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <Card className="p-5 xl:col-span-2">
          <SectionTitle title="Issue Trend" subtitle="Reported vs resolved · last 7 days" action={<Badge text="Live" className="border-emerald-200 bg-emerald-50 text-emerald-600" />} />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={issueTrend} margin={{ left: -20, right: 8, top: 8 }}>
                <defs>
                  <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#0b8276" stopOpacity={0.3} /><stop offset="100%" stopColor="#0b8276" stopOpacity={0} /></linearGradient>
                  <linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#ef7d4d" stopOpacity={0.3} /><stop offset="100%" stopColor="#ef7d4d" stopOpacity={0} /></linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#eef2f6" vertical={false} />
                <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e2e8f0', fontSize: 12 }} />
                <Area type="monotone" dataKey="issues" stroke="#0b8276" strokeWidth={2.5} fill="url(#g1)" />
                <Area type="monotone" dataKey="resolved" stroke="#ef7d4d" strokeWidth={2.5} fill="url(#g2)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="p-5">
          <SectionTitle title="Issue Categories" subtitle="Distribution by type" />
          <div className="h-64 flex items-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={categoryData} dataKey="value" nameKey="name" innerRadius={48} outerRadius={80} paddingAngle={3}>
                  {categoryData.map((c) => <Cell key={c.name} fill={c.color} />)}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e2e8f0', fontSize: 12 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-2">
            {categoryData.map((c) => (
              <div key={c.name} className="flex items-center gap-2 text-xs text-slate-600">
                <span className="h-2.5 w-2.5 rounded-sm" style={{ background: c.color }} /> {c.name} <span className="ml-auto font-semibold">{c.value}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <Card className="p-5 xl:col-span-2">
          <SectionTitle title="Recent Reports" action={<Button variant="ghost" onClick={() => onNavigate('issues')}>View all <ArrowRight className="h-4 w-4" /></Button>} />
          <div className="space-y-2">
            {recent.map((i) => (
              <div key={i.id} className="flex items-center gap-3 rounded-xl border border-slate-100 p-3 hover:bg-slate-50">
                <img src={i.image} alt="" className="h-12 w-12 rounded-lg object-cover" />
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-slate-800 truncate">{i.issue}</span>
                    <Badge text={i.severity} className={severityColor(i.severity)} />
                  </div>
                  <div className="text-xs text-slate-500 flex items-center gap-1 mt-0.5"><MapPin className="h-3 w-3" /> {i.location} · {i.date}</div>
                </div>
                <Badge text={i.status} className={statusColor(i.status)} />
              </div>
            ))}
          </div>
        </Card>

        <div className="space-y-6">
          <Card className="p-5">
            <SectionTitle title="Live Activity" action={<Activity className="h-4 w-4 text-emerald-500 animate-pulse" />} />
            <div className="space-y-3">
              {activity.map((a, idx) => (
                <div key={idx} className="flex gap-3 text-xs">
                  <span className={`mt-1 h-2 w-2 rounded-full shrink-0 ${a.tone === 'error' ? 'bg-error' : a.tone === 'success' ? 'bg-success' : a.tone === 'warning' ? 'bg-warning' : 'bg-info'}`} />
                  <div>
                    <p className="text-slate-700">{a.text}</p>
                    <p className="text-slate-400 mt-0.5">{a.t}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-5">
            <SectionTitle title="Hotspot Map" subtitle="High-priority zones" action={<Button variant="ghost" onClick={() => onNavigate('gis')}>Open GIS <ArrowRight className="h-4 w-4" /></Button>} />
            <MiniMap issues={issues} height="220px" />
          </Card>
        </div>
      </div>

      <Card className="overflow-hidden border-[#f7c7a7] bg-gradient-to-r from-[#fff7f0] via-white to-[#f0fbf6] p-5">
        <div className="mb-4 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em] text-primary"><Sparkles className="h-4 w-4 text-accent" /> Make every street count</div>
        <SectionTitle title="Quick Actions" subtitle="Jump into a core workflow" />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { id: 'detection' as PageId, label: 'Analyze Image', icon: ScanLine, desc: 'Run AI detection' },
            { id: 'photo' as PageId, label: 'Take Photo', icon: Camera, desc: 'Capture & analyze' },
            { id: 'report' as PageId, label: 'Citizen Report', icon: FileBarChart, desc: 'Submit a complaint' },
            { id: 'alerts' as PageId, label: 'Priority Alerts', icon: Gauge, desc: 'Triage queue' },
          ].map((a) => (
            <button key={a.id} onClick={() => onNavigate(a.id)} className="flex flex-col gap-2 rounded-xl border border-slate-200 p-4 text-left hover:border-primary/40 hover:bg-primary/5 transition-all">
              <a.icon className="h-6 w-6 text-primary" />
              <div className="text-sm font-semibold text-slate-800">{a.label}</div>
              <div className="text-xs text-slate-400">{a.desc}</div>
            </button>
          ))}
        </div>
      </Card>
    </div>
  );
}
