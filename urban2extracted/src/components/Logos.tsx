export function UrbanEyeLogo({ className = 'h-9 w-9' }: { className?: string }) {
  return (
    <svg viewBox="0 0 48 48" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="48" height="48" rx="12" fill="url(#ue-bg)" />
      <path d="M9 24c4-7 9-10 15-10s11 3 15 10c-4 7-9 10-15 10S13 31 9 24Z" fill="white" fillOpacity="0.16" stroke="white" strokeWidth="2" strokeLinejoin="round" />
      <circle cx="24" cy="24" r="6" fill="white" />
      <circle cx="24" cy="24" r="2.6" fill="#0b8276" />
      <circle cx="25.6" cy="22.4" r="1.1" fill="white" />
      <defs>
        <linearGradient id="ue-bg" x1="6" y1="6" x2="42" y2="42" gradientUnits="userSpaceOnUse">
          <stop stopColor="#0b8276" />
          <stop offset="1" stopColor="#0a6b60" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export function SwachhBharatLogo({ className = 'h-12 w-12' }: { className?: string }) {
  return (
    <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="32" cy="32" r="31" fill="white" stroke="#0b8276" strokeWidth="1.5" />
      <path d="M32 9c-2.2 4.5-5.2 6.8-9 8.2 0 6.8 3.4 12 9 14.5 5.6-2.5 9-7.7 9-14.5-3.8-1.4-6.8-3.7-9-8.2Z" fill="#0b8276" />
      <circle cx="32" cy="32" r="4.5" fill="#fff" />
      <circle cx="32" cy="32" r="2.2" fill="#0b8276" />
      <path d="M14 50c5 4 12 5 18 5s13-1 18-5" stroke="#ef7d4d" strokeWidth="3" strokeLinecap="round" />
      <text x="32" y="60" textAnchor="middle" fontFamily="Arial, sans-serif" fontSize="6.5" fontWeight="700" fill="#0b8276">SWACHH</text>
    </svg>
  );
}
