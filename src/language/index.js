import { createI18n } from "vue-i18n";


import { getLocal, setLocal } from '@/utils/localStorage.js'

// 动态导入所有语言文件
const languageModules = import.meta.glob("./messages/*.json", { eager: true });

// 构建messages对象
const messages = {};
Object.keys(languageModules).forEach((path) => {
  const fileName = path.split("/").pop()?.replace(".json", "");
  if (fileName) {
    messages[fileName] = languageModules[path].default || languageModules[path];
  }
});

// 语言映射配置
const LANGUAGE_MAPPING = {
  // 英文变体映射到 en-us
  'en': 'en-us',
  'en-us': 'en-us',
  'en-gb': 'en-us',
  'en-au': 'en-us',
  'en-ca': 'en-us',
  'en-nz': 'en-us',
  'en-ie': 'en-us',
  'en-za': 'en-us',
  'en-jm': 'en-us',
  'en-bz': 'en-us',
  'en-tt': 'en-us',
  'en-zw': 'en-us',
  'en-ph': 'en-us',
  'en-in': 'en-us',
  'en-my': 'en-us',
  'en-sg': 'en-us',

  // 中文变体映射到 zh-cn
  'zh': 'zh-cn',
  'zh-cn': 'zh-cn',
  'zh-tw': 'zh-cn',
  'zh-hk': 'zh-cn',
  'zh-mo': 'zh-cn',
  'zh-sg': 'zh-cn',
  'zh-my': 'zh-cn',
};

// 支持的语言列表
const SUPPORTED_LANGUAGES = ['en-us', 'zh-cn'];

function getLocalLang() {
  let localLang = getLocal("language");

  if (!localLang) {
    // 默认使用中文
    let defaultLang = 'zh-cn';
    
    // 可以考虑浏览器语言，但优先使用中文
    const browserLang = navigator.language;
    if (browserLang) {
      const normalizedLang = browserLang.toLowerCase();
      
      // 语言映射转换
      if (LANGUAGE_MAPPING[normalizedLang]) {
        defaultLang = LANGUAGE_MAPPING[normalizedLang];
      } else {
        // 如果没有精确匹配，尝试前缀匹配
        const prefixMatch = Object.keys(LANGUAGE_MAPPING).find(key =>
          normalizedLang.startsWith(key.split('-')[0])
        );
        if (prefixMatch) {
          defaultLang = LANGUAGE_MAPPING[prefixMatch];
        }
      }
    }
    
    // 确保是支持的语言，否则使用中文
    if (!SUPPORTED_LANGUAGES.includes(defaultLang)) {
      defaultLang = 'zh-cn';
    }

    localLang = defaultLang;
    setLocal("language", defaultLang);  // 保存到本地存储
  }
  return localLang;
}

const i18n = createI18n({
  allowComposition: true,
  globalInjection: true,
  legacy: false,
  locale: getLocalLang(),
  messages
});

export default i18n;
export const t = (key) => {
  return i18n.global.t(key);
};
