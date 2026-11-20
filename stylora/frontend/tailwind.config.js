/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: {
          50: '#FDFCFB',
          100: '#FAF7F2',
          200: '#F5EFEB',
          300: '#EAE2D7',
          400: '#DED3C4',
        },
        lavender: {
          50: '#FAF8FD',
          100: '#F3EDFB',
          200: '#E5D8F7',
          300: '#D1BCF0',
          400: '#A78BFA',
          500: '#8B5CF6',
          600: '#7C3AED',
          700: '#6D28D9',
        },
        softpink: {
          50: '#FDF4F8',
          100: '#FCE7F3',
          200: '#FBCFE8',
          300: '#F9A8D4',
          400: '#F472B6',
          500: '#EC4899',
        },
        charcoal: {
          50: '#F6F7F9',
          100: '#ECEEF2',
          200: '#D5D8E0',
          300: '#9EA4B3',
          600: '#474D5A',
          700: '#323742',
          800: '#22252D',
          900: '#17191F',
          950: '#0E1014',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
        serif: ['Playfair Display', 'Georgia', 'serif'],
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(34, 37, 45, 0.05), 0 2px 6px -1px rgba(34, 37, 45, 0.03)',
        'soft-lg': '0 12px 30px -4px rgba(34, 37, 45, 0.08), 0 4px 10px -2px rgba(34, 37, 45, 0.04)',
        'glow-lavender': '0 0 25px -5px rgba(139, 92, 246, 0.25)',
      }
    },
  },
  plugins: [],
}
