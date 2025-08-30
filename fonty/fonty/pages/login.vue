<template>
  <div class="min-h-screen bg-[#F8F3EA] flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <!-- 標題 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-[#3A6B60] mb-2">登入 Typersonal</h1>
        <p class="text-gray-600">使用 Google 帳號快速登入</p>
      </div>

      <!-- 登入卡片 -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
        <!-- Google 登入 -->
        <div class="text-center">
          <AuthComponent />
        </div>
      </div>

      <!-- 返回首頁 -->
      <div class="text-center mt-6">
        <NuxtLink 
          to="/" 
          class="text-[#3A6B60] hover:text-[#5EA897] font-medium flex items-center justify-center gap-2"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/>
          </svg>
          返回首頁
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
// 檢查用戶是否已登入，如果是則重導向到 workshop 頁面
const { user } = useAuth()

watch(user, (newUser) => {
  if (newUser) {
    navigateTo('/workshop')
  }
}, { immediate: true })
</script>

<style scoped>
/* 頁面樣式已經在 template 中使用 Tailwind CSS 處理 */
</style>
