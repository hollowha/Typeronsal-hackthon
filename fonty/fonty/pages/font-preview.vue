<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50">
    <!-- Navbar -->
    <Navbar />

    <!-- Header Section -->
    <section class="relative pt-24 pb-8 overflow-hidden">
      <div class="absolute inset-0">
        <div class="absolute top-20 left-1/4 w-96 h-96 bg-gradient-to-br from-orange-100 to-amber-100 rounded-full blur-3xl opacity-40"></div>
        <div class="absolute bottom-20 right-1/4 w-80 h-80 bg-gradient-to-br from-[#3A6B60]/10 to-[#5EA897]/10 rounded-full blur-3xl opacity-25"></div>
      </div>
      
      <div class="relative max-w-7xl mx-auto px-6 text-center">
        <div class="inline-flex items-center gap-3 bg-white/80 backdrop-blur-sm px-6 py-3 rounded-full shadow-lg border border-orange-200/50 mb-8">
          <div class="w-2 h-2 bg-orange-500 rounded-full animate-pulse"></div>
          <span class="text-orange-600 font-semibold text-sm uppercase tracking-wide">Professional Font Studio</span>
        </div>
        <h1 class="text-5xl md:text-6xl font-black text-slate-800 mb-8 bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
          專業字型預覽工坊
        </h1>
        <p class="text-xl md:text-2xl text-slate-600 max-w-4xl mx-auto leading-relaxed mb-12">
          即時調整字型參數，體驗豐富的繁體中文字型，包含多種手寫體風格
        </p>
      </div>
    </section>

    <!-- Main Studio Section -->
    <section class="pb-32 relative">
      <div class="max-w-7xl mx-auto px-6">
        <!-- Main Demo Interface -->
        <div class="bg-white rounded-4xl shadow-2xl border border-slate-100/50 backdrop-blur-xl overflow-hidden">
          <!-- Top Control Bar -->
          <div class="bg-gradient-to-r from-orange-500/5 to-amber-500/5 border-b border-slate-100 px-8 py-6">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div class="flex gap-2">
                  <div class="w-3 h-3 bg-red-400 rounded-full"></div>
                  <div class="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <div class="w-3 h-3 bg-green-400 rounded-full"></div>
                </div>
                <span class="text-slate-600 font-medium">Typersonal Studio</span>
              </div>
              <div class="flex items-center gap-2 bg-slate-100 px-4 py-2 rounded-full">
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span class="text-slate-600 text-sm font-medium">即時預覽</span>
              </div>
            </div>
          </div>

          <div class="p-8 md:p-12">
            <!-- Text Input Section -->
            <div class="mb-12">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-8 h-8 bg-gradient-to-br from-orange-500 to-amber-500 rounded-lg flex items-center justify-center">
                  <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-slate-800">預覽文字</h3>
                </div>
                <!-- 預覽模式切換 -->
                <div class="flex bg-slate-100 rounded-full p-1">
                  <button 
                    @click="previewMode = 'single'"
                    class="px-4 py-2 rounded-full text-sm font-medium transition-all"
                    :class="previewMode === 'single' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500'"
                  >
                    單行
                  </button>
                  <button 
                    @click="previewMode = 'paragraph'"
                    class="px-4 py-2 rounded-full text-sm font-medium transition-all"
                    :class="previewMode === 'paragraph' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500'"
                  >
                    段落
                  </button>
                </div>
              </div>

              <!-- 單行輸入 -->
              <div v-if="previewMode === 'single'">
                <input 
                  v-model="demoText" 
                  type="text" 
                  placeholder="輸入你想要預覽的文字..."
                  class="w-full text-2xl md:text-3xl text-center py-6 px-8 bg-gradient-to-r from-orange-50/50 to-amber-50/50 border-2 border-orange-200/50 rounded-2xl focus:outline-none focus:ring-4 focus:ring-orange-500/20 focus:border-orange-500 transition-all duration-300 hover:border-orange-300/70"
                  maxlength="20"
                >
              </div>

              <!-- 段落輸入 -->
              <div v-else>
                <textarea 
                  v-model="demoText" 
                  placeholder="輸入段落文字來預覽字型在長文本中的效果..."
                  rows="4"
                  class="w-full text-lg text-left py-6 px-8 bg-gradient-to-r from-orange-50/50 to-amber-50/50 border-2 border-orange-200/50 rounded-2xl focus:outline-none focus:ring-4 focus:ring-orange-500/20 focus:border-orange-500 transition-all duration-300 hover:border-orange-300/70 resize-none"
                  maxlength="200"
                ></textarea>
              </div>
            </div>

            <!-- Main Preview Area -->
            <div class="bg-gradient-to-br from-slate-50 to-slate-100/50 rounded-3xl p-8 md:p-12 mb-12 border border-slate-200/50">
              <div class="text-center mb-8">
                <!-- 單行預覽 -->
                <div 
                  v-if="previewMode === 'single'"
                  class="text-6xl md:text-8xl mb-6 transition-all duration-300 select-none cursor-pointer hover:scale-105 font-preview"
                  :style="computedFontStyle"
                >
                  {{ demoText || '繁體字型預覽' }}
                </div>

                <!-- 段落預覽 -->
                <div 
                  v-else
                  class="text-2xl md:text-4xl mb-6 transition-all duration-300 select-none text-left max-w-4xl mx-auto leading-relaxed font-preview"
                  :style="{...computedFontStyle, fontSize: '2rem', lineHeight: lineHeight}"
                >
                  {{ demoText || '這是一段繁體中文的段落預覽文字。通過這段較長的文字，你可以更好地感受字型在實際使用中的效果，包括字符間距、行高以及整體的視覺感受。這對於選擇合適的字型非常重要，特別是在設計海報、書籍或網頁內容時。' }}
                </div>

                <!-- 字型資訊 -->
                <div class="flex flex-wrap items-center justify-center gap-3 text-slate-500">
                  <div class="w-1 h-1 bg-slate-400 rounded-full"></div>
                  <span class="text-sm">{{ selectedFont.name }}</span>
                  <div class="w-1 h-1 bg-slate-400 rounded-full"></div>
                  <span class="text-sm">粗細: {{ fontWeight }}</span>
                  <div class="w-1 h-1 bg-slate-400 rounded-full"></div>
                  <span class="text-sm">字距: {{ letterSpacing.toFixed(2)}}</span>
                  <div class="w-1 h-1 bg-slate-400 rounded-full"></div>
                  <span class="text-sm">行高: {{ lineHeight.toFixed(1)}}</span>
                  <div class="w-1 h-1 bg-slate-400 rounded-full"></div>
                  <span class="text-sm">模式: {{ previewMode === 'single' ? '單行' : '段落' }}</span>
                </div>
              </div>
            </div>

            <!-- Interactive Controls -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <!-- Left: Font Weight & Size Controls -->
              <div class="space-y-6">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-gradient-to-br from-[#5EA897] to-[#3A6B60] rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM15 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4z"/>
                    </svg>
                  </div>
                  <div>
                    <h4 class="font-semibold text-slate-800">字型控制</h4>
                    <p class="text-sm text-slate-500">即時調整字型粗細、大小、間距</p>
                  </div>
                </div>

                <div class="bg-white rounded-2xl p-6 border border-slate-200/50 shadow-sm space-y-6">
                  <!-- 字型粗細 -->
                  <div>
                    <div class="flex items-center justify-between mb-4">
                      <label class="text-sm font-medium text-slate-700">字型粗細</label>
                      <span class="text-sm text-orange-600 font-bold bg-orange-50 px-3 py-1 rounded-full">{{ fontWeight }}</span>
                    </div>
                    <input
                      type="range"
                      min="100"
                      max="900"
                      step="100"
                      v-model.number="fontWeight"
                      class="w-full h-3 bg-gradient-to-r from-slate-200 via-orange-300 to-orange-500 rounded-full appearance-none cursor-pointer slider-thumb-orange"
                    />
                    <div class="flex justify-between text-xs text-slate-400 mt-2">
                      <span>細</span>
                      <span>一般</span>
                      <span>中</span>
                      <span>粗</span>
                      <span>超粗</span>
                    </div>
                  </div>

                  <!-- 字距調整 -->
                  <div>
                    <div class="flex items-center justify-between mb-4">
                      <label class="text-sm font-medium text-slate-700">字符間距</label>
                      <span class="text-sm text-blue-600 font-bold bg-blue-50 px-3 py-1 rounded-full">{{ letterSpacing.toFixed(2) }}em</span>
                    </div>
                    <input
                      type="range"
                      min="-0.1"
                      max="0.5"
                      step="0.01"
                      v-model.number="letterSpacing"
                      class="w-full h-3 bg-gradient-to-r from-slate-200 via-blue-300 to-blue-500 rounded-full appearance-none cursor-pointer slider-thumb-blue"
                    />
                  </div>

                  <!-- 行高調整 -->
                  <div>
                    <div class="flex items-center justify-between mb-4">
                      <label class="text-sm font-medium text-slate-700">行高</label>
                      <span class="text-sm text-purple-600 font-bold bg-purple-50 px-3 py-1 rounded-full">{{ lineHeight }}</span>
                    </div>
                    <input
                      type="range"
                      min="0.8"
                      max="2.0"
                      step="0.1"
                      v-model.number="lineHeight"
                      class="w-full h-3 bg-gradient-to-r from-slate-200 via-purple-300 to-purple-500 rounded-full appearance-none cursor-pointer slider-thumb-purple"
                    />
                  </div>
                </div>
              </div>

              <!-- Right: Font Family Selection -->
              <div class="space-y-6">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                    </svg>
                  </div>
                  <div>
                    <h4 class="font-semibold text-slate-800">字型選擇</h4>
                    <p class="text-sm text-slate-500">豐富的繁體中文字型</p>
                  </div>
                </div>

                <div class="bg-white rounded-2xl p-6 border border-slate-200/50 shadow-sm">
                  <div class="grid grid-cols-1 gap-3 max-h-80 overflow-y-auto font-list">
                    <button 
                      v-for="(font, index) in fontFamilies" 
                      :key="index"
                      @click="selectedFontIndex = index"
                      class="p-4 rounded-xl text-left border-2 transition-all duration-300 hover:shadow-md font-card"
                      :class="selectedFontIndex === index 
                        ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white border-orange-500 shadow-lg' 
                        : 'bg-slate-50 text-slate-700 border-slate-200 hover:border-orange-300 hover:bg-orange-50'"
                    >
                      <div class="flex items-center justify-between">
                        <div class="flex-1 min-w-0">
                          <div class="font-medium mb-1 truncate">{{ font.name }}</div>
                          <div 
                            class="text-lg mb-2 font-preview-text"
                            :style="{ fontFamily: font.css }"
                          >
                            {{ font.preview }}
                          </div>
                          <div class="text-xs opacity-75 truncate">{{ font.description }}</div>
                        </div>
                        <div class="flex-shrink-0 ml-3">
                          <div v-if="font.isHandwriting" class="text-xs px-2 py-1 rounded-full"
                               :class="selectedFontIndex === index ? 'bg-white/20' : 'bg-orange-100 text-orange-600'">
                            手寫體
                          </div>
                        </div>
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Advanced Typography Controls -->
            <div class="bg-white rounded-2xl p-6 border border-slate-200/50 shadow-sm mb-8">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- 文字顏色 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-3">文字顏色</label>
                  <div class="flex gap-2">
                    <button 
                      v-for="color in textColors" 
                      :key="color.name"
                      @click="selectedTextColor = color.value"
                      class="w-8 h-8 rounded-full border-2 transition-all color-selector"
                      :class="selectedTextColor === color.value ? 'border-slate-400 scale-110' : 'border-slate-200'"
                      :style="{ backgroundColor: color.value }"
                      :title="color.name"
                    ></button>
                  </div>
                </div>

                <!-- 文字陰影 -->
                <div>
                  <div class="flex items-center justify-between mb-3">
                    <label class="text-sm font-medium text-slate-700">文字陰影</label>
                    <span class="text-sm text-slate-500">{{ textShadowIntensity }}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    v-model.number="textShadowIntensity"
                    class="w-full h-2 bg-slate-200 rounded-full appearance-none cursor-pointer"
                  />
                </div>

                <!-- 文字轉換 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-3">文字變形</label>
                  <select 
                    v-model="textTransform"
                    class="w-full p-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                  >
                    <option value="none">無</option>
                    <option value="uppercase">全部大寫</option>
                    <option value="lowercase">全部小寫</option>
                    <option value="capitalize">首字母大寫</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Quick Test Samples -->
            <div class="bg-white rounded-2xl p-6 border border-slate-200/50 shadow-sm mb-8">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
                  <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 1.414L10.586 9.5H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <h4 class="font-semibold text-slate-800">快速測試範例</h4>
                  <p class="text-sm text-slate-500">點擊以快速測試常見中文字符</p>
                </div>
              </div>

              <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
                <button 
                  v-for="sample in quickTestSamples" 
                  :key="sample.text"
                  @click="demoText = sample.text; previewMode = sample.mode"
                  class="p-3 bg-slate-50 hover:bg-orange-50 rounded-xl border border-slate-200 hover:border-orange-200 transition-all duration-200 text-left group"
                >
                  <div class="text-lg font-medium text-slate-800 mb-1">{{ sample.text }}</div>
                  <div class="text-xs text-slate-500 group-hover:text-orange-600">{{ sample.description }}</div>
                </button>
              </div>
            </div>

            <!-- Font Comparison Button -->
            <div class="text-center mb-8">
              <button 
                @click="showComparison = !showComparison"
                class="inline-flex items-center gap-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-4 rounded-full font-bold text-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"/>
                </svg>
                字型對比工具
              </button>
            </div>

            <!-- Font Comparison Modal -->
            <div v-if="showComparison" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="showComparison = false">
              <div class="bg-white rounded-3xl max-w-6xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
                <div class="p-8">
                  <div class="flex items-center justify-between mb-8">
                    <div>
                      <h3 class="text-2xl font-bold text-slate-800 mb-2">字型對比工具</h3>
                      <p class="text-slate-600">同時比較兩種字型的視覺效果</p>
                    </div>
                    <button 
                      @click="showComparison = false"
                      class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-full flex items-center justify-center transition-colors"
                    >
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                      </svg>
                    </button>
                  </div>

                  <!-- Comparison Interface -->
                  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <!-- Left Font -->
                    <div class="space-y-6">
                      <div class="text-center">
                        <h4 class="text-lg font-semibold text-slate-800 mb-4">字型 A</h4>
                        <div class="bg-slate-50 rounded-2xl p-8 border border-slate-200">
                          <div 
                            class="text-4xl mb-4 transition-all duration-300"
                            :style="{
                              fontFamily: fontFamilies[comparisonFont1].css,
                              fontWeight: fontWeight,
                              letterSpacing: `${letterSpacing}em`,
                              color: selectedTextColor
                            }"
                          >
                            {{ demoText || '字型對比' }}
                          </div>
                          <div class="text-sm text-slate-500">{{ fontFamilies[comparisonFont1].name }}</div>
                        </div>
                      </div>
                      
                      <div>
                        <label class="block text-sm font-medium text-slate-700 mb-3">選擇字型 A</label>
                        <select 
                          v-model.number="comparisonFont1"
                          class="w-full p-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                        >
                          <option v-for="(font, index) in fontFamilies" :key="index" :value="index">
                            {{ font.name }} - {{ font.description }}
                          </option>
                        </select>
                      </div>
                    </div>

                    <!-- Right Font -->
                    <div class="space-y-6">
                      <div class="text-center">
                        <h4 class="text-lg font-semibold text-slate-800 mb-4">字型 B</h4>
                        <div class="bg-slate-50 rounded-2xl p-8 border border-slate-200">
                          <div 
                            class="text-4xl mb-4 transition-all duration-300"
                            :style="{
                              fontFamily: fontFamilies[comparisonFont2].css,
                              fontWeight: fontWeight,
                              letterSpacing: `${letterSpacing}em`,
                              color: selectedTextColor
                            }"
                          >
                            {{ demoText || '字型對比' }}
                          </div>
                          <div class="text-sm text-slate-500">{{ fontFamilies[comparisonFont2].name }}</div>
                        </div>
                      </div>
                      
                      <div>
                        <label class="block text-sm font-medium text-slate-700 mb-3">選擇字型 B</label>
                        <select 
                          v-model.number="comparisonFont2"
                          class="w-full p-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                        >
                          <option v-for="(font, index) in fontFamilies" :key="index" :value="index">
                            {{ font.name }} - {{ font.description }}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <!-- Comparison Controls -->
                  <div class="mt-8 pt-8 border-t border-slate-200">
                    <div class="text-center mb-6">
                      <h5 class="text-lg font-semibold text-slate-800 mb-4">對比設定</h5>
                      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                          <label class="block text-sm text-slate-600 mb-2">同步字重：{{ fontWeight }}</label>
                          <input
                            type="range"
                            min="100"
                            max="900"
                            step="100"
                            v-model.number="fontWeight"
                            class="w-full"
                          />
                        </div>
                        <div>
                          <label class="block text-sm text-slate-600 mb-2">同步字距：{{ letterSpacing.toFixed(2) }}</label>
                          <input
                            type="range"
                            min="-0.1"
                            max="0.5"
                            step="0.01"
                            v-model.number="letterSpacing"
                            class="w-full"
                          />
                        </div>
                        <div>
                          <label class="block text-sm text-slate-600 mb-2">文字顏色</label>
                          <div class="flex justify-center gap-1">
                            <button 
                              v-for="color in textColors.slice(0, 4)" 
                              :key="color.name"
                              @click="selectedTextColor = color.value"
                              class="w-6 h-6 rounded-full border-2 transition-all"
                              :class="selectedTextColor === color.value ? 'border-slate-400 scale-110' : 'border-slate-200'"
                              :style="{ backgroundColor: color.value }"
                            ></button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"

