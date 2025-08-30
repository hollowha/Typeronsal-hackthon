/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
    "./app.vue"
  ],
  theme: {
    extend: {
      colors: {
        'brand-orange': '#E29930',
        'brand-amber': '#ea580c',
        'brand-teal': '#3A6B60',
        'brand-teal-light': '#5EA897',
      },
      screens: {
        'xs': '475px',
        '3xl': '1600px',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.75rem' }],
        '10xl': ['10rem', { lineHeight: '1' }],
        '11xl': ['12rem', { lineHeight: '1' }],
      },
      animation: {
        'float-slow': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s ease-in-out infinite',
        'bounce-gentle': 'bounce 3s ease-in-out infinite',
      },
    },
  },
  plugins: [
    function({ addUtilities }) {
      addUtilities({
        '.touch-manipulation': {
          'touch-action': 'manipulation',
        },
        '.scroll-smooth': {
          'scroll-behavior': 'smooth',
        },
        '.text-balance': {
          'text-wrap': 'balance',
        },
      })
    }
  ],
}

