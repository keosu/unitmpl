/**
 * get localStorage 获取本地存储
 * @param { String } key
 */
export function getLocal(key) {
  try {
    if (!key) throw new Error('key is empty')
    const value = uni.getStorageSync(key)
    // 确保返回值不为undefined
    return value ? JSON.parse(value) : null
  } catch (error) {
    console.error('getLocal error:', error)
    return null
  }
}

/**
 * set localStorage 设置本地存储
 * @param { String } key
 * @param value
 */
export function setLocal(key, value) {
  try {
    if (!key) throw new Error('key is empty')
    if (value === undefined || value === null) return
    uni.setStorageSync(key, JSON.stringify(value))
  } catch (error) {
    console.error('setLocal error:', error)
  }
}

/**
 * remove localStorage 移除某个本地存储
 * @param { String } key
 */
export function removeLocal(key) {
  try {
    if (!key) throw new Error('key is empty')
    return uni.removeStorageSync(key)
  } catch (error) {
    console.error('removeLocal error:', error)
    return false
  }
}

/**
 * clear localStorage 清除本地存储
 */
export function clearLocal() {
  try {
    return uni.clearStorageSync()
  } catch (error) {
    console.error('clearLocal error:', error)
    return false
  }
}