// 設置頁面元數據
useHead({
  title: 'Typersonal - 專業字型預覽工坊',
  meta: [
    { name: 'description', content: '專業的字型預覽和調整工具，支援豐富的繁體中文字型和手寫體。' },
    { name: 'keywords', content: '字型預覽, 繁體中文字型, 手寫體, 字型調整' }
  ]
})

// 預覽設定
const demoText = ref("繁體字型預覽")
const previewMode = ref('single') // 'single' 或 'paragraph'

// 字型控制
const fontWeight = ref(400)
const letterSpacing = ref(0.1)
const lineHeight = ref(1.2)
const selectedFontIndex = ref(0)
const selectedTextColor = ref('#ea580c')
const textShadowIntensity = ref(30)
const textTransform = ref('none')

// 手寫字型庫 - 簡潔顯示
const fontFamilies = ref([
  {
    name: "手寫風1",
    css: "'Jason Handwriting 1', '華文行楷', cursive",
    preview: "繁體中文預覽",
    description: "經典風格",
    isHandwriting: true
  },
  {
    name: "手寫風2",
    css: "'Jason Handwriting 2', '華文行楷', cursive",
    preview: "繁體中文預覽",
    description: "流暢筆觸",
    isHandwriting: true
  },
  {
    name: "手寫風3",
    css: "'Jason Handwriting 3', '華文行楷', cursive",
    preview: "繁體中文預覽",
    description: "藝術風格",
    isHandwriting: true
  },
  {
    name: "手寫風4",
    css: "'Jason Handwriting 4', '華文行楷', cursive",
    preview: "繁體中文預覽",
    description: "優雅手寫",
    isHandwriting: true
  },
  {
    name: "手寫風5",
    css: "'Jason Handwriting 5', '華文行楷', cursive",
    preview: "繁體中文預覽",
    description: "現代手感",
    isHandwriting: true
  },
  {
    name: "手寫風6",
    css: "'Jason Handwriting 5p', '華文行楷', cursive",
    preview: "繁體中文預覽",
    description: "進階版本",
    isHandwriting: true
  },
  {
    name: "思源黑體",
    css: "'Noto Sans TC', 'Microsoft JhengHei', '微軟正黑體', sans-serif",
    preview: "繁體中文預覽",
    description: "現代無襯線字型",
    isHandwriting: false
  },
  {
    name: "思源宋體",
    css: "'Noto Serif TC', 'Times New Roman', '新細明體', serif",
    preview: "繁體中文預覽",
    description: "優雅襯線字型",
    isHandwriting: false
  },
  {
    name: "微軟正黑體",
    css: "'Microsoft JhengHei', '微軟正黑體', 'Arial', sans-serif",
    preview: "繁體中文預覽",
    description: "Windows 系統字型",
    isHandwriting: false
  },
  {
    name: "標楷體",
    css: "'DFKai-SB', '標楷體', 'Times New Roman', serif",
    preview: "繁體中文預覽",
    description: "系統預設楷體",
    isHandwriting: true
  }
])

