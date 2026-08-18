import { Card, SectionTitle, Button, Badge } from '@/components/ui';
import { Bell, Shield, Cpu, MapPin, HelpCircle, Heart, Trash2, LogOut } from 'lucide-react';

export function Settings() {
  return (
    <div className="max-w-3xl mx-auto space-y-4">
      <Card className="p-5">
        <SectionTitle title="Citizen Profile" subtitle="Your identity and contact details" />
        <div className="flex items-center gap-4">
          <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-primary to-[#6eaa47] text-white grid place-items-center text-xl font-bold">RG</div>
          <div className="flex-1">
            <div className="font-semibold text-slate-800">Ravi Gupta</div>
            <div className="text-xs text-slate-400">ravi.gupta@example.com · Ward 12, Indore</div>
            <Badge text="Active Citizen" className="border-primary/30 bg-primary/10 text-primary mt-1" />
          </div>
          <Button variant="outline">Edit</Button>
        </div>
      </Card>

      <Card className="p-5">
        <SectionTitle title="My Complaints" subtitle="Quick links to track your reports" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <SummaryTile icon={MapPin} label="Total filed" value="12" tone="bg-primary/10 text-primary" />
          <SummaryTile icon={Cpu} label="In progress" value="4" tone="bg-warning/10 text-warning" />
          <SummaryTile icon={Shield} label="Resolved" value="8" tone="bg-success/10 text-success" />
        </div>
      </Card>

      <Card className="p-5">
        <SectionTitle title="Notifications" subtitle="Stay updated on your complaints" />
        <div className="space-y-3">
          {[
            { icon: Bell, label: 'Status updates', desc: 'When your complaint status changes', on: true },
            { icon: Shield, label: 'Resolution alerts', desc: 'Notify when an issue is resolved', on: true },
            { icon: Cpu, label: 'Weekly civic digest', desc: 'Summary of your ward every Sunday', on: false },
          ].map((s) => (
            <div key={s.label} className="flex items-center gap-3 rounded-xl border border-slate-100 p-3">
              <div className="h-10 w-10 rounded-xl bg-slate-100 grid place-items-center"><s.icon className="h-5 w-5 text-slate-600" /></div>
              <div className="flex-1"><div className="text-sm font-semibold text-slate-800">{s.label}</div><div className="text-xs text-slate-400">{s.desc}</div></div>
              <Toggle on={s.on} />
            </div>
          ))}
        </div>
      </Card>

      <Card className="p-5">
        <SectionTitle title="Preferences" subtitle="Personalize your UrbanEye experience" />
        <div className="space-y-3">
          <PrefRow icon={MapPin} label="Default location" value="Ward 12, Palasia" />
          <PrefRow icon={HelpCircle} label="Language" value="English" />
          <PrefRow icon={Heart} label="Volunteer cleanup alerts" value="On" />
        </div>
      </Card>

      <Card className="p-5">
        <SectionTitle title="Account" subtitle="Manage your session and data" />
        <div className="flex flex-wrap gap-2">
          <Button variant="outline"><Trash2 className="h-4 w-4" /> Clear local data</Button>
          <Button variant="danger"><LogOut className="h-4 w-4" /> Logout</Button>
        </div>
      </Card>
    </div>
  );
}

function Toggle({ on }: { on: boolean }) {
  return <span className={`h-6 w-11 rounded-full p-0.5 transition-colors ${on ? 'bg-primary' : 'bg-slate-300'}`}><span className={`block h-5 w-5 rounded-full bg-white transition-transform ${on ? 'translate-x-5' : ''}`} /></span>;
}

function SummaryTile({ icon: Icon, label, value, tone }: { icon: typeof Bell; label: string; value: string; tone: string }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-slate-100 p-3">
      <div className={`h-10 w-10 rounded-xl grid place-items-center ${tone}`}><Icon className="h-5 w-5" /></div>
      <div><div className="text-xl font-bold text-slate-800">{value}</div><div className="text-[11px] text-slate-400">{label}</div></div>
    </div>
  );
}

function PrefRow({ icon: Icon, label, value }: { icon: typeof Bell; label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-slate-100 p-3">
      <div className="h-10 w-10 rounded-xl bg-accent/10 grid place-items-center"><Icon className="h-5 w-5 text-accent" /></div>
      <div className="flex-1"><div className="text-sm font-semibold text-slate-800">{label}</div></div>
      <span className="text-sm text-slate-600">{value}</span>
    </div>
  );
}
