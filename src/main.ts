import { createApp } from 'vue';
import App from './App.vue';
import { router } from './router';
import vuetify from './plugins/vuetify';
import '@/scss/style.scss';
// import PerfectScrollbar from 'vue3-perfect-scrollbar';
import VueApexCharts from 'vue3-apexcharts';
import TemplateSelection from './views/pages/TemplateSelection.vue';
import VueTablerIcons from 'vue-tabler-icons';
import Maska from 'maska';
const app = createApp(App);


createApp(TemplateSelection).mount('#app');
app.use(router);
// app.use(PerfectScrollbar);
app.use(VueTablerIcons);
app.use(Maska);
app.use(VueApexCharts);
app.use(vuetify).mount('#app');
