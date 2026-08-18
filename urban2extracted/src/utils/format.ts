import { Severity, IssueStatus } from '@/data/mockData';

export const severityColor = (s: Severity): string =>
  s === 'Critical' ? 'bg-red-500/15 text-red-600 border-red-200'
  : s === 'High' ? 'bg-orange-500/15 text-orange-600 border-orange-200'
  : s === 'Medium' ? 'bg-amber-500/15 text-amber-600 border-amber-200'
  : 'bg-emerald-500/15 text-emerald-600 border-emerald-200';

export const statusColor = (s: IssueStatus): string =>
  s === 'Resolved' ? 'bg-emerald-500/15 text-emerald-600 border-emerald-200'
  : s === 'In Progress' ? 'bg-sky-500/15 text-sky-600 border-sky-200'
  : s === 'Assigned' ? 'bg-violet-500/15 text-violet-600 border-violet-200'
  : 'bg-slate-500/15 text-slate-600 border-slate-200';

export const severityDot = (s: Severity): string =>
  s === 'Critical' ? '#e5484d' : s === 'High' ? '#f97316' : s === 'Medium' ? '#f59e0b' : '#10b981';
