/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#0b8276',
        'primary-dark': '#0a6b60',
        secondary: '#0a6b60',
        accent: '#ef7d4d',
        success: '#10b981',
        warning: '#f59e0b',
        error: '#e5484d',
        info: '#1d9bf0',
        sidebar: '#0c4f48',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        card: '0 1px 2px rgba(16,24,40,0.04), 0 1px 3px rgba(16,24,40,0.06)',
        soft: '0 4px 16px rgba(16,24,40,0.06)',
      },
    },
  },
  plugins: [],
};
