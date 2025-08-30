<template>
  <!-- Login State -->
  <div v-if="!userState.user && !userState.isLoading" class="auth-container">
    <!-- Loading State for Login -->
    <div v-if="isLoggingIn" class="loading-state">
      <div class="loading-spinner"></div>
      <p class="loading-text">連接中...</p>
    </div>
    
    <!-- Google Login Button -->
    <button 
      v-else
      @click="handleGoogleLogin"
      class="google-login-btn"
      :disabled="isLoggingIn"
    >
      <div class="btn-content">
        <svg class="google-icon" viewBox="0 0 24 24">
          <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
          <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
          <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
          <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
        </svg>
        <span class="btn-text">
          {{ isLoggingIn ? '登入中...' : 'Google 登入' }}
        </span>
      </div>
    </button>
  </div>

  <!-- User Profile (Logged In State) -->
  <div v-else-if="userState.user" class="user-profile">
    <div class="user-avatar">
      <img 
        :src="userState.user.photoURL || '/default-avatar.svg'" 
        :alt="userState.user.displayName || '使用者'"
        class="avatar-img"
        @error="handleImageError"
      >
    </div>
    
    <div class="user-info">
      <p class="user-name">
        {{ userState.user.displayName || '用戶' }}
      </p>
      <p class="user-email">
        {{ userState.user.email }}
      </p>
    </div>

    <button 
      @click="handleLogout"
      class="logout-btn"
      :disabled="isLoggingOut"
    >
      <svg class="logout-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
      </svg>
      {{ isLoggingOut ? '登出中...' : '登出' }}
    </button>
  </div>

  <!-- General Loading State -->
  <div v-else class="loading-state">
    <div class="loading-spinner"></div>
    <p class="loading-text">載入中...</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { userState } from '~/composables/useAuth.js'

const isLoggingIn = ref(false)
const isLoggingOut = ref(false)

const handleGoogleLogin = async () => {
  isLoggingIn.value = true
  try {
    const { signIn } = await import('~/composables/useAuth.js')
    await signIn()
  } catch (error) {
    console.error('登入失敗:', error);
    console.error('登入失敗，請稍後再試');
  } finally {
    isLoggingIn.value = false
  }
}

const handleLogout = async () => {
  isLoggingOut.value = true
  try {
    console.log('嘗試登出...')
    // 直接調用 userState 的方法來避免導入問題
    await userState.signOutUser()
    console.log('登出完成')
  } catch (error) {
    console.error('登出錯誤:', error)
    console.error('登出失敗，請稍後再試')
  } finally {
    isLoggingOut.value = false
  }
}

const handleImageError = (event) => {
  event.target.src = '/default-avatar.svg'
}
</script>

<style scoped>
.auth-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 50px;
}

/* Google Login Button */
.google-login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  background: white;
  border: 1px solid #dadce0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  font-size: 16px;
  font-weight: 500;
  min-width: 180px;
}

.google-login-btn:hover:not(:disabled) {
  background: #f8f9fa;
  border-color: #dadce0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.google-login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.google-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.btn-text {
  color: #3c4043;
  white-space: nowrap;
}

/* User Profile */
.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: rgba(248, 243, 234, 0.8);
  border: 1px solid #E29930;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  min-height: 50px;
}

.user-avatar {
  flex-shrink: 0;
}

.avatar-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid #E29930;
  object-fit: cover;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 14px;
  margin: 0 0 2px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: transparent;
  border: 1px solid #E29930;
  border-radius: 6px;
  color: #E29930;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
  font-weight: 500;
  flex-shrink: 0;
}

.logout-btn:hover:not(:disabled) {
  background: #E29930;
  color: white;
}

.logout-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.logout-icon {
  width: 14px;
  height: 14px;
}

/* Loading State */
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px 24px;
  background: rgba(248, 243, 234, 0.5);
  border: 1px solid #E29930;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  min-height: 50px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #E2993020;
  border-top: 2px solid #E29930;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #E29930;
  font-size: 14px;
  font-weight: 500;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .user-profile {
    padding: 6px 12px;
    gap: 8px;
  }
  
  .avatar-img {
    width: 32px;
    height: 32px;
  }
  
  .user-name {
    font-size: 13px;
  }
  
  .user-email {
    font-size: 11px;
  }
  
  .logout-btn {
    padding: 4px 8px;
    font-size: 11px;
  }
  
  .logout-icon {
    width: 12px;
    height: 12px;
  }
  
  .google-login-btn {
    min-width: 150px;
    padding: 10px 20px;
    font-size: 14px;
  }
}

/* Accessibility improvements */
.google-login-btn:focus,
.logout-btn:focus {
  outline: 2px solid #E29930;
  outline-offset: 2px;
}

/* Dark mode support (future enhancement) */
@media (prefers-color-scheme: dark) {
  .google-login-btn,
  .user-profile,
  .loading-state {
    background: rgba(0, 0, 0, 0.8);
    border-color: rgba(255, 255, 255, 0.2);
  }
  
  .user-info p:first-child {
    color: #F8F3EA;
  }
}
</style>
