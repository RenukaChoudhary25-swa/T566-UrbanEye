import { Card, Button, SectionTitle } from '@/components/ui';
import { issues } from '@/data/mockData';
import { Download, FileText } from 'lucide-react';

const csv = (rows: Record<string, unknown>[]) => {
  const headers = Object.keys(rows[0]);
  const body = rows.map((r) => headers.map((h) => `"${String(r[h]).replace(/"/g, '""')}"`).join(','));
  return [headers.join(','), ...body].join('\n');
};

export function Reports() {
  const daily = issues;
  const weekly = [
    { ward: 'Ward 12', issues: 86, resolved: 74, rate: '86%' },
    { ward: 'Ward 24', issues: 74, resolved: 61, rate: '82%' },
    { ward: 'Ward 08', issues: 61, resolved: 52, rate: '85%' },
    { ward: 'Ward 18', issues: 54, resolved: 49, rate: '91%' },
  ];

  const download = (name: string, data: Record<string, unknown>[]) => {
    const blob = new Blob([csv(data)], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = name; a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5">
          <SectionTitle title="Daily Report" subtitle="Today's reported issues" action={<Button variant="outline" onClick={() => download('urbaneye_daily.csv', daily.map((i) => ({ id: i.id, issue: i.issue, location: i.location, severity: i.severity, status: i.status, department: i.department, date: i.date })))}><Download className="h-4 w-4" /> CSV</Button>} />
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-xs text-slate-500"><tr><th className="text-left py-2">ID</th><th className="text-left py-2">Issue</th><th className="text-left py-2">Severity</th><th className="text-left py-2">Status</th></tr></thead>
              <tbody className="divide-y divide-slate-100">
                {daily.map((i) => <tr key={i.id}><td className="py-2 font-mono text-xs text-slate-500">{i.id}</td><td className="py-2 text-slate-700">{i.issue}</td><td className="py-2 text-slate-600">{i.severity}</td><td className="py-2 text-slate-600">{i.status}</td></tr>)}
              </tbody>
            </table>
          </div>
        </Card>

        <Card className="p-5">
          <SectionTitle title="Ward-wise Weekly Report" action={<Button variant="outline" onClick={() => download('urbaneye_weekly.csv', weekly)}><Download className="h-4 w-4" /> CSV</Button>} />
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-xs text-slate-500"><tr><th className="text-left py-2">Ward</th><th className="text-left py-2">Issues</th><th className="text-left py-2">Resolved</th><th className="text-left py-2">Rate</th></tr></thead>
              <tbody className="divide-y divide-slate-100">
                {weekly.map((w) => <tr key={w.ward}><td className="py-2 text-slate-700 font-semibold">{w.ward}</td><td className="py-2 text-slate-600">{w.issues}</td><td className="py-2 text-slate-600">{w.resolved}</td><td className="py-2 text-emerald-600 font-semibold">{w.rate}</td></tr>)}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      <Card className="p-5">
        <SectionTitle title="Generated Reports" subtitle="Exportable summaries" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {[
            { name: 'Daily Summary', date: '17 Aug 2026', size: '12 KB' },
            { name: 'Weekly Ward Report', date: '11–17 Aug 2026', size: '38 KB' },
            { name: 'AI Detection Log', date: '17 Aug 2026', size: '64 KB' },
          ].map((r) => (
            <div key={r.name} className="flex items-center gap-3 rounded-xl border border-slate-200 p-4">
              <div className="h-10 w-10 rounded-xl bg-primary/10 grid place-items-center"><FileText className="h-5 w-5 text-primary" /></div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-semibold text-slate-800 truncate">{r.name}</div>
                <div className="text-[11px] text-slate-400">{r.date} · {r.size}</div>
              </div>
              <Button variant="ghost" onClick={() => download(r.name.replace(/\s+/g, '_').toLowerCase() + '.csv', daily.map((i) => ({ id: i.id, issue: i.issue, severity: i.severity, status: i.status })))}><Download className="h-4 w-4" /></Button>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
