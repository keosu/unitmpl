import { getLocal, removeLocal, setLocal } from '../localStorage'

const tokenKey = 'App-Token'
const userKey = 'App-User'

export function getToken() {
  return getLocal(tokenKey)
}

export function setToken(token) {
  return setLocal(tokenKey, token)
}

export function getUser() {
  if (getLocal(userKey)) {
    return JSON.parse(getLocal(userKey))
  } else {
    return {}
  }
}

export function setUser(user) {
  return setLocal(userKey, JSON.stringify(user))
}

export function removeToken() {
  return removeLocal(tokenKey)
}

export function removeUser() {
  return removeLocal(userKey)
}
