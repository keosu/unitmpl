/* 产引入jsencrypt实现数据RSA加密 */
import JSEncrypt from 'jsencrypt' // 处理长文本数据时报错 jsencrypt.js Message too long for RSA
/* 产引入encryptlong实现数据RSA加密 */
// import Encrypt from 'encryptlong' // encryptlong是基于jsencrypt扩展的长文本分段加解密功能。

// 密钥对生成 http://web.chacuo.net/netrsakeypair

// 公钥key
const publicKey ='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAttmiuxfkK0eunCue8la9B0oPGgkVlNACvHiB2IgOqoeHKm8AJMwWdd8m5FNPAQeIEYqyPt8o+AGEODZmB4eb1A/umBm/btb+/J7U3cWQ87oTyMSFQFEaEBhg20sNZ2y1sRvyaRZv4gwGfTqqfsOw0+JH5rdmNzP9V0SSMFkjFIrUY9jT9P+yUTE2itlW3g63B3BlPIJalhUuye8pnHEklAlHRDt/3ksuLANJVShRQlQ2yDHWM2yywHr9xILBxvfZ8fiKT6YFvdyvtY3kL6ApLMjzwujBnGLzdb+ned74NG2oKBPB7qMbkoddzCFN5AqBf6wsj2/Ki2J2kcaJCtSshQIDAQAB'
// 私钥key
const privateKey = ''

export default {
  /* JSEncrypt加密 */
  rsaPublicData(data) {
    let jsencrypt = new JSEncrypt()
    jsencrypt.setPublicKey(publicKey)
    // 如果是对象/数组的话，需要先JSON.stringify转换成字符串
    let result = jsencrypt.encrypt(data)
    return result
  },
  /* JSEncrypt解密 */
  rsaPrivateData(data) {
    let jsencrypt = new JSEncrypt()
    jsencrypt.setPrivateKey(privateKey)
    // 如果是对象/数组的话，需要先JSON.stringify转换成字符串
    let result = jsencrypt.encrypt(data)
    return result
  }
}
