export default defineNuxtRouteMiddleware((to, from) => {
  if (process.client) {
    const { user, isLoading } = useAuth()
    
    // 等待認證狀態載入完成
    if (isLoading.value) {
      return
    }
    
    // 如果用戶未登入，重導向到登入頁面
    if (!user.value) {
      return navigateTo('/login')
    }
  }
})
