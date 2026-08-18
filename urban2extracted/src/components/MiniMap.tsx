import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import { UrbanIssue } from '@/data/mockData';
import { severityDot } from '@/utils/format';

delete (L.Icon.Default.prototype as unknown as { _getIconUrl?: unknown })._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const iconFor = (color: string) =>
  L.divIcon({
    className: 'ue-marker',
    html: `<span style="display:block;width:14px;height:14px;border-radius:50%;background:${color};border:2.5px solid white;box-shadow:0 1px 4px rgba(0,0,0,.4)"></span>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  });

interface Props {
  issues: UrbanIssue[];
  height?: string;
  interactive?: boolean;
  showHotspots?: boolean;
  onMarkerClick?: (i: UrbanIssue) => void;
}

export function MiniMap({ issues, height = '320px', showHotspots = true, onMarkerClick }: Props) {
  return (
    <div style={{ height }} className="rounded-2xl overflow-hidden border border-slate-200">
      <MapContainer center={[22.7196, 75.8577]} zoom={12} scrollWheelZoom className="h-full w-full">
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap" />
        {showHotspots && issues.filter((i) => i.severity === 'Critical' || i.severity === 'High').map((i) => (
          <Circle key={`h-${i.id}`} center={[i.lat, i.lng]} radius={600} pathOptions={{ color: severityDot(i.severity), fillOpacity: 0.15 }} />
        ))}
        {issues.map((i) => (
          <Marker key={i.id} position={[i.lat, i.lng]} icon={iconFor(severityDot(i.severity))} eventHandlers={{ click: () => onMarkerClick?.(i) }}>
            <Popup>
              <div className="text-xs">
                <div className="font-semibold text-slate-800">{i.issue}</div>
                <div className="text-slate-500">{i.location} · {i.ward}</div>
                <div className="mt-1">Severity: <b>{i.severity}</b></div>
                <div>Status: {i.status} · {i.department}</div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
