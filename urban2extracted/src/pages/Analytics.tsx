import { Card, SectionTitle } from '@/components/ui';
import { issueTrend, categoryData, wardData, issues } from '@/data/mockData';
import { BarChart, Bar, LineChart, Line, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid, PieChart, Pie, Cell, RadialBarChart, RadialBar, Legend } from 'recharts';

const severityData = [
  { name: 'Critical', value: 28, fill: '#e5484d' },
  { name: 'High', value: 64, fill: '#f97316' },
  { name: 'Medium', value: 132, fill: '#f59e0b' },
  { name: 'Low', value: 258, fill: '#10b981' },
];

const aiActivity = [
  { h: '00', d: 12 }, { h: '04', d: 8 }, { h: '08', d: 96 }, { h: '12', d: 142 }, { h: '16', d: 168 }, { h: '20', d: 74 },
];

export function Analytics() {
  const resolved = issues.filter((i) => i.status === 'Resolved').length;
  const resolutionRate = Math.round((resolved / issues.length) * 100);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5">
          <SectionTitle title="Issues Over Time" subtitle="Daily volume · last 7 days" />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={issueTrend} margin={{ left: -20, right: 8, top: 8 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eef2f6" vertical={false} />
                <XAxis dataKey="day" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e2e8f0', fontSize: 12 }} />
                <Line type="monotone" dataKey="issues" stroke="#0b8276" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="resolved" stroke="#ef7d4d" strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="p-5">
          <SectionTitle title="Issue Categories" subtitle="Distribution by type" />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={categoryData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={85} paddingAngle={3}>
                  {categoryData.map((c) => <Cell key={c.name} fill={c.color} />)}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e2e8f0', fontSize: 12 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="p-5 lg:col-span-2">
          <SectionTitle title="Ward-wise Issues" subtitle="Issues and response time by ward" />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={wardData} margin={{ left: -20, right: 8, top: 8 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eef2f6" vertical={false} />
                <XAxis dataKey="ward" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e2e8f0', fontSize: 12 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="issues" fill="#0b8276" radius={[6, 6, 0, 0]} />
                <Bar dataKey="response" fill="#ef7d4d" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="p-5">
          <SectionTitle title="Severity Mix" subtitle="By count" />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={severityData} layout="vertical" margin={{ left: 20, right: 8 }}>
                <XAxis type="number" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} width={64} />
                <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e2e8f0', fontSize: 12 }} />
                <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                  {severityData.map((s) => <Cell key={s.name} fill={s.fill} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="p-5">
          <SectionTitle title="Resolution Rate" subtitle="Overall closure" />
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <RadialBarChart innerRadius="60%" outerRadius="100%" data={[{ name: 'Resolved', value: resolutionRate, fill: '#10b981' }]} startAngle={90} endAngle={90 - 360}>
                <RadialBar background dataKey="value" cornerRadius={12} />
              </RadialBarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-center text-2xl font-bold text-slate-800 -mt-20">{resolutionRate}%</p>
          <p className="text-center text-xs text-slate-400 mt-16">Resolved this cycle</p>
        </Card>

        <Card className="p-5 lg:col-span-2">
          <SectionTitle title="AI Activity" subtitle="Detections per 4-hour window" />
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={aiActivity} margin={{ left: -20, right: 8, top: 8 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eef2f6" vertical={false} />
                <XAxis dataKey="h" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e2e8f0', fontSize: 12 }} />
                <Bar dataKey="d" fill="#1d9bf0" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-3 gap-3 mt-3 text-center">
            <Stat label="Avg Response" value="4.2h" />
            <Stat label="Detections Today" value="312" />
            <Stat label="Accuracy" value="91%" />
          </div>
        </Card>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl bg-slate-50 p-3"><div className="text-lg font-bold text-slate-800">{value}</div><div className="text-[11px] text-slate-400">{label}</div></div>;
}
