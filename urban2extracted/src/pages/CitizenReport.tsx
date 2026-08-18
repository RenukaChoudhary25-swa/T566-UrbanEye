import { useRef, useState } from 'react';
import { Card, Button, Badge, SectionTitle } from '@/components/ui';
import { submitReport, ReportReceipt } from '@/services/api';
import { useGeolocation } from '@/hooks/useGeolocation';
import { detectionTypes } from '@/data/mockData';
import { severityColor } from '@/utils/format';
import { Upload, Mic, MapPin, Send, Loader2, CheckCircle2, Camera, Locate } from 'lucide-react';

export function CitizenReport() {
  const [image, setImage] = useState<string | null>(null);
  const [desc, setDesc] = useState('');
  const [category, setCategory] = useState(detectionTypes[0]);
  const [location, setLocation] = useState('');
  const [coords, setCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [locating, setLocating] = useState(false);
  const [recording, setRecording] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [receipt, setReceipt] = useState<ReportReceipt | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleFile = (f?: File) => { if (f) setImage(URL.createObjectURL(f)); };

  const locate = async () => {
    setLocating(true);
    const g = await useGeolocation();
    setCoords({ lat: g.lat, lng: g.lng });
    setLocation(g.label);
    setLocating(false);
  };

  const toggleVoice = () => {
    setRecording((r) => !r);
    if (!recording) setTimeout(() => setRecording(false), 4000);
  };

  const submit = async () => {
    if (!desc && !image) { setError('Add a photo or description before submitting.'); return; }
    setError(null); setSubmitting(true);
    const r = await submitReport({ image: null, description: desc, category, location, lat: coords?.lat, lng: coords?.lng });
    setReceipt(r); setSubmitting(false);
  };

  if (receipt) {
    return (
      <div className="max-w-xl mx-auto">
        <Card className="p-6 text-center">
          <div className="mx-auto h-14 w-14 rounded-2xl bg-emerald-100 grid place-items-center mb-3"><CheckCircle2 className="h-7 w-7 text-emerald-600" /></div>
          <h3 className="text-lg font-bold text-slate-800">Report Submitted</h3>
          <p className="text-xs text-slate-400 mt-1">Your report is now tracked in the UrbanEye system.</p>
          <div className="mt-5 text-left space-y-2 rounded-xl border border-slate-200 p-4">
            <Row label="Report ID" value={receipt.reportId} />
            <Row label="AI Classification" value={receipt.classification} />
            <Row label="Severity" value={<Badge text={receipt.severity} className={severityColor(receipt.severity)} />} />
            <Row label="Location" value={receipt.location} />
            <Row label="Assigned Department" value={receipt.department} />
            <Row label="Status" value={<Badge text={receipt.status} className="border-slate-200 bg-slate-100 text-slate-600" />} />
          </div>
          <div className="flex gap-2 justify-center mt-5">
            <Button onClick={() => { setReceipt(null); setImage(null); setDesc(''); }}>File Another</Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-4">
      <Card className="p-5">
        <SectionTitle title="Citizen Report" subtitle="Report an urban issue with photo, voice, and location" />
        {error && <div className="mb-3 rounded-lg bg-error/10 border border-error/20 text-error text-xs px-3 py-2">{error}</div>}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-medium text-slate-600">Photo</label>
            <button onClick={() => fileRef.current?.click()} onDragOver={(e) => e.preventDefault()} onDrop={(e) => { e.preventDefault(); handleFile(e.dataTransfer.files?.[0]); }}
              className="mt-1 w-full h-36 rounded-xl border-2 border-dashed border-slate-300 grid place-items-center hover:border-primary/50 hover:bg-primary/5 text-slate-400">
              {image ? <img src={image} className="h-full w-full object-cover rounded-xl" alt="" /> : <div className="text-center"><Upload className="h-6 w-6 mx-auto" /><p className="text-xs mt-1">Upload or drag</p></div>}
            </button>
            <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={(e) => handleFile(e.target.files?.[0] || undefined)} />
            <div className="flex gap-2 mt-2">
              <Button variant="outline" className="flex-1" onClick={() => fileRef.current?.click()}><Camera className="h-4 w-4" /> Photo</Button>
              <Button variant="outline" className={`flex-1 ${recording ? '!border-error !text-error' : ''}`} onClick={toggleVoice}><Mic className="h-4 w-4" /> {recording ? 'Recording…' : 'Voice'}</Button>
            </div>
          </div>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-slate-600">Description</label>
              <textarea value={desc} onChange={(e) => setDesc(e.target.value)} rows={3} placeholder="Describe what you observed…"
                className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
            </div>
            <div>
              <label className="text-xs font-medium text-slate-600">Category</label>
              <select value={category} onChange={(e) => setCategory(e.target.value)}
                className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
                {detectionTypes.map((t) => <option key={t}>{t}</option>)}
              </select>
            </div>
          </div>
        </div>

        <div className="mt-4">
          <label className="text-xs font-medium text-slate-600">Location</label>
          <div className="flex gap-2 mt-1">
            <div className="flex-1 flex items-center gap-2 rounded-xl border border-slate-300 px-3 py-2">
              <MapPin className="h-4 w-4 text-primary" />
              <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Search or enter address"
                className="flex-1 bg-transparent text-sm focus:outline-none" />
              {coords && <span className="text-[11px] text-slate-400">{coords.lat.toFixed(3)}, {coords.lng.toFixed(3)}</span>}
            </div>
            <Button variant="outline" onClick={locate} disabled={locating}><Locate className="h-4 w-4" /> {locating ? 'Locating…' : 'GPS'}</Button>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Use GPS for current location, or type an address.</p>
        </div>

        <div className="flex justify-end gap-2 mt-5">
          <Button onClick={submit} disabled={submitting}>{submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />} Submit Report</Button>
        </div>
      </Card>
    </div>
  );
}

function Row({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex justify-between items-center text-sm">
      <span className="text-slate-500">{label}</span>
      <span className="font-semibold text-slate-800">{value}</span>
    </div>
  );
}
