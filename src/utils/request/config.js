// 配置文件
export const getBaseUrl = () => {
  return import.meta.env.VITE_APP_BASE_URL || '';
};

export const getIsEncrypt = () => {
  // 是否加密
  return true;

};

// 不需要加密的接口列表
export const getNoEncryptUrls = () => {
  return [
    // 暂时注释掉，让所有接口都不加密

    // 'register',
    // 'sendMsg',
    // 'sendEmail'
    // 'login',
    // 'register',
    // 'sendMsg',
    // 'sendEmail'
    'common/uploadImg' // 上传接口不需要加密
  ];
};

// 不需要解密的接口列表
export const getNoDecryptUrls = () => {
  return [
    // 暂时注释掉，让所有接口都不解密
    // 'login',
    // 'register',
    // 'sendMsg',
    // 'sendEmail'
  ];
}; 