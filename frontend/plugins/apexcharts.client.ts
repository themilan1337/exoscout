import VueApexCharts from 'vue3-apexcharts'

export default defineNuxtPlugin({
  name: 'apexcharts',
  setup(nuxtApp) {
    nuxtApp.vueApp.use(VueApexCharts)
  }
})