import { useRef, useState, useEffect } from 'react';
import { Card, Button, Badge, SectionTitle } from '@/components/ui';
import { detectImage, DetectionResult } from '@/services/api';
import { severityColor } from '@/utils/format';
import { PageId } from '@/components/navItems';
import {
  Upload,
  Camera,
  ScanLine,
  RefreshCw,
  MapPin,
  Send,
  CheckCircle2,
  Loader2,
  ImageIcon,
} from 'lucide-react';

type Mode = 'idle' | 'preview' | 'analyzing' | 'result';

export function AIDetection({
  onNavigate,
}: {
  onNavigate: (p: PageId) => void;
}) {
  const [mode, setMode] = useState<Mode>('idle');
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [cameraOn, setCameraOn] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fileRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    return () => {
      stopCamera();

      if (imageUrl) {
        URL.revokeObjectURL(imageUrl);
      }
    };
  }, []);

  // -----------------------------
  // HANDLE IMAGE FILE
  // -----------------------------
  const handleFile = (file: File | undefined) => {
    if (!file) return;

    setError(null);

    if (imageUrl) {
      URL.revokeObjectURL(imageUrl);
    }

    setImageFile(file);
    setImageUrl(URL.createObjectURL(file));
    setResult(null);
    setMode('preview');
  };

  // -----------------------------
  // DRAG & DROP
  // -----------------------------
  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();

    const file = e.dataTransfer.files?.[0];

    if (file) {
      handleFile(file);
    }
  };

  // -----------------------------
  // AI DETECTION
  // -----------------------------
  const analyze = async () => {
    if (!imageFile) {
      setError('Please select an image first.');
      return;
    }

    setMode('analyzing');
    setError(null);

    try {
      console.log(
        'Sending actual image:',
        imageFile.name,
        imageFile.type,
        imageFile.size
      );

      const r = await detectImage(imageFile);

      console.log('Detection result:', r);

      setResult(r);
      setMode('result');
    } catch (error) {
      console.error('DETECTION ERROR:', error);

      setError('Analysis failed. Please retry.');
      setMode('preview');
    }
  };

  // -----------------------------
  // RESET
  // -----------------------------
  const reset = () => {
    if (imageUrl) {
      URL.revokeObjectURL(imageUrl);
    }

    setImageUrl(null);
    setImageFile(null);
    setResult(null);
    setMode('idle');
    setError(null);
  };

  // -----------------------------
  // START CAMERA
  // -----------------------------
  const startCamera = async () => {
    try {
      setError(null);

      const s = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment',
        },
      });

      streamRef.current = s;

      setCameraOn(true);

      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = s;
          videoRef.current.play();
        }
      }, 100);
    } catch (error) {
      console.error('Camera error:', error);

      setError(
        'Camera unavailable. You can upload a photo instead.'
      );
    }
  };

  // -----------------------------
  // STOP CAMERA
  // -----------------------------
  const stopCamera = () => {
    streamRef.current?.getTracks().forEach((track) => {
      track.stop();
    });

    streamRef.current = null;
    setCameraOn(false);
  };

  // -----------------------------
  // CAPTURE CAMERA IMAGE
  // -----------------------------
  const capture = () => {
    const video = videoRef.current;

    if (!video) return;

    const canvas = document.createElement('canvas');

    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    const context = canvas.getContext('2d');

    if (!context) return;

    context.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    );

    canvas.toBlob(
      (blob) => {
        if (!blob) return;

        const file = new File(
          [blob],
          'capture.jpg',
          {
            type: 'image/jpeg',
          }
        );

        handleFile(file);
        stopCamera();
      },
      'image/jpeg'
    );
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">

      {/* LEFT SIDE */}
      <div className="lg:col-span-3 space-y-4">

        <Card className="p-5">

          <SectionTitle
            title="Upload or Capture"
            subtitle="Drag & drop, browse, or use your camera"
          />

          {/* ERROR */}
          {error && (
            <div className="mb-3 rounded-lg bg-error/10 border border-error/20 text-error text-xs px-3 py-2">
              {error}
            </div>
          )}

          {/* UPLOAD AREA */}
          {mode === 'idle' && !cameraOn && (
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={onDrop}
              className="border-2 border-dashed border-slate-300 rounded-2xl p-10 text-center hover:border-primary/50 hover:bg-primary/5 transition-all"
            >
              <div className="mx-auto h-14 w-14 rounded-2xl bg-primary/10 grid place-items-center mb-3">
                <Upload className="h-7 w-7 text-primary" />
              </div>

              <p className="text-sm font-semibold text-slate-700">
                Drop an image here
              </p>

              <p className="text-xs text-slate-400 mt-1">
                JPG, PNG · up to 10MB
              </p>

              <div className="flex gap-2 justify-center mt-4">

                <Button
                  onClick={() => fileRef.current?.click()}
                >
                  <ImageIcon className="h-4 w-4" />
                  Browse
                </Button>

                <Button
                  variant="outline"
                  onClick={startCamera}
                >
                  <Camera className="h-4 w-4" />
                  Use Camera
                </Button>

              </div>

              <input
                ref={fileRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={(e) =>
                  handleFile(
                    e.target.files?.[0] || undefined
                  )
                }
              />
            </div>
          )}

          {/* CAMERA */}
          {cameraOn && (
            <div className="rounded-2xl overflow-hidden bg-black">

              <video
                ref={videoRef}
                className="w-full max-h-80 object-contain"
                playsInline
                muted
              />

              <div className="flex justify-center gap-3 p-3 bg-slate-900">

                <Button onClick={capture}>
                  <Camera className="h-4 w-4" />
                  Capture
                </Button>

                <Button
                  variant="outline"
                  onClick={stopCamera}
                  className="!border-white/30 !text-white"
                >
                  Cancel
                </Button>

              </div>
            </div>
          )}

          {/* IMAGE PREVIEW */}
          {mode !== 'idle' &&
            !cameraOn &&
            imageUrl && (
              <div className="relative">

                <img
                  src={imageUrl}
                  alt="Selected civic issue"
                  className="w-full max-h-96 object-contain rounded-2xl bg-slate-100"
                />

                {/* DETECTION RESULT BOX */}
                {mode === 'result' && result && (
                  <div
                    className="absolute border-2 border-accent rounded-lg"
                    style={{
                      left: `${result.bbox.x}%`,
                      top: `${result.bbox.y}%`,
                      width: `${result.bbox.w}%`,
                      height: `${result.bbox.h}%`,
                    }}
                  >
                    <span className="absolute -top-6 left-0 bg-accent text-white text-[10px] font-semibold px-2 py-0.5 rounded-md">
                      {result.category} {result.confidence}%
                    </span>
                  </div>
                )}

                {/* ANALYZING OVERLAY */}
                {mode === 'analyzing' && (
                  <div className="absolute inset-0 grid place-items-center bg-black/40 rounded-2xl">

                    <div className="text-white text-center">

                      <Loader2 className="h-8 w-8 mx-auto animate-spin" />

                      <p className="mt-2 text-sm">
                        Running YOLO inference…
                      </p>

                    </div>

                  </div>
                )}

              </div>
            )}

          {/* BUTTONS */}
          {mode !== 'idle' && !cameraOn && (
            <div className="flex gap-2 mt-4">

              {mode === 'preview' && (
                <Button onClick={analyze}>
                  <ScanLine className="h-4 w-4" />
                  Analyze with AI
                </Button>
              )}

              {mode === 'result' && (
                <Button
                  onClick={() => onNavigate('report')}
                >
                  <Send className="h-4 w-4" />
                  Create Report
                </Button>
              )}

              <Button
                variant="outline"
                onClick={() => fileRef.current?.click()}
              >
                Change
              </Button>

              <Button
                variant="ghost"
                onClick={reset}
              >
                <RefreshCw className="h-4 w-4" />
                Reset
              </Button>

            </div>
          )}

        </Card>

      </div>

      {/* RIGHT SIDE */}
      <div className="lg:col-span-2">

        <Card className="p-5 sticky top-4">

          <SectionTitle
            title="Detection Result"
            subtitle="AI inference output"
          />

          {/* EMPTY RESULT */}
          {!result && mode !== 'analyzing' && (
            <div className="text-center py-12 text-slate-400">

              <ScanLine className="h-10 w-10 mx-auto mb-2 opacity-40" />

              <p className="text-sm">
                Upload an image and run analysis to see results here.
              </p>

            </div>
          )}

          {/* LOADING */}
          {mode === 'analyzing' && (
            <div className="text-center py-12 text-slate-500">

              <Loader2 className="h-8 w-8 mx-auto animate-spin text-primary" />

              <p className="text-sm mt-2">
                Detecting issues…
              </p>

            </div>
          )}

          {/* RESULT */}
          {mode === 'result' && result && (
            <div className="space-y-4">

              <div className="rounded-xl bg-primary/5 border border-primary/20 p-4">

                <div className="flex items-center justify-between">

                  <div className="text-xs text-slate-500">
                    Detected Issue
                  </div>

                  <Badge
                    text={result.severity}
                    className={severityColor(result.severity)}
                  />

                </div>

                <div className="text-lg font-bold text-slate-800 mt-1">
                  {result.category}
                </div>

                <div className="mt-2">

                  <div className="flex justify-between text-xs text-slate-500 mb-1">
                    <span>Confidence</span>

                    <span className="font-semibold">
                      {result.confidence}%
                    </span>
                  </div>

                  <div className="h-2 rounded-full bg-slate-200 overflow-hidden">

                    <div
                      className="h-full bg-primary rounded-full"
                      style={{
                        width: `${result.confidence}%`,
                      }}
                    />

                  </div>

                </div>

              </div>

              <Row
                label="Recommended Action"
                value={result.recommendedAction}
              />

              <Row
                label="Assigned Department"
                value={result.department}
                icon={
                  <MapPin className="h-3.5 w-3.5" />
                }
              />

              <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 flex items-start gap-2">

                <CheckCircle2 className="h-4 w-4 text-emerald-600 mt-0.5" />

                <p className="text-xs text-emerald-700">
                  Ready to file as a citizen report with
                  location and severity pre-filled.
                </p>

              </div>

            </div>
          )}

        </Card>

      </div>

    </div>
  );
}

function Row({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
  icon?: React.ReactNode;
}) {
  return (
    <div>

      <div className="text-xs text-slate-500 mb-1">
        {label}
      </div>

      <div className="text-sm text-slate-800 flex items-start gap-1.5">
        {icon}
        {value}
      </div>

    </div>
  );
}