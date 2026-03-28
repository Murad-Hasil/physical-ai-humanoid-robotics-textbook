/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx,md,mdx}',
    './docs/**/*.{md,mdx}',
    './blog/**/*.{md,mdx}',
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        'cyber-black': '#111111',
        'surface-dark': '#1A1A2E',
        'neon-blue': {
          DEFAULT: '#00F3FF',
          50: '#E0FFFF',
          100: '#B0FFFF',
          200: '#80FFFF',
          300: '#40FFFF',
          400: '#00F3FF',
          500: '#00E0E0',
          600: '#00B0B0',
          700: '#008080',
          800: '#004040',
          900: '#002020',
        },
        'neon-orange': {
          DEFAULT: '#FF6B35',
          50: '#FFE0D0',
          100: '#FFC0A0',
          200: '#FFA070',
          300: '#FF8040',
          400: '#FF6B35',
          500: '#E05020',
          600: '#B03010',
          700: '#802010',
          800: '#501008',
          900: '#280804',
        },
        'electric-blue': {
          DEFAULT: '#0080FF',
          50: '#E0F0FF',
          100: '#B0D8FF',
          200: '#80B8FF',
          300: '#4090FF',
          400: '#0080FF',
          500: '#0068D8',
          600: '#0050A8',
          700: '#003878',
          800: '#002048',
          900: '#001028',
        },
        'glass': {
          bg: 'rgba(26, 26, 46, 0.6)',
          'bg-dark': 'rgba(0, 0, 0, 0.2)',
          border: 'rgba(0, 243, 255, 0.3)',
          'border-dark': 'rgba(255, 255, 255, 0.1)',
        },
      },
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '8px',
        lg: '16px',
        xl: '24px',
      },
      boxShadow: {
        'neon-blue': '0 0 10px rgba(0, 243, 255, 0.5), 0 0 20px rgba(0, 243, 255, 0.3), 0 0 30px rgba(0, 243, 255, 0.2)',
        'neon-blue-sm': '0 0 5px rgba(0, 243, 255, 0.5), 0 0 10px rgba(0, 243, 255, 0.3)',
        'neon-blue-lg': '0 0 20px rgba(0, 243, 255, 0.6), 0 0 40px rgba(0, 243, 255, 0.4), 0 0 60px rgba(0, 243, 255, 0.2)',
        'neon-orange': '0 0 10px rgba(255, 107, 53, 0.5), 0 0 20px rgba(255, 107, 53, 0.3)',
        'electric-blue': '0 0 10px rgba(0, 128, 255, 0.5), 0 0 20px rgba(0, 128, 255, 0.3)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
      },
      animation: {
        'glow': 'glow 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'pulse-cyan': 'pulse-cyan 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scanline': 'scanline 1.5s linear infinite',
        'neon-pulse': 'neon-pulse 2s ease-in-out infinite',
        'glass-shimmer': 'glass-shimmer 3s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%, 100%': {
            boxShadow: '0 0 10px rgba(0, 243, 255, 0.5), 0 0 20px rgba(0, 243, 255, 0.3)',
          },
          '50%': {
            boxShadow: '0 0 20px rgba(0, 243, 255, 0.8), 0 0 40px rgba(0, 243, 255, 0.5)',
          },
        },
        float: {
          '0%, 100%': {
            transform: 'translateY(0)',
          },
          '50%': {
            transform: 'translateY(-10px)',
          },
        },
        'pulse-cyan': {
          '0%, 100%': {
            opacity: '1',
            boxShadow: '0 0 10px rgba(0, 243, 255, 0.5)',
          },
          '50%': {
            opacity: '0.5',
            boxShadow: '0 0 20px rgba(0, 243, 255, 0.8)',
          },
        },
        scanline: {
          '0%': {
            transform: 'translateY(-100%)',
          },
          '100%': {
            transform: 'translateY(100%)',
          },
        },
        'neon-pulse': {
          '0%, 100%': {
            boxShadow: '0 0 10px rgba(0, 243, 255, 0.5), 0 0 20px rgba(0, 243, 255, 0.3), 0 0 30px rgba(0, 243, 255, 0.2)',
          },
          '50%': {
            boxShadow: '0 0 20px rgba(0, 243, 255, 0.8), 0 0 40px rgba(0, 243, 255, 0.5), 0 0 60px rgba(0, 243, 255, 0.3)',
          },
        },
        'glass-shimmer': {
          '0%': {
            background: 'linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0.1) 100%)',
          },
          '50%': {
            background: 'linear-gradient(45deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.15) 100%)',
          },
          '100%': {
            background: 'linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0.1) 100%)',
          },
        },
      },
    },
  },
  plugins: [],
  corePlugins: {
    // Don't preflight to avoid conflicts with Docusaurus/Infima
    preflight: false,
  },
};
