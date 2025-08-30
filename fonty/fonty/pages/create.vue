<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20 flex items-center justify-center">
    <div class="text-center">
      <div class="animate-spin w-16 h-16 border-4 border-[#5EA897] border-t-transparent rounded-full mx-auto mb-4"></div>
      <p class="text-slate-600">正在跳轉到 Workshop 頁面...</p>
    </div>
  </div>
</template>

<script setup>
// 自動重定向到 workshop 頁面
onMounted(() => {
  navigateTo('/workshop')
})
</script>
