import { LayoutDashboard, ScanLine, Camera, MessageSquareWarning, Map, ListChecks, AlertTriangle, BarChart3, FileText, Settings } from 'lucide-react';

export type PageId =
  | 'dashboard' | 'detection' | 'photo' | 'report' | 'gis'
  | 'issues' | 'alerts' | 'analytics' | 'reports' | 'settings';

interface NavItem { id: PageId; label: string; icon: typeof LayoutDashboard; }

export const navItems: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'detection', label: 'AI Detection', icon: ScanLine },
  { id: 'photo', label: 'Take Photo', icon: Camera },
  { id: 'report', label: 'Citizen Report', icon: MessageSquareWarning },
  { id: 'gis', label: 'GIS Monitoring', icon: Map },
  { id: 'issues', label: 'Issue Management', icon: ListChecks },
  { id: 'alerts', label: 'Priority & Alerts', icon: AlertTriangle },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
  { id: 'reports', label: 'Reports', icon: FileText },
  { id: 'settings', label: 'Settings', icon: Settings },
];
