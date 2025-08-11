import smCrypto from 'sm-crypto'
const sm2 = smCrypto.sm2
const sm3 = smCrypto.sm3
const sm4 = smCrypto.sm4
const publicKey = import.meta.env.VITE_APP_PUBLIC_KEY //公钥
const privateKey = import.meta.env.VITE_APP_PRIVATE_KEY //私钥
const KEY = import.meta.env.VITE_APP_KEY
const IV = import.meta.env.VITE_APP_IV
const cipherMode = 1 // 1 - C1C3C2，0 - C1C2C3，默认为1

export default {
	sm3Encrypt(msgString) {
		let encryptData = sm3(msgString) // 	
		return encryptData
	},
	sm2Encrypt(msgString) {	
		let encryptData = sm2.doEncrypt(msgString, publicKey, cipherMode) // 加密	
		return '04'+ encryptData
	},
	sm4encrypt(msgString) {
		let encryptData = sm4.encrypt(JSON.stringify(msgString), KEY, {
			mode: 'cbc',
			iv: IV
		}) // 加密
		return encryptData
	},
	sm4decrypt(word) {
		let decryptData = sm4.decrypt(word, KEY, {
			mode: 'cbc',
			iv: IV
		}) // 解密
		return  JSON.parse(decryptData)
	}
}