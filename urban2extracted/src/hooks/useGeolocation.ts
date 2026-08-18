export function useGeolocation(): Promise<{ lat: number; lng: number; label: string }> {
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      resolve({ lat: 22.7196, lng: 75.8577, label: 'Indore (default)' });
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude, label: 'Current GPS location' }),
      () => resolve({ lat: 22.7196, lng: 75.8577, label: 'Indore (fallback)' }),
      { timeout: 5000 }
    );
  });
}
