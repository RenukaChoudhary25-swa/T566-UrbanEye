import { useMemo } from 'react';
import { Card, Badge, SectionTitle } from '@/components/ui';
import { issues } from '@/data/mockData';
import { scorePriority } from '@/services/api';
import { severityColor } from '@/utils/format';
import { AlertTriangle, Flame, ShieldAlert, Info } from 'lucide-react';

export function PriorityAlerts() {
  const ranked = useMemo(() => issues.map((i) => ({ ...i, score: scorePriority(i.severity, i.confidence, i.impact) })).sort((a, b) => b.score - a.score), []);

  const tier = (s: number) => s >= 75 ? { label: 'Critical', color: 'bg-error/10 text-error border-error/20', icon: Flame } : s >= 55 ? { label: 'High', color: 'bg-orange-500/10 text-orange-600 border-orange-200', icon: AlertTriangle } : s >= 35 ? { label: 'Medium', color: 'bg-amber-500/10 text-amber-600 border-amber-200', icon: ShieldAlert } : { label: 'Low', color: 'bg-emerald-500/10 text-emerald-600 border-emerald-200', icon: Info };

  const counts = { Critical: ranked.filter((r) => r.score >= 75).length, High: ranked.filter((r) => r.score >= 55 && r.score < 75).length, Medium: ranked.filter((r) => r.score >= 35 && r.score < 55).length, Low: ranked.filter((r) => r.score < 35).length };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Object.entries(counts).map(([k, v]) => {
          const t = tier(k === 'Critical' ? 80 : k === 'High' ? 60 : k === 'Medium' ? 40 : 20);
          const Icon = t.icon;
          return (
            <Card key={k} className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-500">{k} Priority</p>
                  <p className="text-2xl font-bold text-slate-800 mt-1">{v}</p>
                </div>
                <div className={`h-10 w-10 rounded-xl grid place-items-center ${t.color}`}><Icon className="h-5 w-5" /></div>
              </div>
            </Card>
          );
        })}
      </div>

      <Card className="p-5">
        <SectionTitle title="Priority Queue" subtitle="Auto-scored by severity, confidence, and impact" />
        <div className="space-y-3">
          {ranked.map((i) => {
            const t = tier(i.score);
            return (
              <div key={i.id} className="flex items-center gap-3 rounded-xl border border-slate-100 p-3 hover:bg-slate-50">
                <div className={`h-12 w-12 rounded-xl grid place-items-center font-bold text-sm ${t.color}`}>{i.score}</div>
                <img src={i.image} alt="" className="h-12 w-12 rounded-lg object-cover" />
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-slate-800 truncate">{i.issue}</span>
                    <Badge text={i.severity} className={severityColor(i.severity)} />
                  </div>
                  <div className="text-xs text-slate-500 mt-0.5">{i.location} · {i.department}</div>
                </div>
                <Badge text={t.label} className={t.color} />
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
