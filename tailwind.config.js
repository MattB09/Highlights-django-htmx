const colors = require('tailwindcss/colors')

module.exports = {
  content: [
    "**/templates/**/*.html"
  ],
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      black: colors.black,
      white: colors.white,
      gray: colors.gray,
      indigo: colors.indigo,
      red: colors.red,
      sky: colors.sky,
    },
    extend: {
      fontFamily: {
        inherit: 'inherit'
      }
    },
  },
  plugins: [],
}
