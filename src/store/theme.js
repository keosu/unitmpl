import { defineStore } from 'pinia'
import { getLocal, setLocal } from '@/utils/localStorage.js'

export const useThemeStore = defineStore('theme', {
	state: () => ({
		currentTheme: getLocal('theme') || 'light'  // 默认使用浅色主题
	}),
	
	actions: {
		// 初始化主题
		initTheme() {
			const savedTheme = getLocal('theme')
			if (savedTheme) {
				this.currentTheme = savedTheme
			} else {
				// 如果没有保存的主题，默认使用浅色并保存
				this.currentTheme = 'light'
				setLocal('theme', 'light')
			}
			
			// 初始化HTML根元素的主题类（适用于H5）
			if (typeof document !== 'undefined') {
				document.documentElement.classList.add(`theme-${this.currentTheme}`)
				document.body.classList.add(`theme-${this.currentTheme}`)
			}
		},
		
		// 设置主题（统一方法名）
		setTheme(theme) {
			if (theme && theme !== this.currentTheme) {
				this.currentTheme = theme
				setLocal('theme', theme)
				
				// 更新HTML根元素的主题类（适用于H5）
				if (typeof document !== 'undefined') {
					document.documentElement.className = document.documentElement.className
						.replace(/theme-\w+/g, '')
					document.documentElement.classList.add(`theme-${theme}`)
					
					// 同时更新body
					document.body.className = document.body.className
						.replace(/theme-\w+/g, '')
					document.body.classList.add(`theme-${theme}`)
				}
				
				console.log('主题已切换到:', theme)
			}
		},
		
		// 切换主题（兼容旧方法名）
		switchTheme(theme) {
			this.setTheme(theme)
		},
		
		// 获取当前主题
		getCurrentTheme() {
			return this.currentTheme
		},
		
		// 切换到另一个主题
		toggleTheme() {
			const newTheme = this.currentTheme === 'light' ? 'dark' : 'light'
			this.setTheme(newTheme)
		}
	}
})
