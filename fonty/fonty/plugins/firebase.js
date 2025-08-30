import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

// Firebase 配置 - 直接寫在代碼中以便快速協作
const firebaseConfig = {
  apiKey: "AIzaSyCcGXPMnpE9sq1zWLPaayafpqBlY_66qvM",
  authDomain: "fonty-a1ffc.firebaseapp.com",
  projectId: "fonty-a1ffc",
  storageBucket: "fonty-a1ffc.firebasestorage.app",
  messagingSenderId: "467528652769",
  appId: "1:467528652769:web:a7c6e4ff1f62565650a4a0",
  measurementId: "G-71Y4MEMCNC"
}

// 初始化 Firebase
const app = initializeApp(firebaseConfig)

// 初始化 Authentication
const auth = getAuth(app)

// 初始化 Firestore
const db = getFirestore(app)

// Google 登入提供者
const googleProvider = new GoogleAuthProvider()
googleProvider.addScope('email')
googleProvider.addScope('profile')
// 確保登出時清除所有狀態
googleProvider.setCustomParameters({
  prompt: 'select_account'
})

export { auth, googleProvider, db }

// Nuxt plugin 預設 export
export default defineNuxtPlugin(() => {
  // Firebase 在客戶端初始化
})
