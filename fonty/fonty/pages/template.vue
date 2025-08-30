<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
    <!-- 導航欄 -->
    <Navbar />
    
    <!-- 頁面標題區域 -->
    <div class="relative overflow-hidden bg-white/80 backdrop-blur-xl border-b border-white/20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
        <div class="text-center">
          <!-- 主圖標 -->
          <div class="w-16 h-16 md:w-20 md:h-20 bg-gradient-to-br from-[#5EA897] to-[#3A6B60] rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-xl">
            <svg class="w-8 h-8 md:w-10 md:h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          
          <!-- 標題 -->
          <h1 class="text-2xl md:text-4xl font-bold text-slate-800 mb-2">
            個人化
            <span class="bg-gradient-to-r from-[#5EA897] to-[#3A6B60] bg-clip-text text-transparent">模板創作</span>
          </h1>
          
          <!-- 副標題 -->
          <p class="text-slate-600 text-sm md:text-base max-w-2xl mx-auto">
            選擇精美模板，應用您的專屬字型，創作獨一無二的個人化作品
          </p>
          
          <!-- 進度指示器 -->
          <div class="flex items-center justify-center gap-2 mt-4">
            <div class="w-8 h-1 bg-gradient-to-r from-[#5EA897] to-gray-200 rounded-full"></div>
            <div class="w-8 h-1 bg-gradient-to-r from-[#5EA897] to-gray-200 rounded-full"></div>
            <div class="w-8 h-1 bg-gradient-to-r from-[#5EA897] to-gray-200 rounded-full"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要內容區域 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 md:py-8">
      <div class="grid grid-cols-1 xl:grid-cols-12 gap-4 md:gap-8">
        
        <!-- 左側控制面板 -->
        <div class="xl:col-span-5 space-y-4 md:space-y-6">
          
          <!-- 模板選擇區域 -->
          <div class="bg-white/80 backdrop-blur-xl rounded-2xl md:rounded-3xl shadow-xl border border-white/20 p-4 md:p-6">
            <div class="flex items-center gap-3 mb-4 md:mb-6">
              <div class="w-8 h-8 md:w-10 md:h-10 bg-gradient-to-br from-[#5EA897] to-[#3A6B60] rounded-lg md:rounded-xl flex items-center justify-center">
                <svg class="w-4 h-4 md:w-5 md:h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"/>
                </svg>
              </div>
              <h2 class="text-lg md:text-xl font-bold text-slate-800">選擇模板</h2>
            </div>
            
            <!-- 模板網格 -->
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 md:gap-4">
              <div
                v-for="template in templates"
                :key="template.id"
                @click="selectTemplate(template.id)"
                class="relative group cursor-pointer"
              >
                <div class="relative overflow-hidden rounded-xl md:rounded-2xl border-2 transition-all duration-300"
                     :class="currentTemplateId === template.id 
                       ? 'border-[#5EA897] shadow-lg shadow-[#5EA897]/20' 
                       : 'border-gray-200 hover:border-[#5EA897]/50'">
                  
                  <!-- 模板縮圖 -->
                  <img 
                    :src="template.thumbnail" 
                    :alt="template.name"
                    class="w-full h-20 sm:h-24 md:h-28 object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                  
                  <!-- 選擇指示器 -->
                  <div v-if="currentTemplateId === template.id"
                       class="absolute inset-0 bg-gradient-to-r from-[#5EA897]/20 to-[#3A6B60]/20 flex items-center justify-center">
                    <div class="w-6 h-6 md:w-8 md:h-8 bg-[#5EA897] rounded-full flex items-center justify-center">
                      <svg class="w-3 h-3 md:w-5 md:h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                      </svg>
                    </div>
                  </div>
                  
                  <!-- 模板名稱 -->
                  <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-2">
                    <p class="text-white text-xs font-medium truncate">{{ template.name }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 字型選擇區域 -->
          <div class="bg-white/80 backdrop-blur-xl rounded-2xl md:rounded-3xl shadow-xl border border-white/20 p-4 md:p-6">
            <div class="flex items-center gap-3 mb-4 md:mb-6">
              <div class="w-8 h-8 md:w-10 md:h-10 bg-gradient-to-br from-[#E29930] to-[#D48826] rounded-lg md:rounded-xl flex items-center justify-center">
                <svg class="w-4 h-4 md:w-5 md:h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"/>
                </svg>
              </div>
              <h2 class="text-lg md:text-xl font-bold text-slate-800">字型風格</h2>
            </div>

            <!-- 從 workshop 過來的字型 -->
            <div v-if="workshopFontData" class="mb-4 md:mb-6">
              <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-3 md:p-4 border border-blue-200">
                <h4 class="font-semibold text-blue-800 mb-3 flex items-center gap-2 text-sm md:text-base">
                  <svg class="w-4 h-4 md:w-5 md:h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                  </svg>
                  已設計的字型風格
                </h4>
                
                <!-- 字型圖片預覽 -->
                <div class="relative mb-3 md:mb-4">
                  <img 
                    :src="workshopFontData.blendedImage || workshopFontData.referenceImage" 
                    alt="Workshop字型"
                    class="w-full h-24 md:h-32 object-cover rounded-lg border border-blue-200"
                  />
                  <div class="absolute top-2 right-2 bg-blue-500 text-white text-xs px-2 py-1 rounded-full">
                    Workshop
                  </div>
                </div>
                
                <!-- 字型信息 -->
                <div class="space-y-1 md:space-y-2 text-xs md:text-sm mb-3 md:mb-4">
                  <div class="flex items-center gap-2">
                    <span class="text-blue-600">融合圖片:</span>
                    <span :class="workshopFontData.blendedImage ? 'text-green-600' : 'text-red-600'">
                      {{ workshopFontData.blendedImage ? '✓' : '✗' }}
                    </span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-blue-600">參考圖片:</span>
                    <span :class="workshopFontData.referenceImage ? 'text-green-600' : 'text-red-600'">
                      {{ workshopFontData.referenceImage ? '✓' : '✗' }}
                    </span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-blue-600">風格選項:</span>
                    <span class="text-slate-700">{{ workshopFontData.styleOption || 'N/A' }}</span>
                  </div>
                </div>
              </div>
            </div>



            <!-- 字型選擇按鈕 -->
            <div class="grid grid-cols-1 gap-3 md:gap-4">
              <!-- 重新微調字型 -->
              <button
                @click="goToWorkshop"
                class="flex items-center gap-3 md:gap-4 p-3 md:p-4 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl border border-blue-200 hover:from-blue-100 hover:to-indigo-200 transition-all duration-200 group shadow-sm hover:shadow-md"
              >
                <div class="w-10 h-10 md:w-12 md:h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg md:rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                  <svg class="w-5 h-5 md:w-6 md:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                  </svg>
                </div>
                <div class="text-left flex-1">
                  <h4 class="font-semibold text-blue-800 mb-0.5 md:mb-1 text-sm md:text-base">重新微調字型</h4>
                  <p class="text-xs md:text-sm text-blue-600">回到 workshop 頁面重新設計您的個人化字型</p>
                </div>
                <svg class="w-4 h-4 md:w-5 md:h-5 text-blue-400 group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </button>

              <!-- 使用現成字型 -->
              <button
                @click="useExistingFonts"
                class="flex items-center gap-3 md:gap-4 p-3 md:p-4 bg-gradient-to-br from-green-50 to-emerald-100 rounded-xl border border-green-200 hover:from-green-100 hover:to-emerald-200 transition-all duration-200 group shadow-sm hover:shadow-md"
              >
                <div class="w-10 h-10 md:w-12 md:h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg md:rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                  <svg class="w-5 h-5 md:w-6 md:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
                  </svg>
                </div>
                <div class="text-left flex-1">
                  <h4 class="font-semibold text-green-800 mb-0.5 md:mb-1 text-sm md:text-base">使用現成字型</h4>
                  <p class="text-xs md:text-sm text-green-600">從預設的手寫字型中選擇，快速開始設計</p>
                </div>
                <svg class="w-4 h-4 md:w-5 md:h-5 text-green-400 group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- 手寫風格生成區域 -->
          <div v-if="showFontGeneration" class="bg-white/80 backdrop-blur-xl rounded-2xl md:rounded-3xl shadow-xl border border-white/20 p-4 md:p-6">
            <div class="flex items-center gap-3 mb-4 md:mb-6">
              <div class="w-8 h-8 md:w-10 md:h-10 bg-gradient-to-br from-[#E29930] to-[#D48826] rounded-lg md:rounded-xl flex items-center justify-center">
                <svg class="w-4 h-4 md:w-5 md:h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" clip-rule="evenodd"/>
                </svg>
              </div>
              <h2 class="text-lg md:text-xl font-bold text-slate-800">生成字型到模板</h2>
            </div>
            
            <!-- 生成狀態 -->
            <div class="mb-4 md:mb-6">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs md:text-sm font-medium text-slate-700">生成進度</span>
                <span class="text-xs md:text-sm text-slate-500">{{ doneCount }}/{{ charsToGenerateCount }}</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-gradient-to-r from-[#E29930] to-[#D48826] h-2 rounded-full transition-all duration-300"
                     :style="{ width: charsToGenerateCount > 0 ? (doneCount / charsToGenerateCount) * 100 + '%' : '0%' }"></div>
              </div>
            </div>
            
            <!-- 生成按鈕 -->
            <button
              @click="batchGenerateFonts"
              :disabled="batching || !canGenerateFonts"
              class="w-full px-3 md:px-4 py-2.5 md:py-3 rounded-lg md:rounded-xl font-medium transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed text-sm md:text-base"
              :class="batching || !canGenerateFonts
                ? 'bg-gradient-to-r from-[#E29930] to-[#D48826] text-white hover:shadow-xl hover:scale-[1.02] active:scale-98'
                : 'bg-gradient-to-r from-[#5EA897] to-[#3A6B60] text-white hover:shadow-xl hover:scale-[1.02] active:scale-98'"
            >
              <svg v-if="batching" class="animate-spin w-4 h-4 md:w-5 md:h-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-4 h-4 md:w-5 md:h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
              </svg>
              {{ batching ? '正在生成...' : '生成手寫字體' }}
            </button>
            
            <!-- 錯誤訊息 -->
            <div v-if="errorMsg" class="mt-3 md:mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-red-700 text-xs md:text-sm">{{ errorMsg }}</p>
            </div>
          </div>

          <!-- Smart Text Generation Area -->
          <div class="bg-white/80 backdrop-blur-xl rounded-2xl md:rounded-3xl shadow-xl border border-white/20 p-4 md:p-6">
            <div class="flex items-center gap-3 mb-4 md:mb-6">
              <div class="w-8 h-8 md:w-10 md:h-10 bg-gradient-to-br from-[#8B5CF6] to-[#7C3AED] rounded-lg md:rounded-xl flex items-center justify-center">
                <svg class="w-4 h-4 md:w-5 md:w-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="flex-1">
                <h2 class="text-lg md:text-xl font-bold text-slate-800">Smart Text Generation</h2>

              </div>

            </div>
            

            
            <!-- Generation Area -->
            <div class="space-y-4">
              <!-- 輸入區域 -->
              <div class="flex gap-4 mb-4">
                <div class="flex-1">
                  <label class="block text-sm font-medium text-slate-700 mb-2">Topic</label>
                  <input
                    v-model="slmCharacters"
                    type="text"
                    placeholder="Enter topic, e.g.: Technology, Life, Creativity"
                    class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    maxlength="20"
                  />
                </div>
                <div class="flex-1">
                  <label class="block text-sm font-medium text-slate-700 mb-2">My Ideas</label>
                  <input
                    v-model="userMessage"
                    type="text"
                    placeholder="Enter your ideas or requirements"
                    class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
              
              <div class="flex justify-center">
                <button
                  @click="startSLMChat"
                  :disabled="chatting || !slmCharacters.trim()"
                  class="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  <svg v-if="chatting" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ chatting ? 'AI Thinking...' : 'Generate Text' }}
                </button>
              </div>
              
              <!-- Test Result -->
              <div v-if="testResult" class="p-4 rounded-lg" 
                   :class="testResult.startsWith('✅') ? 'bg-green-50 border border-green-200 text-green-700' : 'bg-red-50 border border-red-200 text-red-700'">
                <div class="font-medium mb-2">🔍 Test Result:</div>
                <div>{{ testResult }}</div>
              </div>
              
              <!-- Generation Result -->
              <div v-if="chatResult" class="p-4 rounded-lg bg-blue-50 border border-blue-200">
                <div class="font-medium mb-2 text-blue-800">Smart Text Generation:</div>
                <div class="text-blue-700 whitespace-pre-line">{{ chatResult }}</div>
              </div>
              
              <!-- Generation History -->
              <div v-if="chatHistory.length > 0" class="mt-6">
                <h4 class="text-lg font-semibold text-slate-700 mb-3">Generation History</h4>
                <div class="space-y-3">
                  <div v-for="(chat, index) in chatHistory" :key="index" class="p-4 bg-gray-50 rounded-lg">
                    <div class="flex items-start gap-3">
                      <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span class="text-blue-600 font-medium text-sm">U</span>
                      </div>
                      <div class="flex-1">
                        <div class="text-sm text-gray-600 mb-1">
                          <strong>Topic:</strong> {{ chat.characters }} | 
                          <strong>Ideas:</strong> {{ chat.userMessage || 'None' }}
                        </div>
                        <div class="text-sm text-slate-800">{{ chat.response }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Ready to Generate Prompt -->
              <div v-if="slmCharacters.trim() && !chatting && !chatResult && chatHistory.length === 0" class="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                <p class="text-amber-700 text-xs text-center">
                  <svg class="w-4 h-4 inline mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                  </svg>
                  Topic "{{ slmCharacters.trim() }}" entered, click Generate Text button
                </p>
              </div>
              
              <!-- Generation Status Prompt -->
              <div v-if="chatting" class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p class="text-blue-700 text-xs text-center">
                  <svg class="w-4 h-4 inline mr-1 animate-spin" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/>
                  </svg>
                  AI is thinking, please wait...
                </p>
              </div>
              
              <!-- Generation Complete Prompt -->
              <div v-if="chatResult && !chatting" class="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                <p class="text-green-700 text-xs text-center">
                  <svg class="w-4 h-4 inline mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  Text generation completed!
                </p>
              </div>
              


              

            </div>
          </div>
        </div>

        <!-- 右側預覽區域 -->
        <div class="xl:col-span-7 space-y-4 md:space-y-6">
          <!-- 即時預覽 -->
          <div class="bg-white/80 backdrop-blur-xl rounded-2xl md:rounded-3xl shadow-xl border border-white/20 p-4 md:p-6">
            <div class="flex items-center justify-between mb-4 md:mb-6">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 md:w-10 md:h-10 bg-gradient-to-br from-[#E29930] to-[#D48826] rounded-lg md:rounded-xl flex items-center justify-center">
                  <svg class="w-4 h-4 md:w-5 md:h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <h2 class="text-lg md:text-xl font-bold text-slate-800">即時預覽</h2>
              </div>
              
              <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 md:w-2 md:h-2 rounded-full" :class="hasGeneratedFonts ? 'bg-green-500 animate-pulse' : 'bg-amber-400'"></div>
                <span class="text-xs font-medium" :class="hasGeneratedFonts ? 'text-green-600' : 'text-amber-600'">
                  {{ hasGeneratedFonts ? '字型已生成' : '等待生成' }}
                </span>
              </div>
            </div>
            
            <!-- 預覽內容 -->
            <div id="template-preview-container" class="relative bg-white rounded-xl md:rounded-2xl overflow-hidden shadow-lg border border-gray-200 mb-4 md:mb-6">
              <!-- 背景圖片 -->
              <img 
                v-if="currentTemplate"
                :src="currentTemplate.background" 
                :alt="currentTemplate.name"
                class="w-full h-auto block"
                @load="onBgLoad"
                @error="onBgError"
                ref="bgEl"
                crossorigin="anonymous"
                style="display: block;"
              />
              
              <!-- 文字內容 -->
              <div v-if="currentTemplate && currentSlots.length" 
                   class="absolute inset-0"
                   ref="canvasWrap">
                <div
                  v-for="slot in currentSlots"
                  :key="slot.key"
                  v-show="slotSelected[slot.key]"
                  class="absolute"
                  :style="{
                    left: getSlotPosition(slot, 'x') + 'px',
                    top: getSlotPosition(slot, 'y') + 'px',
                    width: getSlotPosition(slot, 'w') + 'px',
                    height: getSlotPosition(slot, 'h') + 'px',
                    pointerEvents: 'none'
                  }"
                >
                  <!-- 如果有生成字體，按字元顯示 -->
                  <div v-if="hasGeneratedFonts && slotInputs[slot.key]" 
                       class="w-full h-full flex flex-wrap items-start justify-start"
                       :class="slot.align === 'center' ? 'justify-center' : slot.align === 'right' ? 'justify-end' : 'justify-start'">
                    
                    <!-- 按行分割並顯示文字 -->
                    <div v-for="(line, lineIndex) in (slotInputs[slot.key] || '').split('\n')" 
                         :key="'line-' + lineIndex"
                         class="w-full flex items-center"
                         :class="slot.align === 'center' ? 'justify-center' : slot.align === 'right' ? 'justify-end' : 'justify-start'"
                         :style="{ 
                           minHeight: (slot.fontSize || 20) + 'px',
                           lineHeight: (slot.lineHeight || 1.4),
                           marginBottom: lineIndex < (slotInputs[slot.key] || '').split('\n').length - 1 ? '8px' : '0'
                         }">
                      
                      <!-- 按字元分割並顯示 -->
                      <template v-for="(char, charIndex) in line.split('')" :key="'char-' + charIndex">
                        <!-- 如果是空格 -->
                        <span v-if="char === ' '" 
                              :style="{ width: (slot.fontSize || 20) * 0.3 + 'px', height: (slot.fontSize || 20) + 'px' }">
                        </span>
                        
                        <!-- 如果有生成的字體圖片 -->
                        <img v-else-if="generatedFontImages.has(char)"
                             :src="generatedFontImages.get(char)" 
                             :alt="char"
                             class="object-contain"
                             :style="{ 
                               height: (slot.fontSize || 20) + 'px',
                               width: 'auto',
                               maxWidth: (slot.fontSize || 20) * 1.2 + 'px'
                             }"
                        />
                        
                        <!-- 如果沒有生成的字體，使用預設字體 -->
                        <span v-else
                              class="inline-block"
                              :style="{ 
                                fontSize: (slot.fontSize || 20) + 'px',
                                color: slot.color || '#333',
                                fontWeight: slot.fontWeight || 'normal',
                                lineHeight: (slot.lineHeight || 1.4)
                              }">
                          {{ char }}
                        </span>
                      </template>
                    </div>
                  </div>
                  
                  <!-- 預設文字顯示 -->
                  <div v-else
                       class="w-full h-full flex items-center"
                       :class="slot.align === 'center' ? 'justify-center' : slot.align === 'right' ? 'justify-end' : 'justify-start'">
                    <span class="text-slate-400 text-xs md:text-sm whitespace-pre-wrap"
                          :style="{ 
                            fontSize: (slot.fontSize || 20) * 0.8 + 'px',
                            textAlign: slot.align || 'left',
                            lineHeight: (slot.lineHeight || 1.4)
                          }">
                      {{ slotInputs[slot.key] || slot.placeholder || '輸入文字...' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 下載按鈕 -->
            <div class="flex flex-col sm:flex-row gap-3">
              <button
                @click="exportAsPNG"
                :disabled="!hasGeneratedFonts"
                class="flex-1 px-4 md:px-6 py-2.5 md:py-3 bg-gradient-to-r from-[#5EA897] to-[#3A6B60] text-white rounded-lg md:rounded-xl hover:from-[#4a9178] hover:to-[#2d5248] transition-all duration-200 flex items-center justify-center gap-2 font-medium shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-98 disabled:opacity-50 disabled:cursor-not-allowed text-sm md:text-base"
              >
                <svg class="w-4 h-4 md:w-5 md:h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                下載圖片
              </button>
              
              <button
                @click="goToWorkshop"
                class="px-4 md:px-6 py-2.5 md:py-3 border-2 border-[#5EA897] text-[#5EA897] rounded-lg md:rounded-xl hover:bg-[#5EA897] hover:text-white transition-all duration-200 flex items-center justify-center gap-2 font-medium shadow-sm hover:shadow-md text-sm md:text-base"
              >
                <svg class="w-4 h-4 md:w-5 md:h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                </svg>
                <span class="hidden sm:inline">重新上傳字型</span>
                <span class="sm:hidden">重新調整</span>
              </button>
            </div>
          </div>

          <!-- 內容編輯 -->
          <div class="bg-white/80 backdrop-blur-xl rounded-2xl md:rounded-3xl shadow-xl border border-white/20 p-4 md:p-6">
            <div class="flex items-center justify-between mb-4 md:mb-6">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 md:w-10 md:h-10 bg-gradient-to-br from-[#5EA897] to-[#3A6B60] rounded-lg md:rounded-xl flex items-center justify-center">
                  <svg class="w-4 h-4 md:w-5 md:h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <h2 class="text-lg md:text-xl font-bold text-slate-800">編輯內容</h2>
              </div>
              
              <label class="inline-flex items-center gap-2 text-xs md:text-sm font-medium text-slate-600 select-none cursor-pointer">
                <input
                  type="checkbox"
                  v-model="allSelected"
                  class="w-3 h-3 md:w-4 md:h-4 accent-[#5EA897] rounded"
                />
                全選
              </label>
            </div>

            <div v-if="currentSlots.length" class="space-y-3 md:space-y-4">
              <div
                v-for="slot in currentSlots"
                :key="slot.key"
                class="space-y-2 md:space-y-3 p-3 md:p-4 bg-slate-50 rounded-lg md:rounded-xl border border-slate-200 hover:border-[#5EA897]/30 transition-colors duration-200"
              >
                <div class="flex items-center justify-between">
                  <label class="text-xs md:text-sm font-semibold text-slate-700">{{ slot.label }}</label>
                  <label class="inline-flex items-center gap-1.5 md:gap-2 text-xs text-slate-600 select-none cursor-pointer">
                    <input
                      type="checkbox"
                      v-model="slotSelected[slot.key]"
                      class="w-2.5 h-2.5 md:w-3 md:h-3 accent-[#5EA897] rounded"
                    />
                    生成
                  </label>
                </div>
                
                <textarea
                  v-model="slotInputs[slot.key]"
                  :rows="slot.multiline ? 3 : 2"
                  class="w-full rounded-lg md:rounded-xl border border-slate-300 focus:ring-2 focus:ring-[#5EA897] focus:border-transparent text-slate-800 p-2.5 md:p-3 text-xs md:text-sm resize-none transition-all duration-200"
                  :placeholder="slot.placeholder || `輸入${slot.label}...`"
                ></textarea>
                
                <div class="flex items-center justify-between text-xs text-slate-500">
                  <div class="flex items-center gap-2">
                    <span class="px-1.5 md:px-2 py-0.5 md:py-1 bg-slate-200 rounded-full text-xs">{{ slot.align.toUpperCase() }}</span>
                    <span class="px-1.5 md:px-2 py-0.5 md:py-1 bg-slate-200 rounded-full text-xs">{{ slot.fontSize }}px</span>
                  </div>
                  <span class="text-slate-400 text-xs">使用生成字體</span>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-6 md:py-8 text-slate-500">
              <svg class="w-10 h-10 md:w-12 md:h-12 mx-auto mb-3 text-slate-300" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"/>
              </svg>
              <p class="text-xs md:text-sm">請先選擇模板</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  reactive,
  computed,
  onMounted,
  onBeforeUnmount,
  nextTick,
  watch,
} from "vue";

// 導入 html2canvas
import html2canvas from 'html2canvas';

// ===== 服務端設定 =====
const { getApiUrl } = useApi(); // 生成單字圖片 API



// ===== 模板（固定背景／位置／樣式） =====
// 重新設計美觀的賀卡模板
const templates = [
  {
    id: "wedding",
    name: "結婚賀卡",
    aspect: "4 / 3",
    thumbnail: "/cards/wedding_thumb.png",
    background: "/cards/wedding_bg.png",
    slots: [
      {
        key: "title",
        label: "標題",
        x: 50,
        y: 15,
        w: 40,
        fontSize: 32,
        fontWeight: "bold",
        align: "center",
        color: "#8B4513",
        defaultText: "新婚快樂",
        placeholder: "輸入標題...",
        multiline: false
      },
      {
        key: "message",
        label: "祝福語",
        x: 20,
        y: 45,
        w: 60,
        fontSize: 24,
        lineHeight: 1.5,
        align: "center",
        color: "#2F4F4F",
        defaultText: "願你們白頭偕老\n永結同心",
        placeholder: "輸入祝福語...",
        multiline: true
      },
      {
        key: "signature",
        label: "簽名",
        x: 70,
        y: 75,
        w: 20,
        fontSize: 20,
        align: "right",
        color: "#8B4513",
        defaultText: "祝福者",
        placeholder: "輸入簽名...",
        multiline: false
      }
    ]
  },
  {
    id: "love",
    name: "情書",
    aspect: "3 / 4",
    thumbnail: "/cards/love_thumb.png",
    background: "/cards/love_bg.png",
    slots: [
      {
        key: "greeting",
        label: "問候",
        x: 20,
        y: 20,
        w: 60,
        fontSize: 28,
        fontWeight: "bold",
        align: "center",
        color: "#DC143C",
        defaultText: "親愛的",
        placeholder: "輸入問候語...",
        multiline: false
      },
      {
        key: "content",
        label: "內容",
        x: 15,
        y: 40,
        w: 70,
        fontSize: 22,
        lineHeight: 1.6,
        align: "left",
        color: "#2F4F4F",
        defaultText: "每一天都因為有你\n而變得更加美好",
        placeholder: "輸入內容...",
        multiline: true
      },
      {
        key: "ending",
        label: "結尾",
        x: 60,
        y: 75,
        w: 30,
        fontSize: 20,
        align: "center",
        color: "#DC143C",
        defaultText: "愛你的我",
        placeholder: "輸入結尾...",
        multiline: false
      }
    ]
  },
  {
    id: "journal",
    name: "手寫帳",
    aspect: "16 / 9",
    thumbnail: "/cards/journal_thumb.png",
    background: "/cards/journal_bg.png",
    slots: [
      {
        key: "date",
        label: "日期",
        x: 10,
        y: 10,
        w: 25,
        fontSize: 18,
        align: "left",
        color: "#2F4F4F",
        defaultText: "2024年1月1日",
        placeholder: "輸入日期...",
        multiline: false
      },
      {
        key: "title",
        label: "標題",
        x: 35,
        y: 15,
        w: 30,
        fontSize: 24,
        fontWeight: "bold",
        align: "center",
        color: "#8B4513",
        defaultText: "今日記錄",
        placeholder: "輸入標題...",
        multiline: false
      },
      {
        key: "content",
        label: "內容",
        x: 15,
        y: 35,
        w: 70,
        fontSize: 20,
        lineHeight: 1.8,
        align: "left",
        color: "#2F4F4F",
        defaultText: "今天過得很充實...",
        placeholder: "輸入內容...",
        multiline: true
      }
    ]
  }
];

// ===== 狀態 =====
const currentTemplateId = ref("wedding");
const errorMsg = ref("");

// 產字參數與結果
const samplingStep = ref(15);
const referenceImage = ref(null);
const batching = ref(false);
const doneCount = ref(0);
const failures = ref([]);

// 生成的字體圖片
const generatedFontImages = ref(new Map()); // char -> imageUrl
const hasGeneratedFonts = computed(() => generatedFontImages.value && generatedFontImages.value.size > 0);

// 欄位內容 & 勾選狀態
const slotInputs = reactive({});
const slotSelected = reactive({}); // key -> boolean（是否要生成）

const generatedAny = computed(() => {
  if (!slotInputs || typeof slotInputs !== 'object') return false;
  return Object.values(slotInputs).some((v) => (v || "").length > 0);
});
const currentTemplate = computed(
  () => {
    if (!templates || !Array.isArray(templates) || !currentTemplateId.value) {
      return { id: "default", name: "預設模板", aspect: "3 / 2", slots: [] };
    }
    const template = templates.find((t) => t.id === currentTemplateId.value);
    return template || { id: "default", name: "預設模板", aspect: "3 / 2", slots: [] };
  }
);
const currentSlots = computed(() => currentTemplate.value?.slots || []);

const allSelected = computed({
  get() {
    return (
      currentSlots.value.length > 0 &&
      currentSlots.value.every((s) => !!slotSelected[s.key])
    );
  },
  set(v) {
    if (currentSlots.value && Array.isArray(currentSlots.value)) {
      currentSlots.value.forEach((s) => (slotSelected[s.key] = !!v));
    }
  },
});

const selectedKeys = computed(() => {
  if (!currentSlots.value || !Array.isArray(currentSlots.value)) return [];
  return currentSlots.value.filter((s) => !!slotSelected[s.key]).map((s) => s.key);
});

// 新增：控制字型生成區域顯示
const showFontGeneration = ref(false)

// 新增：檢查是否可以生成字型
const canGenerateFonts = computed(() => {
  // 如果有workshop字型數據，允許生成
  if (workshopFontData.value) {
    return referenceImage.value && true; // 只要有referenceImage就可以
  }
  // 否則需要等待用戶輸入文字
  return referenceImage.value && uniqueChars.value && uniqueChars.value.length > 0;
})

// ===== Smart Text Generation Related Variables =====
const slmCharacters = ref("Technology");
const slmStatus = ref("checking");

// Test and generation related variables
const testing = ref(false);
const testResult = ref("");
const chatting = ref(false);
const chatResult = ref("");
const userMessage = ref("Please generate related text content");
const chatHistory = ref([]);





// 新增：計算要生成的字元數量（用於進度條顯示）
const charsToGenerateCount = computed(() => {
  if (uniqueChars.value && uniqueChars.value.length > 0) {
    return uniqueChars.value.length;
  } else if (workshopFontData.value) {
    return 6; // 預設字元數量
  }
  return 0;
})

// 新增：workshop 字型數據
const workshopFontData = ref(null)

// 簡化模板選擇函數
function selectTemplate(templateId) {
  console.log('選擇模板:', templateId);
  
  // 驗證模板ID是否有效
  if (!templateId || !templates || !Array.isArray(templates) || !templates.find(t => t.id === templateId)) {
    console.warn('無效的模板ID:', templateId, '使用預設模板');
    templateId = "wedding";
  }
  
  currentTemplateId.value = templateId;
  
  // 重置相關狀態
  if (hasGeneratedFonts.value !== undefined) {
    hasGeneratedFonts.value = false;
  }
  if (generatedFontImages.value) {
    generatedFontImages.value.clear();
  }
  errorMsg.value = "";
  
  // 延遲更新以確保DOM更新完成
  if (typeof nextTick === 'function') {
    nextTick(() => {
      console.log('模板選擇完成，準備更新背景圖片');
      
      // 檢查背景圖片是否已載入
      if (bgEl.value && bgEl.value.complete && bgEl.value.naturalWidth > 0) {
        console.log('背景圖片已載入，直接更新');
        if (typeof onBgLoad === 'function') {
          onBgLoad({ target: bgEl.value });
        }
      } else {
        console.log('背景圖片未載入，等待載入事件');
        // 強制觸發圖片載入檢查
        setTimeout(() => {
          if (bgEl.value) {
            console.log('強制檢查背景圖片狀態');
            if (bgEl.value.complete && bgEl.value.naturalWidth > 0) {
              if (typeof onBgLoad === 'function') {
                onBgLoad({ target: bgEl.value });
              }
            }
          }
        }, 500);
      }
    });
  }
}

// 從被勾選的欄位收集唯一字元
const uniqueChars = computed(() => {
  if (!selectedKeys.value || !Array.isArray(selectedKeys.value)) return [];
  let s = "";
  for (const k of selectedKeys.value) s += slotInputs[k] || "";
  const arr = Array.from(s || "").filter((ch) => ch && ch.trim().length);
  return Array.from(new Set(arr));
});

function onRefImageChange(e) {
  if (!e || !e.target) {
    console.warn("onRefImageChange: 事件對象無效");
    return;
  }
  
  const f = e.target.files?.[0] || null;
  if (f && f.type !== "image/png") {
    console.warn("請上傳 PNG 檔");
    e.target.value = "";
    if (referenceImage.value !== undefined) {
      referenceImage.value = null;
    }
    return;
  }
  if (referenceImage.value !== undefined) {
    referenceImage.value = f;
  }
}

// 批量生成字型圖片
async function batchGenerateFonts() {
  if (!referenceImage.value) {
    console.warn("請先上傳你的手寫字（PNG）");
    return;
  }
  
  // 檢查是否有選中的區塊
  if (!selectedKeys.value || selectedKeys.value.length === 0) {
    console.warn("請先勾選欲生成的區塊");
    return;
  }
  
  // 獲取要生成的字元
  let charsToGenerate = uniqueChars.value || [];
  
  // 如果沒有字元但有workshop字型，使用預設字元
  if (charsToGenerate.length === 0 && workshopFontData.value) {
    console.log("沒有輸入文字，使用預設字元進行生成");
    charsToGenerate = ['早', '安', '你', '好', '謝', '謝']; // 預設字元
  } else if (charsToGenerate.length === 0) {
    console.warn("勾選的區塊沒有可生成的字");
    return;
  }

  batching.value = true;
  doneCount.value = 0;
  failures.value = [];
  errorMsg.value = "";
  
  // 清空之前的生成結果
  if (generatedFontImages.value) {
    generatedFontImages.value.clear();
  }
  
  console.log(`開始生成 ${charsToGenerate.length} 個字元:`, charsToGenerate);
  console.log('使用的參考圖片:', referenceImage.value);

  for (const ch of charsToGenerate) {
    try {
      const form = new FormData();
      form.append("character", ch);
      form.append("sampling_step", String(samplingStep.value));
      
      // 檢查 referenceImage 的類型並正確處理
      if (referenceImage.value instanceof File) {
        // 如果是 File 對象，直接使用
        form.append("reference_image", referenceImage.value);
        console.log(`字元 ${ch}: 使用 File 對象`);
      } else if (typeof referenceImage.value === 'string') {
        // 如果是 URL 字符串，需要先轉換為 File 對象
        try {
          const response = await fetch(referenceImage.value);
          const blob = await response.blob();
          const file = new File([blob], 'reference.png', { type: 'image/png' });
          form.append("reference_image", file);
          console.log(`字元 ${ch}: 將 URL 轉換為 File 對象`);
        } catch (fetchError) {
          console.error(`無法獲取圖片 ${referenceImage.value}:`, fetchError);
          throw new Error("無法處理參考圖片");
        }
      } else {
        throw new Error("參考圖片格式不正確");
      }

      console.log(`正在生成字元: ${ch}`);
      
      const res = await fetch(getApiUrl('/ai/generate'), {
        method: "POST",
        body: form,
      });
      
      if (!res.ok) {
        const errorText = await res.text();
        console.error(`API 錯誤 ${res.status}:`, errorText);
        throw new Error(`模型服務回應失敗 (${res.status}): ${errorText}`);
      }
      
      const data = await res.json();
      if (!data?.image) throw new Error("缺少 image URL");

      // 將生成的圖片URL存儲到Map中
      if (generatedFontImages.value) {
        generatedFontImages.value.set(ch, data.image);
      }
      console.log(`字元 ${ch} 生成成功:`, data.image);
      
    } catch (e) {
      console.error("生成失敗：", ch, e);
      failures.value.push(ch);
    } finally {
      doneCount.value += 1;
    }
  }

  if (!generatedFontImages.value || generatedFontImages.value.size === 0) {
    errorMsg.value = "全部字元皆產生失敗，請稍後重試";
  } else {
    errorMsg.value = "";
    console.log(`成功生成 ${generatedFontImages.value.size} 個字元:`, Array.from(generatedFontImages.value.keys()));
    console.log('生成的字體圖片:', Object.fromEntries(generatedFontImages.value));
    
    // 設置生成完成標記
    if (hasGeneratedFonts.value !== undefined) {
      hasGeneratedFonts.value = true;
    }
    
    // 強制更新預覽
    if (typeof nextTick === 'function') {
      await nextTick();
    }
    if (typeof updateContainRect === 'function') {
      updateContainRect();
    }
    
    // 顯示成功訊息
    console.log(`✅ 成功生成 ${generatedFontImages.value.size} 個字元的手寫字體！`);
  }

  batching.value = false;
}

// ===== Smart Text Generation Functions =====
// Test connection
async function testSLMConnection() {
  try {
    testing.value = true
    testResult.value = 'Testing connection...'
    
    const response = await fetch('http://localhost:8001/health', {
      method: 'GET'
    })
    
    if (response.ok) {
      const result = await response.json()
      testResult.value = `✅ Test successful! Service status: ${result.status}, Model status: ${result.model_status}`
      slmStatus.value = 'active'
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('❌ Test error:', error)
    testResult.value = `❌ Test error: ${error.message}`
    slmStatus.value = 'unhealthy'
  } finally {
    testing.value = false
  }
}

// Start text generation
async function startSLMChat() {
  try {
    chatting.value = true
    chatResult.value = ''
    
    const formData = new FormData()
    formData.append('characters', slmCharacters.value || 'Technology')
    formData.append('user_message', userMessage.value || 'Please generate related text content')
    formData.append('context', 'Smart Text Generation')
    
    const response = await fetch('http://localhost:8001/slm-chat', {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      const result = await response.json()
      chatResult.value = result.slm_response
      
      // Add to generation history
      chatHistory.value.unshift({
        characters: slmCharacters.value,
        userMessage: userMessage.value,
        response: result.slm_response,
        timestamp: new Date().toLocaleTimeString()
      })
      
      console.log('🎉 Text generation successful:', result)
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
  } catch (error) {
    console.error('❌ Text generation error:', error)
    chatResult.value = `❌ Text generation error: ${error.message}`
  } finally {
    chatting.value = false
  }
}

// 檢查服務狀態
async function checkSLMStatus() {
  try {
    const response = await fetch('http://localhost:8001/health', {
      method: 'GET'
    });
    
    if (response.ok) {
      const result = await response.json();
      slmStatus.value = result.status || 'active';
      console.log("服務狀態:", result);
    } else {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
  } catch (error) {
    console.error("檢查服務狀態失敗:", error);
    slmStatus.value = "unhealthy";
    
    // 如果是網絡錯誤，提供更詳細的日誌
    if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
      console.warn("服務可能未啟動或無法訪問");
    }
  }
}

// ===== 預覽與匯出 =====
const canvasWrap = ref(null);
const bgEl = ref(null);
const bgMeta = reactive({ w: 0, h: 0 });
const containRect = reactive({ x: 0, y: 0, w: 0, h: 0 });

const computedAspect = computed(() => {
  if (bgMeta && bgMeta.w > 0 && bgMeta.h > 0) return `${bgMeta.w} / ${bgMeta.h}`;
  return currentTemplate.value?.aspect || "3 / 2";
});

function onBgLoad(e) {
  const img = e.target;
  console.log('背景圖片載入完成:', img);
  console.log('圖片原始尺寸:', img.naturalWidth, 'x', img.naturalHeight);
  console.log('圖片顯示尺寸:', img.offsetWidth, 'x', img.offsetHeight);
  
  // 檢查圖片是否有效
  if (img.naturalWidth === 0 || img.naturalHeight === 0) {
    console.error('圖片尺寸無效，嘗試重新載入');
    // 強制重新載入
    img.src = img.src + '?t=' + Date.now();
    return;
  }
  
  // 確保 bgMeta 已初始化
  if (bgMeta && typeof bgMeta === 'object') {
    bgMeta.w = img.naturalWidth;
    bgMeta.h = img.naturalHeight;
    console.log('背景元數據已設置:', bgMeta);
  } else {
    console.warn('bgMeta 未初始化，跳過設置');
  }
  
  // 延遲更新以確保DOM完全渲染
  setTimeout(() => {
    if (typeof updateContainRect === 'function') {
      updateContainRect();
    }
    // 強制觸發重新渲染
    nextTick(() => {
      console.log('強制觸發重新渲染');
    });
  }, 200);
}

function onBgError(e) {
  console.error('背景圖片載入失敗:', e);
  if (e && e.target) {
    console.error('圖片src:', e.target.src);
  }
  console.warn('背景圖片載入失敗，請檢查圖片路徑');
}

function onResize() {
  if (typeof updateContainRect === 'function') {
    updateContainRect();
  }
}

// 自動載入 workshop 的字型數據
function loadWorkshopFontData() {
  try {
    const fontDataStr = localStorage.getItem('workshop_font_data')
    console.log('localStorage 中的 workshop_font_data:', fontDataStr)
    
    if (fontDataStr) {
      const fontData = JSON.parse(fontDataStr)
      console.log('解析後的字型數據:', fontData)

      // 檢查數據是否過期（24小時）
      const now = Date.now()
      const dataAge = now - fontData.timestamp
      const maxAge = 24 * 60 * 60 * 1000 // 24小時

      if (dataAge > maxAge) {
        console.log('字型數據已過期，清除舊數據')
        localStorage.removeItem('workshop_font_data')
        workshopFontData.value = null
        return
      }

      // 設定 workshop 字型數據
      if (workshopFontData.value !== undefined) {
        workshopFontData.value = fontData
        console.log('workshop 字型數據已設定:', workshopFontData.value)
      }

      // 自動設定上傳的字型圖片
      if (fontData.blendedImage || fontData.referenceImage) {
        console.log('找到字型圖片:', fontData.blendedImage || fontData.referenceImage)
        // 設定 referenceImage 為 workshop 的字型圖片
        if (referenceImage.value !== undefined) {
          referenceImage.value = fontData.blendedImage || fontData.referenceImage
        }
        
        // 自動啟用字型生成功能
        if (showFontGeneration.value !== undefined) {
          showFontGeneration.value = true
        }
        console.log('✅ 自動啟用字型生成功能')
      }
    } else {
      console.log('未找到 workshop 字型數據')
      workshopFontData.value = null
    }
  } catch (error) {
    console.error('載入 workshop 字型數據失敗:', error)
    workshopFontData.value = null
  }
}

// 組件掛載時
onMounted(() => {
  console.log('🔍 Template 頁面載入完成');
  console.log('🔍 檢查 localStorage 中的 workshop_font_data');
  
  // 確保模板數據已初始化
  if (!currentTemplateId.value) {
    currentTemplateId.value = "wedding";
  }
  
  // 初始化必要的函數
  if (typeof selectTemplate === 'function' && currentTemplateId.value) {
    selectTemplate(currentTemplateId.value);
  }
  if (typeof onResize === 'function') {
    window.addEventListener("resize", onResize);
  }
  
  // 自動載入 workshop 的字型數據
  if (typeof loadWorkshopFontData === 'function') {
    loadWorkshopFontData();
  }
  
  // 延遲檢查背景圖片狀態
  setTimeout(() => {
    console.log('🔍 延遲檢查背景圖片狀態');
    console.log('背景圖片元素:', bgEl.value);
    console.log('背景元數據:', bgMeta);
    
    // 如果背景圖片已經載入，強制更新
    if (bgEl.value && bgEl.value.complete && bgEl.value.naturalWidth > 0) {
      console.log('🔍 背景圖片已載入，強制更新');
      if (typeof onBgLoad === 'function') {
        onBgLoad({ target: bgEl.value });
      }
    } else {
      console.log('🔍 背景圖片未載入，等待載入事件');
    }
  }, 1000);
  
  // 檢查當前狀態
  console.log('🔍 當前 template 頁面狀態:');
  console.log('- workshopFontData:', workshopFontData.value);
  console.log('- referenceImage:', referenceImage.value);
  console.log('- showFontGeneration:', showFontGeneration.value);
  
  // 檢查服務狀態
  if (typeof checkSLMStatus === 'function') {
    checkSLMStatus();
  }
})

onBeforeUnmount(() => {
  if (typeof onResize === 'function') {
    window.removeEventListener("resize", onResize);
  }
});

// 移除舊的 Canvas 相關函數，因為現在使用 HTML2Canvas
// 使用生成的字體圖片繪製文字
// async function drawTextBlockWithGeneratedFonts(ctx, text, x, y, w, slot) {
//   if (!text) return;
//   
//   const fontSize = slot.fontSize || 20;
//   const scale = 3; // 放大倍數
//   const scaledFontSize = fontSize * scale;
//   
//   ctx.textBaseline = "top";
//   ctx.textAlign = slot.align;
//   
//   const lines = (text || "").split("\n");
//   const lh = (slot.lineHeight ? slot.lineHeight : 1.4) * scaledFontSize;
//   
//   let currentY = y;
//   
//   for (const line of lines) {
//     const words = line.split("");
//     let currentX = x;
//     
//     if (slot.align === "center") {
//       currentX = x + w / 2;
//     } else if (slot.align === "right") {
//       currentX = x + w;
//     }
//     
//     for (const char of words) {
//       if (char.trim() === "") {
//         // 空格處理
//         const spaceWidth = scaledFontSize * 0.5;
//         currentX += spaceWidth;
//         continue;
//       }
//       
//       if (generatedFontImages.value.has(char)) {
//         // 使用生成的字體圖片
//         const img = new Image();
//         img.crossOrigin = "anonymous";
//         await new Promise((resolve, reject) => {
//           img.onload = resolve;
//           img.onerror = reject;
//           img.src = generatedFontImages.value.get(char);
//         });
//         
//         const charWidth = (img.width / img.height) * scaledFontSize;
//         ctx.drawImage(img, currentX, currentY, charWidth, scaledFontSize);
//         currentX += charWidth;
//       } else {
//         // 沒有生成的字體圖片，使用預設字體
//         ctx.font = `${scaledFontSize}px Arial`;
//         ctx.fillStyle = "#1f2937";
//         ctx.fillText(char, currentX, currentY);
//         currentX += ctx.measureText(char).width;
//       }
//     }
//     
//     currentY += lh;
//   }
// }

// 移除舊的圖片繪製函數
// async function drawImageScaled(ctx, src, x, y, w, h) {
//   return new Promise((resolve, reject) => {
//     const img = new Image();
//     img.crossOrigin = "anonymous";
//     img.onload = () => {
//       ctx.drawImage(img, x, y, w, h);
//       resolve();
//     };
//     img.onerror = reject;
//     img.src = src;
//   });
// }

// 簡化座標計算，確保預覽正常顯示
function slotStyle(slot, asText = false) {
  if (!slot || !containRect) {
    console.warn('slotStyle: slot 或 containRect 未定義');
    return {};
  }
  
  const rect = containRect;
  const { x, y, w } = slotPixelsForRect(slot, rect);
  
  const style = { 
    position: 'absolute',
    top: `${y}px`, 
    width: `${w}px`,
    zIndex: 10
  };
  
  if (slot.align === 'center') { 
    style.left = `${x}px`; 
    style.transform = 'translateX(-50%)'; 
    style.textAlign = 'center'; 
  }
  else if (slot.align === 'right') { 
    style.left = `${x}px`; 
    style.transform = 'translateX(-100%)'; 
    style.textAlign = 'right'; 
  }
  else { 
    style.left = `${x}px`; 
    style.textAlign = 'left'; 
  }
  
  if (asText) {
    style.fontSize = (slot.fontSize || 20) + 'px';
    style.lineHeight = String(slot.lineHeight || 1.3);
    style.whiteSpace = 'pre-wrap';
    style.color = slot.color || '#1f2937';
    style.fontWeight = slot.fontWeight || 'normal';
    
    // 如果有生成的字體，使用圖片字體
    if (hasGeneratedFonts.value) {
      style.fontFamily = 'Arial, sans-serif'; // 備用字體
    }
  }
  
  return style;
}

// 簡化座標計算函數
function slotPixelsForRect(slot, rect) {
  if (!slot || !rect) {
    console.warn('slotPixelsForRect: slot 或 rect 未定義');
    return { x: 0, y: 0, w: 0 };
  }
  
  const xPct = slot.x / 100;
  const yPct = slot.y / 100;
  const wPct = slot.w / 100;
  
  const x = rect.x + rect.w * xPct;
  const y = rect.y + rect.h * yPct;
  const w = rect.w * wPct;
  
  return { x, y, w };
}

// 新的位置計算函數，直接基於背景圖片尺寸
function getSlotPosition(slot, dimension) {
  console.log('getSlotPosition 被調用:', { slot, dimension, bgMeta });
  
  // 檢查是否在瀏覽器環境中
  if (typeof document === 'undefined') {
    console.warn('服務端渲染環境，返回預設值');
    // 服務端渲染時返回預設值
    switch (dimension) {
      case 'x':
        return (slot.x / 100) * 800; // 預設寬度800px
      case 'y':
        return (slot.y / 100) * 600; // 預設高度600px
      case 'w':
        return (slot.w / 100) * 800;
      case 'h':
        return (slot.h / 100) * 600;
      default:
        return 0;
    }
  }
  
  if (!bgMeta || !bgMeta.w || !bgMeta.h) {
    console.warn('背景圖片尺寸未載入，使用預設值');
    // 使用預設值
    const container = document.getElementById('template-preview-container');
    if (!container) return 0;
    
    const containerRect = container.getBoundingClientRect();
    const defaultWidth = containerRect.width;
    const defaultHeight = containerRect.height;
    
    // 根據維度返回對應的值
    switch (dimension) {
      case 'x':
        return (slot.x / 100) * defaultWidth;
      case 'y':
        return (slot.y / 100) * defaultHeight;
      case 'w':
        return (slot.w / 100) * defaultWidth;
      case 'h':
        return (slot.h / 100) * defaultHeight;
      default:
        return 0;
    }
  }
  
  const container = document.getElementById('template-preview-container');
  if (!container) {
    console.error('找不到預覽容器');
    return 0;
  }
  
  const containerRect = container.getBoundingClientRect();
  const imgElement = bgEl.value;
  
  if (!imgElement) {
    console.error('找不到背景圖片元素');
    return 0;
  }
  
  const imgRect = imgElement.getBoundingClientRect();
  console.log('容器尺寸:', containerRect);
  console.log('圖片元素尺寸:', imgRect);
  
  // 計算背景圖片在容器中的實際尺寸和位置
  const imgAspect = bgMeta.w / bgMeta.h;
  const containerAspect = containerRect.width / containerRect.height;
  
  let imgWidth, imgHeight, imgX, imgY;
  
  if (imgAspect > containerAspect) {
    // 圖片較寬，以容器寬度為準
    imgWidth = containerRect.width;
    imgHeight = containerRect.width / imgAspect;
    imgX = 0;
    imgY = (containerRect.height - imgHeight) / 2;
  } else {
    // 圖片較高，以容器高度為準
    imgHeight = containerRect.height;
    imgWidth = containerRect.height * imgAspect;
    imgX = (containerRect.width - imgWidth) / 2;
    imgY = 0;
  }
  
  console.log('計算的圖片尺寸和位置:', { imgWidth, imgHeight, imgX, imgY });
  
  // 根據維度返回對應的值
  let result;
  switch (dimension) {
    case 'x':
      result = imgX + (slot.x / 100) * imgWidth;
      break;
    case 'y':
      result = imgY + (slot.y / 100) * imgHeight;
      break;
    case 'w':
      result = (slot.w / 100) * imgWidth;
      break;
    case 'h':
      result = (slot.h / 100) * imgHeight;
      break;
    default:
      result = 0;
  }
  
  console.log(`維度 ${dimension} 的結果:`, result);
  return result;
}

// 簡化背景圖片計算函數
function calcContainRect(boxW, boxH, imgW, imgH) {
  if (!imgW || !imgH || !boxW || !boxH) return { x: 0, y: 0, w: boxW || 800, h: boxH || 600 };
  
  const imgR = imgW / imgH;
  const boxR = boxW / boxH;
  
  if (imgR > boxR) {
    const w = boxW;
    const h = boxW / imgR;
    return { x: 0, y: (boxH - h) / 2, w, h };
  } else {
    const h = boxH;
    const w = boxH * imgR;
    return { x: (boxW - w) / 2, y: 0, w, h };
  }
}

// 簡化更新容器尺寸函數
function updateContainRect() {
  nextTick(() => {
    const wrap = canvasWrap.value;
    
    // 檢查是否在瀏覽器環境中
    if (typeof document === 'undefined') {
      console.warn('服務端渲染環境，跳過容器尺寸更新');
      return;
    }
    
    const container = document.getElementById('template-preview-container');
    
    if (!wrap || !container || !bgMeta || !bgMeta.w || !bgMeta.h) {
      console.log('更新容器尺寸失敗:', { wrap: !!wrap, container: !!container, bgMeta });
      return;
    }
    
    const cw = container.clientWidth;
    const ch = container.clientHeight;
    const imgR = bgMeta.w / bgMeta.h;
    const boxR = cw / ch;
    
    console.log('容器尺寸:', cw, 'x', ch);
    console.log('圖片比例:', imgR, '容器比例:', boxR);
    
    if (imgR > boxR) {
      const w = cw;
      const h = cw / imgR;
      containRect.x = 0;
      containRect.y = (ch - h) / 2;
      containRect.w = w;
      containRect.h = h;
    } else {
      const h = ch;
      const w = ch * imgR;
      containRect.x = (cw - w) / 2;
      containRect.y = 0;
      containRect.w = w;
      containRect.h = h;
    }
    
    console.log('容器矩形已更新:', containRect);
  });
}

// 輸出圖片

// 使用 HTML2Canvas 下載，確保與預覽完全一致
async function exportAsPNG() {
  if (!hasGeneratedFonts || !hasGeneratedFonts.value) {
    console.warn("請先生成字體");
    return;
  }

  try {
    // 檢查是否在瀏覽器環境中
    if (typeof document === 'undefined') {
      throw new Error("服務端渲染環境無法導出圖片");
    }
    
    // 獲取包含背景圖片的整個預覽容器
    const previewContainer = document.getElementById('template-preview-container');
    
    if (!previewContainer) {
      throw new Error("無法找到預覽容器");
    }

    // 顯示載入狀態
    errorMsg.value = "正在生成圖片...";
    
    console.log('開始截圖，容器:', previewContainer);
    console.log('容器尺寸:', previewContainer.offsetWidth, 'x', previewContainer.offsetHeight);
    
    // 等待一下確保DOM完全渲染
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // 確保所有圖片都已載入
    const images = previewContainer.querySelectorAll('img');
    console.log('找到的圖片數量:', images.length);
    
    await Promise.all(Array.from(images).map((img, index) => {
      console.log(`圖片 ${index}:`, img.src, '載入狀態:', img.complete);
      if (img.complete) return Promise.resolve();
      return new Promise((resolve, reject) => {
        img.onload = () => {
          console.log(`圖片 ${index} 載入完成`);
          resolve();
        };
        img.onerror = () => {
          console.log(`圖片 ${index} 載入失敗`);
          resolve(); // 不阻擋其他圖片
        };
        // 設置超時以防圖片載入失敗
        setTimeout(() => {
          console.log(`圖片 ${index} 載入超時`);
          resolve();
        }, 3000);
      });
    }));
    
    // 檢查容器內容
    console.log('容器HTML內容:', previewContainer.innerHTML);
    console.log('背景圖片元素:', bgEl.value);
    console.log('背景圖片尺寸:', bgMeta.w, 'x', bgMeta.h);
    
    // 使用 HTML2Canvas 截圖
    const canvas = await html2canvas(previewContainer, {
      scale: 2, // 降低到2x以避免記憶體問題
      useCORS: true, // 允許跨域圖片
      allowTaint: true, // 允許外部圖片
      backgroundColor: '#ffffff', // 設置白色背景
      width: previewContainer.offsetWidth,
      height: previewContainer.offsetHeight,
      scrollX: 0,
      scrollY: 0,
      foreignObjectRendering: false, // 關閉外部對象渲染
      removeContainer: false, // 不移除容器
      imageTimeout: 15000, // 增加圖片載入超時時間
      logging: true, // 啟用日誌以便調試
      onclone: (clonedDoc) => {
        console.log('克隆文檔:', clonedDoc);
        // 在克隆文檔中確保圖片正確載入
        const clonedImages = clonedDoc.querySelectorAll('img');
        clonedImages.forEach((img, index) => {
          console.log(`克隆圖片 ${index}:`, img.src);
          if (img.src && !img.src.startsWith('data:')) {
            img.crossOrigin = 'anonymous';
          }
        });
      }
    });

    // 獲取最終尺寸
    const finalWidth = canvas.width;
    const finalHeight = canvas.height;
    
    console.log('截圖完成，畫布尺寸:', finalWidth, 'x', finalHeight);
    
    // 檢查畫布內容
    const ctx = canvas.getContext('2d');
    const imageData = ctx.getImageData(0, 0, finalWidth, finalHeight);
    const hasContent = imageData.data.some(pixel => pixel !== 0);
    console.log('畫布是否有內容:', hasContent);

    // 下載圖片
    const url = canvas.toDataURL('image/png', 1.0);
    
    // 檢查是否在瀏覽器環境中
    if (typeof document !== 'undefined') {
      const a = document.createElement('a');
      a.href = url;
      a.download = `${currentTemplate.value.name}_${new Date().getTime()}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } else {
      console.warn('服務端渲染環境，無法下載圖片');
    }
    
    errorMsg.value = "";
    console.log("圖片匯出成功！檔案名稱:", a.download);
    console.log("✅ 圖片下載成功！");
    
  } catch (error) {
    console.error("匯出失敗:", error);
    errorMsg.value = "匯出失敗：" + error.message;
    console.error("❌ 匯出失敗：" + error.message);
  }
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}

// 移除舊的圖片繪製函數
// async function drawImageScaled(ctx, src, x, y, w, h) {
//   return new Promise((resolve, reject) => {
//     const img = new Image();
//     img.crossOrigin = "anonymous";
//     img.onload = () => {
//       ctx.drawImage(img, x, y, w, h);
//       resolve();
//     };
//     img.onerror = reject;
//     img.src = src;
//   });
// }

// 跳轉到 workshop 頁面
function goToWorkshop() {
  navigateTo('/workshop')
}

// 新增：使用 workshop 字型
const useWorkshopFont = async () => {
  if (workshopFontData.value) {
    try {
      // 獲取字型圖片URL
      const imageUrl = workshopFontData.value.blendedImage || workshopFontData.value.referenceImage
      console.log('🎨 準備載入 workshop 字型圖片:', imageUrl)
      
      if (!imageUrl) {
        console.error('❌ 未找到 workshop 字型圖片')
        return
      }
      
      // 將URL轉換為File對象
      const response = await fetch(imageUrl)
      if (!response.ok) {
        throw new Error(`無法獲取圖片: ${response.status}`)
      }
      
      const blob = await response.blob()
      const file = new File([blob], 'workshop_font.png', { type: 'image/png' })
      
      // 設定 referenceImage 為 File 對象
      referenceImage.value = file
      
      // 顯示字型生成區域
      showFontGeneration.value = true
      
      // 重置生成狀態
      hasGeneratedFonts.value = false
      
      // 顯示成功訊息
      console.log('✅ 已載入 workshop 字型風格，可以開始生成字型到模板！')
      
      console.log('✅ 已使用 workshop 字型:', referenceImage.value)
      console.log('📁 字型文件類型:', referenceImage.value instanceof File ? 'File' : typeof referenceImage.value)
      console.log('📁 字型文件大小:', referenceImage.value instanceof File ? `${referenceImage.value.size} bytes` : 'N/A')
      
    } catch (error) {
      console.error('❌ 載入 workshop 字型失敗:', error)
      console.error(`❌ 載入字型失敗: ${error.message}`)
    }
  }
}

// 新增：使用現成字型
const useExistingFonts = () => {
  // 顯示現成字型選擇對話框
  const fontOptions = [
    { name: 'JasonHandwriting1', displayName: '傑森手寫體 1', path: '/fonts/JasonHandwriting1.woff2' },
    { name: 'JasonHandwriting2', displayName: '傑森手寫體 2', path: '/fonts/JasonHandwriting2.woff2' },
    { name: 'JasonHandwriting3', displayName: '傑森手寫體 3', path: '/fonts/JasonHandwriting3.woff2' },
    { name: 'JasonHandwriting4', displayName: '傑森手寫體 4', path: '/fonts/JasonHandwriting4.woff2' },
    { name: 'JasonHandwriting5', displayName: '傑森手寫體 5', path: '/fonts/JasonHandwriting5.woff2' },
    { name: 'JasonHandwriting5p', displayName: '傑森手寫體 5+', path: '/fonts/JasonHandwriting5p.woff2' }
  ]
  
  // 創建字型選擇對話框
  const selectedFont = prompt(
    `請選擇要使用的手寫字型：\n\n${fontOptions.map((font, index) => `${index + 1}. ${font.displayName}`).join('\n')}\n\n請輸入數字 1-6：`
  )
  
  if (selectedFont && /^[1-6]$/.test(selectedFont)) {
    const fontIndex = parseInt(selectedFont) - 1
    const selectedFontData = fontOptions[fontIndex]
    
    console.log('🎨 選擇了現成字型:', selectedFontData.displayName)
    
    // 設定為使用現成字型模式
    showFontGeneration.value = true
    hasGeneratedFonts.value = false
    
    // 顯示成功訊息
    console.log(`✅ 已選擇字型：${selectedFontData.displayName}\n\n現在可以開始生成字型到模板！`)
    
    // 這裡可以添加邏輯來使用選定的字型
    // 例如：設定一個標記來表示使用現成字型
    // useExistingFontMode.value = true
    // selectedExistingFont.value = selectedFontData
    
  } else if (selectedFont !== null) {
    console.warn('❌ 請輸入有效的數字 1-6')
  }
}


</script>

<style scoped>
/* 範圍滑塊樣式 */
.range-slider-orange {
  -webkit-appearance: none;
  appearance: none;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(
    to right,
    #d1d5db 0%,
    #d1d5db 50%,
    #e29930 50%,
    #e29930 100%
  );
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.range-slider-orange:hover {
  background: linear-gradient(
    to right,
    #d1d5db 0%,
    #d1d5db 50%,
    #d48826 50%,
    #d48826 100%
  );
}

.range-slider-orange::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e29930, #d48826);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(226, 153, 48, 0.4);
  transition: all 0.2s ease;
}

.range-slider-orange::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(226, 153, 48, 0.6);
}

.range-slider-orange::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e29930, #d48826);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(226, 153, 48, 0.4);
  transition: all 0.2s ease;
}

.range-slider-orange::-moz-range-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(226, 153, 48, 0.6);
}

/* 自定義動畫 */
@keyframes scale-98 {
  0% { transform: scale(1); }
  100% { transform: scale(0.98); }
}

.active\:scale-98:active {
  animation: scale-98 0.1s ease-out;
}

/* 玻璃擬態效果 */
.backdrop-blur-xl {
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}

/* 漸變文字效果 */
.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}

/* 懸停效果 */
.group:hover .group-hover\:scale-110 {
  transform: scale(1.1);
}

.group:hover .group-hover\:scale-105 {
  transform: scale(1.05);
}

/* 進度條動畫 */
@keyframes progress-glow {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.progress-glow {
  animation: progress-glow 2s ease-in-out infinite;
}

/* 響應式設計優化 */
@media (max-width: 1024px) {
  .lg\:grid-cols-12 {
    grid-template-columns: 1fr;
  }
  
  .lg\:col-span-5,
  .lg\:col-span-7 {
    grid-column: span 1;
  }
}

/* 深色模式支援 */
@media (prefers-color-scheme: dark) {
  .bg-white\/80 {
    background-color: rgba(30, 41, 59, 0.8);
  }
  
  .border-white\/20 {
    border-color: rgba(255, 255, 255, 0.1);
  }
  
  .text-slate-800 {
    color: #f1f5f9;
  }
  
  .text-slate-600 {
    color: #cbd5e1;
  }
  
  .text-slate-500 {
    color: #94a3b8;
  }
  
  .bg-slate-50 {
    background-color: rgba(30, 41, 59, 0.5);
  }
  
  .border-slate-200 {
    border-color: rgba(148, 163, 184, 0.3);
  }
}

/* 動畫優化 */
.transition-all {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.duration-300 {
  transition-duration: 300ms;
}

/* 陰影效果 */
.shadow-xl {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* 邊框圓角 */
.rounded-2xl {
  border-radius: 1rem;
}

.rounded-3xl {
  border-radius: 1.5rem;
}

/* 字體優化 */
.font-semibold {
  font-weight: 600;
}

.font-bold {
  font-weight: 700;
}

/* 間距優化 */
.space-y-6 > * + * {
  margin-top: 1.5rem;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}

.space-y-3 > * + * {
  margin-top: 0.75rem;
}

/* 響應式間距 */
@media (max-width: 768px) {
  .space-y-6 > * + * {
    margin-top: 1rem;
  }
  
  .space-y-4 > * + * {
    margin-top: 0.75rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.5rem;
  }
}
</style>
