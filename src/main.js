import {
	createSSRApp
} from "vue";
import App from "./App.vue";
import uviewPlus from 'uview-plus'

import i18n from "./language";
import './styles/theme.css'
import './styles/theme-extended.css'

import * as Pinia from 'pinia';
export function createApp() {
	const app = createSSRApp(App);
	app.use(uviewPlus)
	app.use(i18n)
	app.use(Pinia.createPinia())
	
	return {
		app,
	};
}
