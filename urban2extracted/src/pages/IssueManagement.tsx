import { useMemo, useState } from 'react';
import { Card, Badge, Button, SectionTitle } from '@/components/ui';
import { issues, UrbanIssue, IssueStatus, detectionTypes } from '@/data/mockData';
import { severityColor, statusColor } from '@/utils/format';
import { Search, UserPlus, Play, CheckCircle2 } from 'lucide-react';

export function IssueManagement() {
  const [list, setList] = useState<UrbanIssue[]>(issues);
  const [q, setQ] = useState('');
  const [type, setType] = useState('All');
  const [sev, setSev] = useState('All');
  const [status, setStatus] = useState('All');

  const filtered = useMemo(() => list.filter((i) =>
    (q === '' || i.issue.toLowerCase().includes(q.toLowerCase()) || i.id.toLowerCase().includes(q.toLowerCase()) || i.location.toLowerCase().includes(q.toLowerCase())) &&
    (type === 'All' || i.category === type) &&
    (sev === 'All' || i.severity === sev) &&
    (status === 'All' || i.status === status)
  ), [list, q, type, sev, status]);

  const advance = (id: string, to: IssueStatus) => {
    setList((prev) => prev.map((i) => i.id === id ? { ...i, status: to } : i));
  };

  const next = (s: IssueStatus): { label: string; to: IssueStatus; icon: typeof UserPlus } | null => {
    if (s === 'Pending') return { label: 'Assign', to: 'Assigned', icon: UserPlus };
    if (s === 'Assigned') return { label: 'Start', to: 'In Progress', icon: Play };
    if (s === 'In Progress') return { label: 'Resolve', to: 'Resolved', icon: CheckCircle2 };
    return null;
  };

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 flex-1 min-w-48 rounded-xl border border-slate-300 px-3 py-2">
            <Search className="h-4 w-4 text-slate-400" />
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search ID, issue, location…" className="flex-1 bg-transparent text-sm focus:outline-none" />
          </div>
          <Select value={type} onChange={setType} options={['All', ...detectionTypes]} />
          <Select value={sev} onChange={setSev} options={['All', 'Critical', 'High', 'Medium', 'Low']} />
          <Select value={status} onChange={setStatus} options={['All', 'Pending', 'Assigned', 'In Progress', 'Resolved']} />
        </div>
      </Card>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-slate-500 text-xs">
              <tr>
                <th className="text-left px-4 py-3 font-semibold">ID</th>
                <th className="text-left px-4 py-3 font-semibold">Issue</th>
                <th className="text-left px-4 py-3 font-semibold">Location</th>
                <th className="text-left px-4 py-3 font-semibold">Severity</th>
                <th className="text-left px-4 py-3 font-semibold">Date</th>
                <th className="text-left px-4 py-3 font-semibold">Status</th>
                <th className="text-left px-4 py-3 font-semibold">Department</th>
                <th className="text-right px-4 py-3 font-semibold">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map((i) => {
                const n = next(i.status);
                return (
                  <tr key={i.id} className="hover:bg-slate-50">
                    <td className="px-4 py-3 font-mono text-xs text-slate-500">{i.id}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <img src={i.image} alt="" className="h-9 w-9 rounded-lg object-cover" />
                        <div>
                          <div className="font-semibold text-slate-800">{i.issue}</div>
                          <div className="text-[11px] text-slate-400">{i.category}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-slate-600">{i.location}<div className="text-[11px] text-slate-400">{i.ward}</div></td>
                    <td className="px-4 py-3"><Badge text={i.severity} className={severityColor(i.severity)} /></td>
                    <td className="px-4 py-3 text-slate-500 text-xs">{i.date}</td>
                    <td className="px-4 py-3"><Badge text={i.status} className={statusColor(i.status)} /></td>
                    <td className="px-4 py-3 text-slate-600 text-xs">{i.department}</td>
                    <td className="px-4 py-3 text-right">
                      {n ? (
                        <Button variant="outline" className="!px-3 !py-1.5 !text-xs" onClick={() => advance(i.id, n.to)}>
                          <n.icon className="h-3.5 w-3.5" /> {n.label}
                        </Button>
                      ) : <span className="text-xs text-emerald-600 font-semibold">Done</span>}
                    </td>
                  </tr>
                );
              })}
              {filtered.length === 0 && <tr><td colSpan={8} className="text-center py-10 text-slate-400 text-sm">No issues match your filters.</td></tr>}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

function Select({ value, onChange, options }: { value: string; onChange: (v: string) => void; options: string[] }) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)} className="rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
      {options.map((o) => <option key={o}>{o}</option>)}
    </select>
  );
}
