import { defineStore } from 'pinia'
import { getLocal, setLocal } from '@/utils/localStorage.js'

export const useThemeStore = defineStore('theme', {
	state: () => ({
		currentTheme: 'dark'
	}),
	
	actions: {
		// 初始化主题
		initTheme() {
			const savedTheme = getLocal('theme')
			if (savedTheme) {
				this.currentTheme = savedTheme
			}
		},
		
		// 切换主题
		switchTheme(theme) {
			if (theme !== this.currentTheme) {
				this.currentTheme = theme
				setLocal('theme', theme)
				console.log('主题已切换到:', theme)
			}
		},
		
		// 获取当前主题
		getCurrentTheme() {
			return this.currentTheme
		}
	}
})
