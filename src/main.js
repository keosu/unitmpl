import {
	createSSRApp
} from "vue";
import App from "./App.vue";
import uviewPlus from 'uview-plus'

import i18n from "./language";
import './styles/theme.css'
import './styles/theme-extended.css'
import './styles/theme-global.css'

import * as Pinia from 'pinia';
import { useThemeStore } from './store/theme.js'

export function createApp() {
	const app = createSSRApp(App);
	const pinia = Pinia.createPinia()
	
	app.use(uviewPlus)
	app.use(i18n)
	app.use(pinia)
	
	// 初始化主题
	const themeStore = useThemeStore(pinia)
	themeStore.initTheme()
	
	return {
		app,
		Pinia
	};
}
