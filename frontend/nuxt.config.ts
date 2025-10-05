import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-10-05",
  devtools: { enabled: true },
  ssr: false,
  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBaseUrl: 'https://ocie-coua-exquisitely.ngrok-free.dev', // Will be automatically populated from NUXT_PUBLIC_API_BASE_URL
      apiVersion: 'v1',
      apiTimeout: 30000,
      apiDebug: false
    }
  },

  vite: {
    plugins: [
      tailwindcss(),
    ],
  },

  modules: ["@nuxt/image"],
});