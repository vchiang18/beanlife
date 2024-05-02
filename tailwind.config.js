// // docker directions
// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   purge: [],
//   darkMode: false, // or 'media' or 'class'
//   theme: {
//     extend: {},
//   },
//   variants: {
//     extend: {},
//   },
//   plugins: [],
// }

// venv directions
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // './app-name/templates/app-name/**/*.html',
    './servings/templates/servings/**/*.html',
    './users/templates/registration/**/*.html',
    // Add paths to other apps if necessary
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
