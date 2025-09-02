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
    let defaultLang = navigator.language;  // 获取浏览器语言
    if (defaultLang) {
      // 浏览器可能是en en-us之类的，需要转换为支持的语言
      defaultLang = defaultLang.toLowerCase();  // 将浏览器语言转换为小写

      // 语言映射转换 - 使用映射表进行精确匹配
      if (LANGUAGE_MAPPING[defaultLang]) {
        defaultLang = LANGUAGE_MAPPING[defaultLang];
      } else {
        // 如果没有精确匹配，尝试前缀匹配
        const prefixMatch = Object.keys(LANGUAGE_MAPPING).find(key =>
          defaultLang.startsWith(key.split('-')[0])
        );
        if (prefixMatch) {
          defaultLang = LANGUAGE_MAPPING[prefixMatch];
        }
      }
      // 如果没有匹配到，则使用默认语言
      if (!SUPPORTED_LANGUAGES.includes(defaultLang)) {
        defaultLang = import.meta.env.VITE_DEFAULT_LANG;; // 默认使用配置文件中的默认语言
      }

      localLang = defaultLang;
    }
    setLocal("language", defaultLang);  // 设置本地语言
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
