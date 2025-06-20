/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    '../../../**/*.{html,py,js}',
  ],
  plugins: [require('daisyui')],
  daisyui: {
    themes: ['light', 'dark','cupcake'], // ou autres thèmes : ['cupcake', 'dracula']
  },
}
