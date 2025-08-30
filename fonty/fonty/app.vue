<template>
  <div class="bg-[#F8F3EA] min-h-screen">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup>
// 設置應用程式級別的元數據
useHead({
  htmlAttrs: {
    lang: 'zh-TW'
  },
  titleTemplate: '%s - Typersonal',
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ]
})
</script>