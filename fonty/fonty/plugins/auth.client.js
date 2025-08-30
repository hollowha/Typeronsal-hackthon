import { userState } from '~/composables/useAuth.js'

export default defineNuxtPlugin(() => {
  // 在客戶端初始化 Firebase Auth 監聽器
  if (process.client) {
    userState.initAuthListener()
  }
})
