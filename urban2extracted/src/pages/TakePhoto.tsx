import { useRef, useState, useEffect } from 'react';
import { Card, Button, Badge, SectionTitle } from '@/components/ui';
import { detectImage, DetectionResult } from '@/services/api';
import { severityColor } from '@/utils/format';
import { PageId } from '@/components/navItems';
import { Camera, ScanLine, RefreshCw, Send, CheckCircle2, Loader2 } from 'lucide-react';

type Step = 'camera' | 'preview' | 'analyzing' | 'result';

export function TakePhoto({ onNavigate }: { onNavigate: (p: PageId) => void }) {
  const [step, setStep] = useState<Step>('camera');
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => { startCamera(); return () => stopCamera(); }, []);

  const startCamera = async () => {
    try {
      const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      streamRef.current = s;
      setTimeout(() => { if (videoRef.current) { videoRef.current.srcObject = s; videoRef.current.play(); } }, 50);
    } catch {
      setError('Camera not available. Use AI Detection to upload an image instead.');
    }
  };

  const stopCamera = () => { streamRef.current?.getTracks().forEach((t) => t.stop()); streamRef.current = null; };

  const capture = () => {
    const v = videoRef.current;
    if (!v) return;
    const canvas = document.createElement('canvas');
    canvas.width = v.videoWidth || 640; canvas.height = v.videoHeight || 480;
    canvas.getContext('2d')?.drawImage(v, 0, 0);
    canvas.toBlob((b) => {
      if (!b) return;
      setImageUrl(URL.createObjectURL(b));
      setStep('preview');
      stopCamera();
    }, 'image/jpeg');
  };

  const analyze = async () => {
    setStep('analyzing');
    const r = await detectImage(new Blob());
    setResult(r);
    setStep('result');
  };

  const reset = () => {
    if (imageUrl) URL.revokeObjectURL(imageUrl);
    setImageUrl(null); setResult(null); setError(null); setStep('camera'); startCamera();
  };

  return (
    <div className="max-w-3xl mx-auto space-y-4">
      <Card className="p-5">
        <SectionTitle title="Camera Capture" subtitle="Capture → Preview → Analyze → Report" />
        {error && <div className="mb-3 rounded-lg bg-error/10 border border-error/20 text-error text-xs px-3 py-2">{error}</div>}

        {step === 'camera' && (
          <div className="rounded-2xl overflow-hidden bg-black">
            <video ref={videoRef} className="w-full max-h-96 object-contain" playsInline muted />
            <div className="flex justify-center p-4 bg-slate-900">
              <Button onClick={capture}><Camera className="h-4 w-4" /> Capture Photo</Button>
            </div>
          </div>
        )}

        {(step === 'preview' || step === 'analyzing' || step === 'result') && imageUrl && (
          <div className="relative">
            <img src={imageUrl} alt="capture" className="w-full max-h-96 object-contain rounded-2xl bg-slate-100" />
            {step === 'result' && result && (
              <div className="absolute border-2 border-accent rounded-lg" style={{ left: `${result.bbox.x}%`, top: `${result.bbox.y}%`, width: `${result.bbox.w}%`, height: `${result.bbox.h}%` }}>
                <span className="absolute -top-6 left-0 bg-accent text-white text-[10px] font-semibold px-2 py-0.5 rounded-md">{result.category} {result.confidence}%</span>
              </div>
            )}
            {step === 'analyzing' && (
              <div className="absolute inset-0 grid place-items-center bg-black/40 rounded-2xl text-white">
                <div className="text-center"><Loader2 className="h-8 w-8 mx-auto animate-spin" /><p className="mt-2 text-sm">Analyzing…</p></div>
              </div>
            )}
          </div>
        )}

        <div className="flex gap-2 mt-4">
          {step === 'preview' && <Button onClick={analyze}><ScanLine className="h-4 w-4" /> Analyze</Button>}
          {step === 'result' && <Button onClick={() => onNavigate('report')}><Send className="h-4 w-4" /> File Report</Button>}
          {step !== 'camera' && step !== 'analyzing' && <Button variant="ghost" onClick={reset}><RefreshCw className="h-4 w-4" /> Retake</Button>}
        </div>
      </Card>

      {step === 'result' && result && (
        <Card className="p-5">
          <SectionTitle title="AI Detection Result" />
          <div className="flex items-center gap-3 mb-3">
            <Badge text={result.category} className="border-primary/30 bg-primary/10 text-primary" />
            <Badge text={result.severity} className={severityColor(result.severity)} />
            <span className="text-xs text-slate-500">Confidence {result.confidence}%</span>
          </div>
          <div className="text-sm text-slate-700"><b>Action:</b> {result.recommendedAction}</div>
          <div className="text-sm text-slate-700 mt-1"><b>Dept:</b> {result.department}</div>
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 mt-3 flex items-start gap-2">
            <CheckCircle2 className="h-4 w-4 text-emerald-600 mt-0.5" />
            <p className="text-xs text-emerald-700">Detection ready. File a report to assign it to the responsible department.</p>
          </div>
        </Card>
      )}
    </div>
  );
}
