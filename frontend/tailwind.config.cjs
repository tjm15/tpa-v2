module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        cta: {
          DEFAULT: '#f5c315', // Call to Action (Bright Yellow)
        },
        heading: {
          DEFAULT: '#2a3a60', // Primary Text / Headings (Deep Navy)
        },
        panel: {
          DEFAULT: '#e6e6ef', // Background / Panels (Light Grey-Lavender)
        },
        accent: {
          DEFAULT: '#329c85', // Accent / Tagline (Soft Teal-Green)
        },
        body: {
          DEFAULT: '#545c6d', // Body Text / Secondary UI (Muted Grey-Blue)
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'), // Add this line
  ],
};
