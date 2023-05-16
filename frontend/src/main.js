import './assets/main.css'

import { createApp } from 'vue'
import Popper from "vue3-popper";
import App from './App.vue'

createApp(App).mount('#app')
App.component("Popper",Popper)