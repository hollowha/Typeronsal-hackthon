<template>
  <div class="min-h-screen bg-[#F8F3EA]">
    <!-- 主標題區域 -->
    <div class="pt-8 pb-6 px-8">
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-[#3A6B60] mb-2 underline">字型工坊</h1>
            <p class="text-[#3A6B60]">創造屬於你的獨特字型風格</p>
          </div>
          <div class="flex items-center gap-3">
            <div v-if="isProcessing" class="flex items-center gap-2 text-[#3A6B60] bg-[#5EA897] bg-opacity-20 px-3 py-2 rounded-lg border border-[#5EA897]">
              <div class="w-4 h-4 border-2 border-[#3A6B60] border-t-transparent rounded-full animate-spin"></div>
              <span class="text-sm font-medium">AI 生成中</span>
            </div>
            <div v-else-if="previewImage" class="flex items-center gap-2 text-[#3A6B60] bg-[#5EA897] bg-opacity-20 px-3 py-2 rounded-lg border border-[#5EA897]">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <span class="text-sm font-medium">預覽就緒</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-8 pb-20">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 左側 - 預覽區域 -->
        <div class="space-y-6">
          <!-- 預覽卡片 -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="p-6">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-semibold text-[#3A6B60]">即時預覽</h2>
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 bg-[#5EA897] rounded-full animate-pulse"></div>
                  <span class="text-sm text-[#3A6B60]">即時更新</span>
                </div>
              </div>
              
              <div
                class="relative bg-white rounded-xl aspect-video flex items-center justify-center overflow-hidden transition-all duration-300 border border-gray-200"
                :class="{ 'ring-2 ring-[#E29930] bg-orange-50 border-[#E29930]': isThicknessChanging }"
              >
                <div v-if="isProcessing" class="absolute inset-0 bg-white bg-opacity-90 flex items-center justify-center z-10">
                  <div class="text-center">
                    <div class="w-8 h-8 border-3 border-[#3A6B60] border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
                    <span class="text-[#3A6B60] font-medium">AI 正在創作中</span>
                  </div>
                </div>
                
                <img
                  v-if="previewImage"
                  :src="previewImage"
                  alt="字型預覽"
                  class="max-h-full max-w-full object-contain transition-all duration-500"
                  :class="{ 'scale-105': isThicknessChanging }"
                />
                
                <div v-else class="text-center text-gray-500">
                  <div class="w-16 h-16 bg-[#5EA897] bg-opacity-25 rounded-xl flex items-center justify-center mx-auto mb-4 border border-[#5EA897] border-opacity-30">
                    <svg class="w-8 h-8 text-[#5EA897]" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <p class="font-medium text-[#3A6B60]">字型預覽區域</p>
                  <p class="text-sm mt-2 text-gray-500" v-if="!hasUserAdjusted">正在載入原始字型預覽</p>
                  <p class="text-sm mt-2 text-gray-500" v-else-if="styleOption.length === 0">選擇風格標籤開始調整</p>
                  <p class="text-sm mt-2 text-gray-500" v-else>正在生成個性化效果</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 精細調整區域 - 移到預覽下方 -->
          <div v-if="styleOption.length > 0" class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center gap-3 mb-6">
              <div class="w-8 h-8 bg-[#5EA897] bg-opacity-25 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-[#3A6B60]" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z"/>
                </svg>
              </div>
              <div>
                <h3 class="font-semibold text-[#3A6B60]">精細調整</h3>
                <p class="text-sm text-gray-600">微調字型的視覺效果</p>
              </div>
            </div>

            <div class="space-y-8">
              <!-- 筆觸粗細 -->
              <div>
                <div class="flex items-center justify-between mb-4">
                  <div class="flex items-center gap-2">
                    <div class="w-3 h-3 bg-[#5EA897] rounded-full"></div>
                    <span class="font-medium text-[#3A6B60]">筆觸粗細</span>
                  </div>
                  <div class="flex items-center gap-2 text-sm">
                    <span class="text-gray-600">即時預覽</span>
                    <div class="w-2 h-2 bg-[#5EA897] rounded-full animate-pulse"></div>
                  </div>
                </div>
                
                <div class="space-y-4">
                  <div class="flex items-center gap-4">
                    <span class="text-sm text-gray-500 w-8 text-center">細</span>
                    <div class="flex-1 relative">
                      <input
                        type="range"
                        min="-1.5"
                        max="1.5"
                        step="0.05"
                        v-model.number="thickness"
                        class="w-full range-slider-teal"
                        :class="{ 'animate-pulse': isThicknessChanging }"
                      />
                    </div>
                    <span class="text-sm text-gray-500 w-8 text-center">粗</span>
                  </div>
                  <div class="text-center">
                    <span class="inline-block bg-[#5EA897] bg-opacity-20 text-[#3A6B60] text-sm px-3 py-1 rounded-full font-medium">
                      {{ thickness.toFixed(2) }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- 風格融合比例 -->
              <div>
                <div class="flex items-center justify-between mb-4">
                  <div class="flex items-center gap-2">
                    <div class="w-3 h-3 bg-[#E29930] rounded-full"></div>
                    <span class="font-medium text-[#3A6B60]">風格融合比例</span>
                  </div>
                  <span class="text-xs text-[#E29930] bg-[#E29930] bg-opacity-20 px-2 py-1 rounded-full">
                    原圖 ← → {{ styleOption[0] || '風格' }}
                  </span>
                </div>
                
                <div class="space-y-4">
                  <div class="flex items-center gap-4">
                    <span class="text-sm text-gray-500 w-12 text-center">原圖</span>
                    <div class="flex-1 relative">
                      <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.05"
                        v-model.number="alpha"
                        class="w-full range-slider-orange"
                      />
                    </div>
                    <span class="text-sm text-gray-500 w-12 text-center">風格</span>
                  </div>
                  <div class="text-center">
                    <span class="inline-block bg-[#E29930] bg-opacity-20 text-[#E29930] text-sm px-3 py-1 rounded-full font-medium">
                      {{ Math.round(alpha * 100) }}% 風格強度
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 預覽文字輸入 -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 bg-[#5EA897] bg-opacity-25 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-[#3A6B60]" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                </svg>
              </div>
              <div>
                <h3 class="font-semibold text-[#3A6B60]">預覽文字</h3>
                <p class="text-sm text-gray-600">輸入想要預覽的文字內容</p>
              </div>
            </div>
            
            <input
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#E29930] focus:border-transparent transition-all duration-200 text-lg bg-gray-50 text-[#3A6B60] placeholder-gray-500"
              placeholder="輸入你想預覽的字"
              v-model="character"
            />
          </div>

          <!-- 重新生成按鈕 -->
          <div class="flex justify-center">
            <button
              @click="hasUserAdjusted && styleOption.length > 0 ? blend() : generateOriginalPreview()"
              class="bg-[#E29930] hover:bg-[#d18825] text-white px-8 py-3 rounded-xl font-medium shadow-sm hover:shadow-md transform hover:scale-[1.02] transition-all duration-200 flex items-center gap-3"
              :disabled="isProcessing"
              :class="{ 'opacity-50 cursor-not-allowed transform-none': isProcessing }"
            >
              <svg v-if="!isProcessing" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"/>
              </svg>
              {{ 
                isProcessing ? '生成中...' : 
                (hasUserAdjusted && styleOption.length > 0) ? '重新生成' : '重新載入預覽'
              }}
            </button>
          </div>
        </div>

        <!-- 右側 - 控制面板 -->
        <div class="space-y-6">
          <!-- 快速開始卡片 -->
          <div class="bg-gradient-to-br from-[#5EA897] from-10% via-[#5EA897] via-30% to-[#3A6B60] to-90% rounded-2xl shadow-lg border border-[#5EA897] p-6 text-white">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold">滿意目前效果？</h3>
                <p class="text-sm text-white text-opacity-90">直接使用原始字型生成完整字體包</p>
              </div>
            </div>
            
            <button
              @click="proceedWithOriginal"
              class="w-full bg-white bg-opacity-20 hover:bg-opacity-30 text-white font-semibold py-3 px-4 rounded-xl transition-all duration-200 flex items-center justify-center gap-2 backdrop-blur-sm border border-white border-opacity-30"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              直接生成字型
            </button>
          </div>

          <!-- 或者分隔線 -->
          <div class="relative flex items-center">
            <div class="flex-grow border-t border-gray-300"></div>
            <span class="flex-shrink mx-4 text-gray-500 bg-[#F8F3EA] px-2">或者</span>
            <div class="flex-grow border-t border-gray-300"></div>
          </div>

          <!-- 進階調整區域 -->
          <div class="space-y-6">
            <!-- 風格選擇 -->
            <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-8 h-8 bg-[#E29930] bg-opacity-25 rounded-lg flex items-center justify-center">
                  <svg class="w-4 h-4 text-[#E29930]" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <h3 class="font-semibold text-[#3A6B60]">風格調整</h3>
                    <span class="bg-[#E29930] bg-opacity-20 text-[#E29930] text-xs px-2 py-1 rounded-full">進階功能</span>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">選擇風格標籤來個性化你的字型</p>
                </div>
              </div>
              
              <div class="grid grid-cols-2 gap-3">
                <div
                  v-for="option in styleOptions"
                  :key="option"
                  @click="toggleTag(option)"
                  class="relative p-4 border-2 rounded-xl cursor-pointer transition-all duration-200 group hover:scale-[1.02]"
                  :class="
                    styleOption.includes(option)
                      ? 'border-[#E29930] bg-[#E29930] bg-opacity-10'
                      : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
                  "
                >
                  <div class="text-center">
                    <div class="font-medium text-[#3A6B60] mb-1">{{ option }}</div>
                    <div v-if="styleOption.includes(option)" class="absolute -top-2 -right-2 w-6 h-6 bg-[#E29930] rounded-full flex items-center justify-center">
                      <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 選擇風格後的功能區 -->
              <div v-if="styleOption.length > 0" class="mt-4 space-y-3">
                <!-- 回到原始字型按鈕 -->
                <button
                  @click="resetToOriginal"
                  class="w-full bg-gray-100 hover:bg-gray-200 text-[#3A6B60] font-medium py-3 px-4 rounded-xl transition-all duration-200 flex items-center justify-center gap-2 border border-gray-300 hover:border-gray-400"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"/>
                  </svg>
                  回到原始字型
                </button>

                <!-- 提示訊息 -->
                <div class="p-3 bg-[#5EA897] bg-opacity-10 rounded-lg border border-[#5EA897] border-opacity-30">
                  <div class="flex items-center gap-2 text-sm text-[#3A6B60]">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                    </svg>
                    <span>✨ 精細調整工具已在預覽區域下方顯示</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部確認按鈕 -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-6">
      <div class="max-w-7xl mx-auto flex justify-center">
        <button
          @click="$router.push('/create')"
          class="bg-[#3A6B60] hover:bg-[#2d5349] text-white px-12 py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200 flex items-center gap-3"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          確認生成字型
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 添加認證中介軟體
definePageMeta({
  middleware: 'auth'
})

import { ref, watch } from "vue";

const API_BASE_URL = "https://typersonal.dy6.click/8000";
const imageUrl = ref("");
const previewImage = ref("");
const character = ref("字"); // 預設值
const enableBlend = ref(true);
const alpha = ref(0.5);
const thickness = ref(0);
const blendImageUrl = ref("");

// 狀態管理
const isProcessing = ref(false);
const isThicknessChanging = ref(false);
const hasUserAdjusted = ref(false); // 追蹤用戶是否已經進行調整

onMounted(() => {
  const img = localStorage.getItem("fonty_api_image");
  const savedCharacter = localStorage.getItem("fonty_character");
  
  imageUrl.value = img || "";
  
  // 如果有儲存的字元，就使用儲存的字元
  if (savedCharacter) {
    character.value = savedCharacter;
  }
  
  // 自動載入原始字型預覽
  if (img && character.value.trim()) {
    generateOriginalPreview();
  }
});

// Use an array for multiple selection - 預設選擇第一個風格標籤
const styleOption = ref([]);
const styleOptions = ["書法風", "簡約現代", "潑墨風", "潮流街頭", "可愛手繪"];

// 監聽粗細調整，即時預覽
let debounceTimeout;
watch(thickness, async () => {
  if (imageUrl.value && styleOption.value.length > 0) {
    hasUserAdjusted.value = true;
    // 顯示粗細調整的視覺反饋
    isThicknessChanging.value = true;
    
    // 清除之前的計時器
    clearTimeout(debounceTimeout);
    
    // 設置新的計時器，300ms 後執行
    debounceTimeout = setTimeout(async () => {
      await blend();
      // 延遲一點時間讓用戶看到效果
      setTimeout(() => {
        isThicknessChanging.value = false;
      }, 500);
    }, 300);
  }
});

// 監聽風格融合比例調整，即時預覽
watch(alpha, async () => {
  if (imageUrl.value && styleOption.value.length > 0) {
    hasUserAdjusted.value = true;
    
    // 清除之前的計時器
    clearTimeout(debounceTimeout);
    
    // 設置新的計時器，300ms 後執行
    debounceTimeout = setTimeout(async () => {
      await blend();
    }, 300);
  }
});

// 監聽文字變化，觸發預覽更新
watch(character, async () => {
  if (imageUrl.value && character.value.trim()) {
    if (hasUserAdjusted.value && styleOption.value.length > 0) {
      // 如果用戶已經調整過，使用進階模式
      clearTimeout(debounceTimeout);
      debounceTimeout = setTimeout(async () => {
        await blend();
      }, 500);
    } else {
      // 否則顯示原始預覽
      clearTimeout(debounceTimeout);
      debounceTimeout = setTimeout(async () => {
        await generateOriginalPreview();
      }, 500);
    }
  }
});

function toggleTag(option) {
  hasUserAdjusted.value = true;
  
  if (styleOption.value.includes(option)) {
    // 移除選中的標籤
    styleOption.value = styleOption.value.filter(item => item !== option);
  } else {
    // 添加新標籤（只允許單選）
    styleOption.value = [option];
    
    // 如果切換了風格標籤，自動觸發預覽更新
    if (imageUrl.value) {
      setTimeout(() => {
        blend();
      }, 200);
    }
  }
}

// 直接使用原始字型的函數
function proceedWithOriginal() {
  // 這裡可以直接跳轉到下一步或者設置某個標記
  // 暫時先跳轉到相同頁面，實際應用中可能跳轉到結果頁面
  alert('將使用原始字型生成完整字體包！');
  // $router.push('/result'); // 實際的跳轉邏輯
}

// 回到原始字型的函數
function resetToOriginal() {
  // 清除所有選擇和調整
  styleOption.value = [];
  thickness.value = 0;
  alpha.value = 0.5;
  hasUserAdjusted.value = false;
  
  // 重新載入原始預覽
  if (imageUrl.value && character.value.trim()) {
    generateOriginalPreview();
  }
}

// 原始字型預覽函數（不做任何風格調整）
async function generateOriginalPreview() {
  if (!imageUrl.value) return;
  
  isProcessing.value = true;
  
  try {
    const blob = await fetch(imageUrl.value).then((res) => res.blob());
    const form = new FormData();
    form.append("character", character.value);
    // 使用預設風格但設置 alpha = 0 確保不影響原圖
    form.append("style_option", "書法風"); // 使用預設風格以滿足 API 要求
    form.append("alpha", 0); // alpha = 0 表示完全使用原圖，不融合風格
    form.append("thickness", 0); // 不調整粗細
    form.append("image_a", blob, "image_a.png");

    const res = await fetch(`${API_BASE_URL}/ai/blend`, {
      method: "POST",
      body: form,
    });
    
    if (!res.ok) throw new Error("伺服器回應失敗");
    
    const data = await res.json();
    previewImage.value = data.image;
    
    setTimeout(() => {
      isProcessing.value = false;
    }, 500);
    
  } catch (err) {
    isProcessing.value = false;
    console.error("預覽生成失敗", err);
    
    const errorMessages = {
      'Failed to fetch': '網路連線問題，請檢查網路狀態',
      '伺服器回應失敗': 'AI 服務暫時忙碌，請稍後再試',
      default: '預覽生成失敗，請稍後重試'
    };
    
    const message = errorMessages[err.message] || errorMessages.default;
    alert(message);
  }
}

async function blend() {
  // 只有在用戶選擇風格標籤時才執行
  if (!enableBlend.value || !imageUrl.value || styleOption.value.length === 0) return;
  
  hasUserAdjusted.value = true;
  isProcessing.value = true;
  
  try {
    const blob = await fetch(imageUrl.value).then((res) => res.blob());
    const form = new FormData();
    form.append("character", character.value);
    form.append("style_option", styleOption.value[0]);
    form.append("alpha", alpha.value);
    form.append("thickness", thickness.value);
    form.append("image_a", blob, "image_a.png");

    const res = await fetch(`${API_BASE_URL}/ai/blend`, {
      method: "POST",
      body: form,
    });
    
    if (!res.ok) throw new Error("伺服器回應失敗");
    
    const data = await res.json();
    previewImage.value = data.image;
    
    // 成功提示 - 短暫顯示
    setTimeout(() => {
      isProcessing.value = false;
    }, 500);
    
  } catch (err) {
    isProcessing.value = false;
    console.error("融合失敗", err);
    
    // 更友善的錯誤提示
    const errorMessages = {
      'Failed to fetch': '網路連線問題，請檢查網路狀態',
      '伺服器回應失敗': 'AI 服務暫時忙碌，請稍後再試',
      default: '生成失敗，請稍後重試'
    };
    
    const message = errorMessages[err.message] || errorMessages.default;
    alert(message);
  }
}
</script>

<style scoped>
/* 統一色系的滑桿樣式 - 墨綠色版本 */
.range-slider-teal {
  -webkit-appearance: none;
  appearance: none;
  height: 6px;
  border-radius: 6px;
  background: linear-gradient(to right, #e2e8f0, #5EA897);
  outline: none;
  transition: all 0.2s ease;
}

.range-slider-teal::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #5EA897, #3A6B60);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(94, 168, 151, 0.3);
  transition: all 0.2s ease;
}

.range-slider-teal::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 16px rgba(94, 168, 151, 0.4);
}

/* 橘色滑桿 */
.range-slider-orange {
  -webkit-appearance: none;
  appearance: none;
  height: 6px;
  border-radius: 6px;
  background: linear-gradient(to right, #fef3c7, #E29930);
  outline: none;
  transition: all 0.2s ease;
}

.range-slider-orange::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #E29930, #d18825);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(226, 153, 48, 0.3);
  transition: all 0.2s ease;
}

.range-slider-orange::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 16px rgba(226, 153, 48, 0.4);
}

/* Firefox 支援 */
.range-slider-teal::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #5EA897, #3A6B60);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(94, 168, 151, 0.3);
}

.range-slider-teal::-moz-range-track {
  height: 6px;
  border-radius: 6px;
  background: linear-gradient(to right, #e2e8f0, #5EA897);
}

.range-slider-orange::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #E29930, #d18825);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(226, 153, 48, 0.3);
}

.range-slider-orange::-moz-range-track {
  height: 6px;
  border-radius: 6px;
  background: linear-gradient(to right, #fef3c7, #E29930);
}

/* 響應式設計 */
@media (max-width: 1024px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .max-w-7xl {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .grid-cols-1 {
    gap: 1rem;
  }
}

/* 卡片懸停效果 */
.bg-white {
  transition: all 0.2s ease;
}

.bg-white:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

/* 按鈕動畫 */
button {
  transition: all 0.2s ease;
}

/* 輸入框樣式優化 */
input[type="text"] {
  transition: all 0.2s ease;
}

input[type="text"]:focus {
  box-shadow: 0 0 0 3px rgba(226, 153, 48, 0.1);
}
</style>
