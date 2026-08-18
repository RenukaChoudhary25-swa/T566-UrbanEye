export type Severity = 'Critical' | 'High' | 'Medium' | 'Low';
export type IssueStatus = 'Pending' | 'Assigned' | 'In Progress' | 'Resolved';

export interface UrbanIssue {
  id: string;
  issue: string;
  category: string;
  location: string;
  ward: string;
  severity: Severity;
  status: IssueStatus;
  department: string;
  date: string;
  confidence: number;
  impact: number;
  lat: number;
  lng: number;
  image: string;
}

export const issues: UrbanIssue[] = [
  { id: 'UE-4821', issue: 'Garbage accumulation', category: 'Garbage', location: 'Palasia Main Road', ward: 'Ward 12', severity: 'Critical', status: 'Pending', department: 'Solid Waste', date: 'Today, 10:42 AM', confidence: 94, impact: 92, lat: 22.7196, lng: 75.8577, image: '/images/Screenshot_2026-08-17_122130.png' },
  { id: 'UE-4818', issue: 'Waterlogging on carriageway', category: 'Waterlogging', location: 'Vijay Nagar Square', ward: 'Ward 24', severity: 'High', status: 'In Progress', department: 'Storm Water', date: 'Today, 09:18 AM', confidence: 89, impact: 82, lat: 22.7533, lng: 75.8937, image: '/images/Screenshot_2026-08-17_114822.png' },
  { id: 'UE-4816', issue: 'Road surface damage', category: 'Pothole', location: 'Rau Ring Road', ward: 'Ward 8', severity: 'High', status: 'Assigned', department: 'Public Works', date: 'Yesterday, 06:40 PM', confidence: 91, impact: 77, lat: 22.6732, lng: 75.8066, image: '/images/Screenshot_2026-08-17_114907.png' },
  { id: 'UE-4811', issue: 'Overflowing public bin', category: 'Overflowing Dustbin', location: 'Rau Market', ward: 'Ward 8', severity: 'Medium', status: 'Pending', department: 'Solid Waste', date: 'Yesterday, 03:22 PM', confidence: 87, impact: 62, lat: 22.6547, lng: 75.8014, image: '/images/Screenshot_2026-08-17_114822.png' },
  { id: 'UE-4809', issue: 'Open storm drain', category: 'Open Drain', location: 'MR 10 Service Lane', ward: 'Ward 18', severity: 'High', status: 'Resolved', department: 'Public Works', date: '16 Aug, 11:05 AM', confidence: 96, impact: 88, lat: 22.7411, lng: 75.9052, image: '/images/Screenshot_2026-08-17_114907.png' },
  { id: 'UE-4803', issue: 'Public hygiene concern', category: 'Public Hygiene', location: 'Sarwate Bus Stand', ward: 'Ward 3', severity: 'Medium', status: 'Resolved', department: 'Health & Sanitation', date: '15 Aug, 02:16 PM', confidence: 84, impact: 55, lat: 22.7163, lng: 75.8665, image: '/images/Screenshot_2026-08-17_114822.png' },
];

export const issueTrend = [
  { day: '11 Aug', issues: 42, resolved: 28 }, { day: '12 Aug', issues: 56, resolved: 37 }, { day: '13 Aug', issues: 49, resolved: 35 }, { day: '14 Aug', issues: 71, resolved: 44 }, { day: '15 Aug', issues: 62, resolved: 49 }, { day: '16 Aug', issues: 84, resolved: 58 }, { day: '17 Aug', issues: 68, resolved: 46 },
];

export const categoryData = [
  { name: 'Garbage', value: 38, color: '#0b8276' }, { name: 'Potholes', value: 24, color: '#f59e0b' }, { name: 'Waterlogging', value: 16, color: '#1d9bf0' }, { name: 'Dustbins', value: 12, color: '#ef7d4d' }, { name: 'Other', value: 10, color: '#93a4a4' },
];

export const wardData = [
  { ward: 'W-12', issues: 86, response: 82 }, { ward: 'W-24', issues: 74, response: 68 }, { ward: 'W-08', issues: 61, response: 76 }, { ward: 'W-18', issues: 54, response: 88 }, { ward: 'W-03', issues: 42, response: 91 },
];

export const detectionTypes = ['Garbage', 'Pothole', 'Waterlogging', 'Overflowing Dustbin', 'Open Drain', 'Dead Animal', 'Public Hygiene'];
