<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
      <!-- 標題 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">SLM 對話測試</h1>
        <p class="text-gray-600">測試SLM後端的LLM對話功能</p>
      </div>

      <!-- 狀態指示器 -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold text-gray-700">服務狀態</h2>
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-full" :class="slmStatus === 'active' ? 'bg-green-500' : 'bg-red-500'"></div>
            <span class="text-sm" :class="slmStatus === 'active' ? 'text-green-600' : 'text-red-600'">
              {{ slmStatus === 'active' ? 'SLM服務正常' : 'SLM服務離線' }}
            </span>
          </div>
        </div>
      </div>

      <!-- 對話區域 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-700 mb-4">與SLM對話</h3>
        
        <!-- 輸入區域 -->
        <div class="mb-6">
          <div class="flex gap-4 mb-4">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-2">要分析的字元</label>
              <input
                v-model="characters"
                type="text"
                placeholder="輸入要分析的字元，如：ABC、你好、123"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                maxlength="20"
              />
            </div>
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-2">用戶訊息（可選）</label>
              <input
                v-model="userMessage"
                type="text"
                placeholder="輸入你的問題或要求"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <div class="flex gap-3">
            <button
              @click="testSLMConnection"
              :disabled="testing"
              class="px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <svg v-if="testing" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ testing ? '測試中...' : '測試SLM連接' }}
            </button>
            
            <button
              @click="startSLMChat"
              :disabled="chatting || !characters.trim()"
              class="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <svg v-if="chatting" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ chatting ? 'SLM思考中...' : '開始對話' }}
            </button>
          </div>
        </div>

        <!-- 測試結果 -->
        <div v-if="testResult" class="mb-6 p-4 rounded-lg" 
             :class="testResult.startsWith('✅') ? 'bg-green-50 border border-green-200 text-green-700' : 'bg-red-50 border border-red-200 text-red-700'">
          <div class="font-medium mb-2">🔍 連接測試結果：</div>
          <div>{{ testResult }}</div>
        </div>

        <!-- 對話結果 -->
        <div v-if="chatResult" class="p-4 rounded-lg bg-blue-50 border border-blue-200">
          <div class="font-medium mb-2 text-blue-800">🤖 SLM回應：</div>
          <div class="text-blue-700 whitespace-pre-line">{{ chatResult }}</div>
        </div>

        <!-- 歷史對話 -->
        <div v-if="chatHistory.length > 0" class="mt-6">
          <h4 class="text-lg font-semibold text-gray-700 mb-3">對話歷史</h4>
          <div class="space-y-3">
            <div v-for="(chat, index) in chatHistory" :key="index" class="p-4 bg-gray-50 rounded-lg">
              <div class="flex items-start gap-3">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-blue-600 font-medium text-sm">U</span>
                </div>
                <div class="flex-1">
                  <div class="text-sm text-gray-600 mb-1">
                    <strong>字元:</strong> {{ chat.characters }} | 
                    <strong>訊息:</strong> {{ chat.userMessage || '無' }}
                  </div>
                  <div class="text-sm text-gray-800">{{ chat.response }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 響應式變量
const characters = ref('ABC')
const userMessage = ref('請分析這些字元的特徵')
const testing = ref(false)
const chatting = ref(false)
const testResult = ref('')
const chatResult = ref('')
const slmStatus = ref('checking')
const chatHistory = ref([])

// 測試SLM連接
async function testSLMConnection() {
  try {
    testing.value = true
    testResult.value = '正在測試SLM連接...'
    
    const formData = new FormData()
    formData.append('characters', characters.value || 'ABC')
    formData.append('message', '測試SLM功能')
    
    const response = await fetch('http://localhost:8001/test-simple', {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      const result = await response.json()
      testResult.value = `✅ SLM測試成功！接收字元: ${result.received_characters}, 狀態: ${result.status}`
      slmStatus.value = 'active'
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('❌ SLM測試錯誤:', error)
    testResult.value = `❌ SLM測試錯誤: ${error.message}`
    slmStatus.value = 'inactive'
  } finally {
    testing.value = false
  }
}

// 開始SLM對話
async function startSLMChat() {
  try {
    chatting.value = true
    chatResult.value = ''
    
    const formData = new FormData()
    formData.append('characters', characters.value || 'ABC')
    formData.append('user_message', userMessage.value || '請分析這些字元的特徵')
    formData.append('context', '字型生成分析')
    
    const response = await fetch('http://localhost:8001/slm-chat', {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      const result = await response.json()
      chatResult.value = result.slm_response
      
      // 添加到對話歷史
      chatHistory.value.unshift({
        characters: characters.value,
        userMessage: userMessage.value,
        response: result.slm_response,
        timestamp: new Date().toLocaleTimeString()
      })
      
      console.log('🎉 SLM對話成功:', result)
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('❌ SLM對話錯誤:', error)
    chatResult.value = `❌ SLM對話錯誤: ${error.message}`
  } finally {
    chatting.value = false
  }
}

// 頁面載入時檢查服務狀態
onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8001/')
    if (response.ok) {
      slmStatus.value = 'active'
    }
  } catch (error) {
    slmStatus.value = 'inactive'
  }
})
</script>

<style scoped>
/* 自定義樣式 */
</style>