// 文字顏色選項
const textColors = ref([
  { name: '橙色', value: '#ea580c' },
  { name: '藍色', value: '#2563eb' },
  { name: '綠色', value: '#059669' },
  { name: '紫色', value: '#9333ea' },
  { name: '紅色', value: '#dc2626' },
  { name: '黃色', value: '#d97706' },
  { name: '灰色', value: '#4b5563' },
  { name: '黑色', value: '#1f2937' }
])

// 快速測試範例
const quickTestSamples = ref([
  { text: '繁體中文', description: '基礎測試', mode: 'single' },
  { text: '你好世界', description: '常用詞彙', mode: 'single' },
  { text: '設計師', description: '專業術語', mode: 'single' },
  { text: '創意靈感', description: '抽象概念', mode: 'single' },
  { text: 'Hello 中文', description: '中英混合', mode: 'single' },
  { text: '2025年', description: '數字測試', mode: 'single' },
  { text: '字型設計是一門結合藝術與技術的專業領域，它要求設計師具備深厚的文字美學素養。', description: '長文本測試', mode: 'paragraph' },
  { text: '臺灣繁體', description: '地區用字', mode: 'single' },
  { text: '書法藝術', description: '傳統文化', mode: 'single' },
  { text: 'AI智慧', description: '現代科技', mode: 'single' },
  { text: '永無島', description: '創意詞彙', mode: 'single' },
  { text: '手寫溫度', description: '情感表達', mode: 'single' }
])

