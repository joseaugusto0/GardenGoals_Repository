/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.tsx"],
  theme: {
    extend: {},
    colors: {
        secondary: {
          500: "#836177"
        },
        background: {
          500: "#53736D",
          300: "#77A493",
          100: "#1B7D6D"
        }
    }
  },
  plugins: [],
}
