// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  css: ['@/assets/css/main.css', '@/assets/css/fonts.css'],
  modules: ['@nuxtjs/tailwindcss'],
  
  // 运行时配置 - API地址
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 
        (process.env.NODE_ENV === 'production' 
          ? 'https://typersonal.dy6.click/8000' 
          : 'http://localhost:8000')
    }
  },
  
  // PWA 和移動端優化
  app: {
    head: {
      viewport: 'width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes',
      charset: 'utf-8',
      meta: [
        { name: 'mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'default' },
        { name: 'apple-mobile-web-app-title', content: 'Typersonal' },
        { name: 'application-name', content: 'Typersonal' },
        { name: 'msapplication-TileColor', content: '#E29930' },
        { name: 'theme-color', content: '#E29930' },
        { name: 'format-detection', content: 'telephone=no' }
      ],
      link: [
        { rel: 'manifest', href: '/manifest.json' },
        { rel: 'apple-touch-icon', href: '/typersonal3.png' },
        // Google Fonts for basic Chinese fonts
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@100;200;300;400;500;600;700;800;900&family=Noto+Serif+TC:wght@200;300;400;500;600;700;800;900&display=swap' }
      ]
    }
  },

  // 移動端優化的渲染選項
  nitro: {
    compressPublicAssets: true,
    minify: true
  },

  // 性能優化
  experimental: {
    payloadExtraction: false
  },
  
  // 組件自動導入
  components: {
    global: true,
    dirs: ['~/components']
  }
})