// 字型對比功能
const showComparison = ref(false)
const comparisonFont1 = ref(0) // 思源黑體
const comparisonFont2 = ref(3) // 華康手札體

// 計算當前選中的字型
const selectedFont = computed(() => fontFamilies.value[selectedFontIndex.value])

// 計算完整的字型樣式
const computedFontStyle = computed(() => {
  const shadowIntensity = textShadowIntensity.value / 100
  const shadowBlur = Math.floor(shadowIntensity * 20)
  const shadowOffset = Math.floor(shadowIntensity * 5)
  
  return {
    fontFamily: selectedFont.value.css,
    fontWeight: fontWeight.value,
    letterSpacing: `${letterSpacing.value}em`,
    lineHeight: lineHeight.value,
    color: selectedTextColor.value,
    textTransform: textTransform.value,
    textShadow: shadowIntensity > 0.1 
      ? `${shadowOffset}px ${shadowOffset}px ${shadowBlur}px rgba(0,0,0,0.3)` 
      : 'none',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
  }
})
</script>

<style>
/* 自定義滑桿樣式 */
.slider-thumb-orange::-webkit-slider-thumb {
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ea580c, #fb923c);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
  transition: all 0.2s ease;
}

.slider-thumb-orange::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(234, 88, 12, 0.4);
}

