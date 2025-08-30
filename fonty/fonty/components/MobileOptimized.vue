<template>
  <div class="mobile-optimized-container">
    <!-- Mobile-First Navigation Bar -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-lg border-b border-gray-200/50 safe-area-top">
      <div class="px-4 py-3">
        <div class="flex items-center justify-between">
          <!-- Logo - Optimized for mobile -->
          <NuxtLink to="/" class="flex items-center space-x-2">
            <img src="/typersonal3.png" alt="Typersonal" class="w-8 h-8 object-contain">
            <span class="text-lg font-bold text-brand-orange">Typersonal</span>
          </NuxtLink>
          
          <!-- Mobile Menu Button -->
          <button @click="toggleMobileMenu" class="p-2 rounded-lg hover:bg-gray-100 touch-manipulation">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
        </div>
      </div>
    </nav>

    <!-- Mobile Menu Overlay -->
    <div v-if="showMobileMenu" class="fixed inset-0 z-40 bg-black/50" @click="closeMobileMenu">
      <div class="fixed right-0 top-0 h-full w-80 bg-white shadow-xl">
        <div class="p-6">
          <div class="flex justify-between items-center mb-8">
            <h3 class="text-xl font-bold">選單</h3>
            <button @click="closeMobileMenu" class="p-2 rounded-lg hover:bg-gray-100">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          
          <nav class="space-y-4">
            <NuxtLink v-for="link in mobileNavLinks" :key="link.path" 
                      :to="link.path" 
                      @click="closeMobileMenu"
                      class="block py-3 px-4 rounded-lg hover:bg-gray-50 text-lg font-medium text-gray-700">
              {{ link.name }}
            </NuxtLink>
          </nav>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="pt-16">
      <slot />
    </main>

    <!-- Mobile-First Footer -->
    <footer class="bg-gray-900 text-white py-12">
      <div class="px-4">
        <div class="text-center mb-8">
          <img src="/typersonal3.png" alt="Typersonal" class="w-12 h-12 mx-auto mb-4 object-contain">
          <h3 class="text-xl font-bold mb-2">Typersonal</h3>
          <p class="text-gray-400">AI 驅動的字型生成平台</p>
        </div>
        
        <div class="grid grid-cols-2 gap-8 mb-8">
          <div>
            <h4 class="font-semibold mb-4">產品</h4>
            <nav class="space-y-2 text-sm">
              <a href="/workshop" class="block text-gray-300 hover:text-white">字型創作</a>
              <a href="/market" class="block text-gray-300 hover:text-white">字型市集</a>
              <a href="/workshop" class="block text-gray-300 hover:text-white">上傳字型</a>
            </nav>
          </div>
          
          <div>
            <h4 class="font-semibold mb-4">支援</h4>
            <nav class="space-y-2 text-sm">
              <a href="#" class="block text-gray-300 hover:text-white">使用教學</a>
              <a href="#" class="block text-gray-300 hover:text-white">常見問題</a>
              <a href="#" class="block text-gray-300 hover:text-white">聯絡我們</a>
            </nav>
          </div>
        </div>
        
        <div class="text-center text-sm text-gray-400 border-t border-gray-800 pt-6">
          © 2025 Typersonal. 保留所有權利。
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showMobileMenu = ref(false)

const mobileNavLinks = [
  { name: '首頁', path: '/' },
  { name: '字型創作', path: '/workshop' },
  { name: '字型市集', path: '/market' },
  { name: '上傳字型', path: '/workshop' },
  { name: '登入', path: '/login' }
]

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
  // 防止背景滾動
  if (showMobileMenu.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
  document.body.style.overflow = ''
}

// 清理
onUnmounted(() => {
  document.body.style.overflow = ''
})
</script>

<style scoped>
.safe-area-top {
  padding-top: env(safe-area-inset-top);
}

/* iOS Safari 特定優化 */
@supports (-webkit-touch-callout: none) {
  .mobile-optimized-container {
    -webkit-overflow-scrolling: touch;
  }
}

/* 觸控目標最小尺寸 */
button, a {
  min-height: 44px;
  min-width: 44px;
}
</style>
