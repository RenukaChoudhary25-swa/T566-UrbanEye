import { useState } from 'react';
import { Shell } from '@/components/Shell';
import { PageId } from '@/components/navItems';
import { Dashboard } from '@/pages/Dashboard';
import { AIDetection } from '@/pages/AIDetection';
import { TakePhoto } from '@/pages/TakePhoto';
import { CitizenReport } from '@/pages/CitizenReport';
import { GISMonitoring } from '@/pages/GISMonitoring';
import { IssueManagement } from '@/pages/IssueManagement';
import { PriorityAlerts } from '@/pages/PriorityAlerts';
import { Analytics } from '@/pages/Analytics';
import { Reports } from '@/pages/Reports';
import { Settings } from '@/pages/Settings';

export default function App() {
  const [page, setPage] = useState<PageId>('dashboard');

  const render = () => {
    switch (page) {
      case 'dashboard': return <Dashboard onNavigate={setPage} />;
      case 'detection': return <AIDetection onNavigate={setPage} />;
      case 'photo': return <TakePhoto onNavigate={setPage} />;
      case 'report': return <CitizenReport />;
      case 'gis': return <GISMonitoring />;
      case 'issues': return <IssueManagement />;
      case 'alerts': return <PriorityAlerts />;
      case 'analytics': return <Analytics />;
      case 'reports': return <Reports />;
      case 'settings': return <Settings />;
      default: return <Dashboard onNavigate={setPage} />;
    }
  };

  return (
    <Shell active={page} onNavigate={setPage}>
      {render()}
    </Shell>
  );
}