.slider-thumb-orange::-webkit-slider-track {
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(90deg, #fed7aa, #ea580c);
}

.slider-thumb-purple::-webkit-slider-thumb {
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #9333ea, #c084fc);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(147, 51, 234, 0.3);
  transition: all 0.2s ease;
}

.slider-thumb-purple::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(147, 51, 234, 0.4);
}

.slider-thumb-purple::-webkit-slider-track {
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(90deg, #e9d5ff, #9333ea);
}

.slider-thumb-blue::-webkit-slider-thumb {
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #60a5fa);
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
  transition: all 0.2s ease;
}

.slider-thumb-blue::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
}

.slider-thumb-blue::-webkit-slider-track {
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(90deg, #dbeafe, #2563eb);
}

/* 字型預覽區域優化 */
.font-preview {
  word-break: break-all;
  overflow-wrap: break-word;
  hyphens: auto;
}

/* 滾動條優化 */
.font-list::-webkit-scrollbar {
  width: 6px;
}

.font-list::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.font-list::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.font-list::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* 響應式字型卡片 */
@media (max-width: 768px) {
  .font-card {
    padding: 0.75rem;
  }
  
  .font-preview-text {
    font-size: 3rem;
  }
}

/* 顏色選擇器動畫 */
.color-selector {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.color-selector:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>
