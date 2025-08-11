/**
 * get localStorage 获取本地存储
 * @param { String } key
 */
export function getLocal(key) {
  if (!key) throw new Error('key is empty')
  const value = uni.getStorageSync(key)
  return value ? JSON.parse(value) : null
}

/**
 * set localStorage 设置本地存储
 * @param { String } key
 * @param value
 */
export function setLocal(key, value) {
  if (!key) throw new Error('key is empty')
  if (!value) return
  uni.setStorageSync(key, JSON.stringify(value))
}

/**
 * remove localStorage 移除某个本地存储
 * @param { String } key
 */
export function removeLocal(key) {
  if (!key) throw new Error('key is empty')
  return uni.removeStorageSync(key)
}

/**
 * clear localStorage 清除本地存储
 */
export function clearLocal() {
  return uni.clearStorageSync()
}
