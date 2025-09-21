/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        montserrat: ["Montserrat", "sans-serif"],
        poppins: ["Poppins", "sans-serif"],
        script: ["Dancing Script", "cursive"],
      },
      colors: {
        driftaway: "#2bc8bd",
      },
    },
  },
  plugins: [],
};
