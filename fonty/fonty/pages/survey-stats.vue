<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <Navbar />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">📊 問卷調查統計</h1>
        <p class="text-xl text-gray-600">字型產品市場調查結果分析</p>
        
        <!-- Admin Notice -->
        <div v-if="!userState.isAuthenticated" class="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p class="text-yellow-800">⚠️ 請先登入以查看統計數據</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#3A6B60] mx-auto mb-4"></div>
        <p class="text-gray-600">載入統計數據中...</p>
      </div>

      <!-- Statistics -->
      <div v-else-if="userState.isAuthenticated" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <!-- Total Responses -->
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">總回應數</p>
              <p class="text-3xl font-bold text-gray-900">{{ stats.total || 0 }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Very Interested -->
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">很有興趣</p>
              <p class="text-3xl font-bold text-green-600">{{ stats.very_interested || 0 }}</p>
              <p class="text-sm text-gray-500">{{ getPercentage('very_interested') }}%</p>
            </div>
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Maybe Interested -->
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">有點興趣</p>
              <p class="text-3xl font-bold text-yellow-600">{{ stats.maybe_interested || 0 }}</p>
              <p class="text-sm text-gray-500">{{ getPercentage('maybe_interested') }}%</p>
            </div>
            <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Not Interested -->
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">沒興趣</p>
              <p class="text-3xl font-bold text-gray-600">{{ stats.not_interested || 0 }}</p>
              <p class="text-sm text-gray-500">{{ getPercentage('not_interested') }}%</p>
            </div>
            <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Responses -->
      <div v-if="userState.isAuthenticated && recentResponses.length > 0" class="bg-white rounded-2xl shadow-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">最近回應</h3>
        </div>
        <div class="divide-y divide-gray-200">
          <div v-for="response in recentResponses.slice(0, 10)" :key="response.id" class="px-6 py-4 hover:bg-gray-50">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div :class="[
                  'w-3 h-3 rounded-full',
                  response.response === 'very_interested' ? 'bg-green-500' :
                  response.response === 'maybe_interested' ? 'bg-yellow-500' : 'bg-gray-500'
                ]"></div>
                <span class="font-medium text-gray-900">
                  {{ response.userDisplayName || '匿名用戶' }}
                </span>
                <span :class="[
                  'px-2 py-1 text-xs font-medium rounded-full',
                  response.response === 'very_interested' ? 'bg-green-100 text-green-800' :
                  response.response === 'maybe_interested' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                ]">
                  {{ getResponseText(response.response) }}
                </span>
              </div>
              <span class="text-sm text-gray-500">
                {{ formatDate(response.timestamp) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Visual Chart (Simple) -->
      <div v-if="userState.isAuthenticated && stats.total > 0" class="bg-white rounded-2xl shadow-lg p-6 mt-8">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">回應分佈</h3>
        <div class="space-y-4">
          <!-- Very Interested Bar -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <span class="text-sm font-medium text-green-600">很有興趣</span>
              <span class="text-sm text-gray-500">{{ stats.very_interested || 0 }} ({{ getPercentage('very_interested') }}%)</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div class="bg-green-500 h-3 rounded-full" :style="{ width: getPercentage('very_interested') + '%' }"></div>
            </div>
          </div>
          
          <!-- Maybe Interested Bar -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <span class="text-sm font-medium text-yellow-600">有點興趣</span>
              <span class="text-sm text-gray-500">{{ stats.maybe_interested || 0 }} ({{ getPercentage('maybe_interested') }}%)</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div class="bg-yellow-500 h-3 rounded-full" :style="{ width: getPercentage('maybe_interested') + '%' }"></div>
            </div>
          </div>
          
          <!-- Not Interested Bar -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <span class="text-sm font-medium text-gray-600">沒興趣</span>
              <span class="text-sm text-gray-500">{{ stats.not_interested || 0 }} ({{ getPercentage('not_interested') }}%)</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div class="bg-gray-500 h-3 rounded-full" :style="{ width: getPercentage('not_interested') + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Refresh Button -->
      <div v-if="userState.isAuthenticated" class="text-center mt-8">
        <button 
          @click="loadStats"
          :disabled="isLoading"
          class="inline-flex items-center px-6 py-3 bg-[#3A6B60] text-white font-medium rounded-xl hover:bg-[#2d5248] transition-colors duration-200"
        >
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"/>
          </svg>
          重新整理數據
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { collection, query, getDocs, orderBy, limit } from 'firebase/firestore'
import { db } from '~/plugins/firebase.js'
import { userState } from '~/composables/useAuth.js'

const stats = ref({
  total: 0,
  very_interested: 0,
  maybe_interested: 0,
  not_interested: 0
})

const recentResponses = ref([])
const isLoading = ref(false)

const loadStats = async () => {
  if (!userState.isAuthenticated) return

  isLoading.value = true
  
  try {
    // 獲取所有調查回應
    const q = query(collection(db, 'surveys'), orderBy('timestamp', 'desc'), limit(50))
    const querySnapshot = await getDocs(q)
    
    // 重置統計
    const newStats = {
      total: 0,
      very_interested: 0,
      maybe_interested: 0,
      not_interested: 0
    }
    
    const responses = []
    
    querySnapshot.forEach((doc) => {
      const data = doc.data()
      responses.push({
        id: doc.id,
        ...data
      })
      
      // 統計計數
      newStats.total++
      if (data.response === 'very_interested') {
        newStats.very_interested++
      } else if (data.response === 'maybe_interested') {
        newStats.maybe_interested++
      } else if (data.response === 'not_interested') {
        newStats.not_interested++
      }
    })
    
    stats.value = newStats
    recentResponses.value = responses
    
  } catch (error) {
    console.error('載入統計數據失敗:', error)
  } finally {
    isLoading.value = false
  }
}

const getPercentage = (type) => {
  if (stats.value.total === 0) return 0
  return Math.round((stats.value[type] / stats.value.total) * 100)
}

const getResponseText = (response) => {
  switch (response) {
    case 'very_interested': return '很有興趣'
    case 'maybe_interested': return '有點興趣'
    case 'not_interested': return '沒興趣'
    default: return '未知'
  }
}

const formatDate = (timestamp) => {
  if (!timestamp) return ''
  
  try {
    // Firebase Timestamp 轉換
    const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp)
    return date.toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return '時間格式錯誤'
  }
}

onMounted(() => {
  if (userState.isAuthenticated) {
    loadStats()
  }
})

// SEO Meta
useSeoMeta({
  title: 'Typersonal - 問卷統計',
  description: '字型產品市場調查統計結果'
})
</script>
