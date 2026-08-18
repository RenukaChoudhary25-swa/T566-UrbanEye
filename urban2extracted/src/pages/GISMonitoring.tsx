import { useState } from 'react';
import { Card, Badge, SectionTitle } from '@/components/ui';
import { MiniMap } from '@/components/MiniMap';
import { issues, UrbanIssue, detectionTypes } from '@/data/mockData';
import { severityColor, statusColor } from '@/utils/format';
import { Filter, X, MapPin } from 'lucide-react';

export function GISMonitoring() {
  const [type, setType] = useState('All');
  const [sev, setSev] = useState('All');
  const [status, setStatus] = useState('All');
  const [selected, setSelected] = useState<UrbanIssue | null>(null);

  const filtered = issues.filter((i) =>
    (type === 'All' || i.category === type) &&
    (sev === 'All' || i.severity === sev) &&
    (status === 'All' || i.status === status)
  );

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 text-sm font-semibold text-slate-700"><Filter className="h-4 w-4 text-primary" /> Filters</div>
          <Select label="Issue Type" value={type} onChange={setType} options={['All', ...detectionTypes]} />
          <Select label="Severity" value={sev} onChange={setSev} options={['All', 'Critical', 'High', 'Medium', 'Low']} />
          <Select label="Status" value={status} onChange={setStatus} options={['All', 'Pending', 'Assigned', 'In Progress', 'Resolved']} />
          <span className="text-xs text-slate-400 ml-auto">{filtered.length} markers</span>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="lg:col-span-3">
          <MiniMap issues={filtered} height="560px" onMarkerClick={setSelected} />
        </div>
        <div>
          <Card className="p-5">
            <SectionTitle title="Marker Detail" subtitle="Click a marker on the map" />
            {!selected && <p className="text-sm text-slate-400 py-10 text-center">Select a marker to view issue details.</p>}
            {selected && (
              <div className="space-y-3">
                <img src={selected.image} alt="" className="w-full h-32 object-cover rounded-xl" />
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-slate-800">{selected.issue}</span>
                  <button onClick={() => setSelected(null)} className="text-slate-400 hover:text-slate-600"><X className="h-4 w-4" /></button>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Badge text={selected.severity} className={severityColor(selected.severity)} />
                  <Badge text={selected.status} className={statusColor(selected.status)} />
                </div>
                <Row label="ID" value={selected.id} />
                <Row label="Location" value={<span className="flex items-center gap-1"><MapPin className="h-3 w-3" />{selected.location}</span>} />
                <Row label="Ward" value={selected.ward} />
                <Row label="Department" value={selected.department} />
                <Row label="Reported" value={selected.date} />
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}

function Select({ label, value, onChange, options }: { label: string; value: string; onChange: (v: string) => void; options: string[] }) {
  return (
    <div>
      <label className="text-[11px] text-slate-400 block">{label}</label>
      <select value={value} onChange={(e) => onChange(e.target.value)} className="rounded-lg border border-slate-300 px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
        {options.map((o) => <option key={o}>{o}</option>)}
      </select>
    </div>
  );
}

function Row({ label, value }: { label: string; value: React.ReactNode }) {
  return <div className="flex justify-between text-sm"><span className="text-slate-500">{label}</span><span className="font-semibold text-slate-800 text-right">{value}</span></div>;
}
