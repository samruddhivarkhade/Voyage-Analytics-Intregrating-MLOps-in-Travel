/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Flight website palette - bright, modern, clean
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          600: '#0084FF',
          700: '#0073E6',
          800: '#005FCC',
          900: '#003399',
        },
        secondary: {
          600: '#00BCD4',
          700: '#00A8C8',
        },
        accent: '#FF6B35',
        dark: {
          50: '#1F2937',
          200: '#4B5563',
          900: '#111827',
        },
        surface: '#FFFFFF',
        'surface-alt': '#F8FAFB',
      },
      fontFamily: {
        serif: ['Playfair Display', 'DM Serif Display', 'serif'],
        sans: ['DM Sans', 'Sora', 'Plus Jakarta Sans', 'Outfit', 'sans-serif'],
      },
      backgroundImage: {
        'grain': 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 400 400\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' result=\'noise\' /%3E%3C/filter%3E%3Crect width=\'400\' height=\'400\' filter=\'url(%23noise)\' opacity=\'0.05\'/%3E%3C/svg%3E")',
        'gradient-warm': 'linear-gradient(135deg, #0084FF 0%, #00BCD4 100%)',
        'gradient-dark': 'linear-gradient(135deg, #F8FAFB 0%, #FFFFFF 100%)',
      },
      boxShadow: {
        'glow': '0 0 20px rgba(0, 132, 255, 0.2)',
        'glow-red': '0 0 20px rgba(255, 107, 53, 0.2)',
      },
      keyframes: {
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(400px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
      },
      animation: {
        slideUp: 'slideUp 0.6s ease-out',
        fadeIn: 'fadeIn 0.6s ease-out',
        scaleIn: 'scaleIn 0.5s ease-out',
        'slide-in': 'slideIn 0.3s ease-out',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}

