import CryptoJS from 'crypto-js'
// import Qs from 'qs'
let keyStr = 'LWOBTHyQNtGn3hoW'
let ivStr = 'HW8wxCRzrZW0jyMC'

// RSA加密

/**
 *
 * 第一个参数word是待加密或者解密的字符串；
 * 第二个参数keyStr是aes加密需要用到的16位字符串的key；
 * 第三个参数是初始化向量 iv。
 */
export default {
  // 加密
  encrypt(data) {
    let word = JSON.stringify(data)
    let key = CryptoJS.enc.Utf8.parse(keyStr)
    let iv = CryptoJS.enc.Utf8.parse(ivStr)
    // let srcs = CryptoJS.enc.Utf8.parse(word)

    let encrypted = CryptoJS.AES.encrypt(word, key, {
      iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    })
    return encrypted.toString()
  },
  // 解密
  decrypt(word) {
    let key = CryptoJS.enc.Utf8.parse(keyStr)
    let iv = CryptoJS.enc.Utf8.parse(ivStr)

    let decrypt = CryptoJS.AES.decrypt(word, key, {
      iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    })
    let dataStr = CryptoJS.enc.Utf8.stringify(decrypt)
    try {
      return JSON.parse(dataStr)
    } catch (err) {
      return dataStr
    }
  },
  // 将参数转成Md5加密
  getMd5(data) {
    let ascii = sortByASCII(data)
    let t = getTimestamp()
    ascii.t = t
    ascii.key = keyStr
    let sortStr = ObjToString(ascii)
    let md5 = CryptoJS.MD5(sortStr).toString().toUpperCase()
    return {
      t: t,
      sign: md5
    }
  }
}

function getTimestamp() {
  return new Date().getTime()
}
/* 对象按照ASCII值排序 */
function sortByASCII(obj) {
  let arr = []
  let num = 0
  for (let i in obj) {
    arr[num] = i
    num++
  }
  let sortArr = arr.sort()
  let sortObj = {}
  for (let i in sortArr) {
    let key = sortArr[i]
    let val = obj[key]
    if (val || val === 0 || val === false) {
      sortObj[key] = val
    }
  }
  return sortObj
}
/* 对象转成 url请求参数 */
function ObjToString(data) {
  let strArr = []
  for (let key in data) {
    strArr.push(`${key}=${data[key]}`)
  }
  return strArr.join('&')
}
