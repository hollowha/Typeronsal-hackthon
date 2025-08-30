<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50">
    <!-- Navbar -->
    <Navbar />
    
    <!-- Hero Section -->
    <section class="relative pt-20 md:pt-28 pb-8 md:pb-16">
      <div class="absolute inset-0">
        <div class="absolute top-20 left-1/4 w-96 h-96 bg-gradient-to-br from-[#3A6B60]/10 to-[#5EA897]/10 rounded-full blur-3xl opacity-40"></div>
        <div class="absolute bottom-20 right-1/4 w-80 h-80 bg-gradient-to-br from-orange-100 to-amber-100 rounded-full blur-3xl opacity-30"></div>
      </div>
      
      <div class="relative max-w-7xl mx-auto px-4 md:px-6">
        <div class="text-center mb-8 md:mb-12">
          <h1 class="text-3xl md:text-5xl lg:text-6xl font-bold text-slate-800 mb-4">
            字型市集
          </h1>
          <p class="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed mb-6">
            探索由全球創作者分享的精美字型，找到最適合您的設計風格
          </p>
          
          <!-- Search Bar -->
          <div class="max-w-2xl mx-auto relative">
            <div class="relative">
              <label for="font-search" class="sr-only">搜尋字型</label>
              <input
                id="font-search"
                v-model="searchQuery"
                type="text"
                placeholder="搜尋字型名稱、風格或作者..."
                class="w-full px-6 py-4 pr-14 rounded-2xl border border-gray-200 bg-white/80 backdrop-blur-sm shadow-lg focus:outline-none focus:ring-2 focus:ring-[#3A6B60] focus:border-transparent transition-all duration-300 text-slate-700 placeholder-slate-400 search-input"
                aria-label="搜尋字型"
              />
              <button 
                class="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-[#3A6B60] transition-colors duration-300"
                aria-label="執行搜尋"
                @click="performSearch"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="relative">
      <div class="max-w-7xl mx-auto px-4 md:px-6 pb-16">
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          <!-- Filter Sidebar -->
          <div class="lg:col-span-1">
            <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6 sticky top-24 max-h-[calc(100vh-6rem)] overflow-y-auto custom-scrollbar">
              <!-- Category Filter -->
              <div class="mb-8">
                <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center">
                  <div class="w-2 h-2 bg-[#3A6B60] rounded-full mr-3"></div>
                  分類篩選
                </h3>
                <div class="space-y-2">
                  <button
                    v-for="category in categories"
                    :key="category.name"
                    @click="selectCategory(category.name)"
                    :class="[
                      'w-full text-left px-4 py-3 rounded-xl transition-all duration-200 flex items-center justify-between group focus:outline-none focus:ring-2 focus:ring-[#3A6B60] focus:ring-offset-2',
                      selectedCategory === category.name
                        ? 'bg-gradient-to-r from-[#3A6B60] to-[#5EA897] text-white shadow-lg category-active'
                        : 'hover:bg-slate-50 text-slate-600 hover:text-slate-800'
                    ]"
                    :aria-pressed="selectedCategory === category.name"
                  >
                    <div class="flex items-center">
                      <span class="text-lg mr-3" role="img" :aria-label="category.name">{{ category.icon }}</span>
                      <span class="font-medium">{{ category.name }}</span>
                    </div>
                    <span :class="[
                      'text-xs px-2 py-1 rounded-full',
                      selectedCategory === category.name
                        ? 'bg-white/20 text-white'
                        : 'bg-slate-100 text-slate-500 group-hover:bg-slate-200'
                    ]">
                      {{ getCategoryCount(category.name) }}
                    </span>
                  </button>
                </div>
              </div>
              
              <!-- Style Tags -->
              <div class="mb-8">
                <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center">
                  <div class="w-2 h-2 bg-[#E29930] rounded-full mr-3"></div>
                  風格標籤
                </h3>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="tag in styleTags"
                    :key="tag"
                    @click="toggleTag(tag)"
                    :class="[
                      'px-3 py-2 rounded-full text-sm font-medium transition-all duration-200 border focus:outline-none focus:ring-2 focus:ring-offset-2 tag-chip',
                      selectedTags.includes(tag)
                        ? 'bg-gradient-to-r from-[#E29930] to-[#d18825] text-white border-[#E29930] shadow-md active focus:ring-[#E29930]'
                        : 'bg-white text-slate-600 border-slate-200 hover:border-[#E29930] hover:text-[#E29930] hover:shadow-sm focus:ring-[#E29930]'
                    ]"
                    :aria-pressed="selectedTags.includes(tag)"
                  >
                    {{ tag }}
                  </button>
                </div>
              </div>
              
              <!-- Sort Options -->
              <div>
                <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center">
                  <div class="w-2 h-2 bg-orange-500 rounded-full mr-3"></div>
                  排序方式
                </h3>
                <label for="sort-select" class="sr-only">選擇排序方式</label>
                <select
                  id="sort-select"
                  v-model="sortBy"
                  class="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white focus:outline-none focus:ring-2 focus:ring-[#3A6B60] focus:border-transparent transition-all duration-300 text-slate-700"
                >
                  <option value="latest">最新上傳</option>
                  <option value="popular">最受歡迎</option>
                  <option value="downloads">下載次數</option>
                  <option value="rating">評分排序</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Products Grid -->
          <div class="lg:col-span-3">
            <!-- Results Header -->
            <div class="flex items-center justify-between mb-6">
              <div>
                <p class="text-slate-600">
                  找到 <span class="font-bold text-[#3A6B60]">{{ filteredProducts.length }}</span> 個字型
                  <span v-if="searchQuery" class="text-slate-500">搜尋 "{{ searchQuery }}"</span>
                </p>
              </div>
              <div class="flex items-center gap-3">
                <span class="text-sm text-slate-500">顯示方式:</span>
                <div class="flex bg-white rounded-lg border border-gray-200 p-1">
                  <button
                    @click="viewMode = 'grid'"
                    :class="[
                      'p-2 rounded transition-all duration-200',
                      viewMode === 'grid'
                        ? 'bg-[#3A6B60] text-white'
                        : 'text-slate-400 hover:text-slate-600'
                    ]"
                  >
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
                    </svg>
                  </button>
                  <button
                    @click="viewMode = 'list'"
                    :class="[
                      'p-2 rounded transition-all duration-200',
                      viewMode === 'list'
                        ? 'bg-[#3A6B60] text-white'
                        : 'text-slate-400 hover:text-slate-600'
                    ]"
                  >
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Loading State -->
            <div v-if="isLoading" class="flex items-center justify-center py-20">
              <div class="flex flex-col items-center space-y-4">
                <div class="loading">
                  <div class="w-12 h-12 border-4 border-[#3A6B60] border-t-transparent rounded-full animate-spin"></div>
                </div>
                <p class="text-slate-600">載入中...</p>
              </div>
            </div>

            <!-- Empty State -->
            <div v-else-if="showEmptyState" class="flex flex-col items-center justify-center py-20 text-center">
              <div class="w-24 h-24 bg-gradient-to-br from-slate-100 to-slate-200 rounded-full flex items-center justify-center mb-6">
                <svg class="w-12 h-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
              <h3 class="text-xl font-bold text-slate-800 mb-2">找不到符合條件的字型</h3>
              <p class="text-slate-600 mb-6 max-w-md">
                請嘗試調整搜尋條件、更換關鍵字，或瀏覽其他分類
              </p>
              <div class="flex flex-col sm:flex-row gap-3">
                <button
                  @click="clearAllFilters"
                  class="px-6 py-3 bg-[#3A6B60] text-white rounded-xl font-medium hover:bg-[#2f5951] transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-[#3A6B60] focus:ring-offset-2"
                >
                  清除所有篩選
                </button>
                <button
                  @click="selectCategory('全部')"
                  class="px-6 py-3 border border-[#3A6B60] text-[#3A6B60] rounded-xl font-medium hover:bg-[#3A6B60] hover:text-white transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[#3A6B60] focus:ring-offset-2"
                >
                  瀏覽所有字型
                </button>
              </div>
            </div>

            <!-- Products Grid/List -->
            <div v-else-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              <article
                v-for="product in paginatedProducts"
                :key="product.id"
                class="group bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 cursor-pointer product-card focus-within:ring-2 focus-within:ring-[#3A6B60] focus-within:ring-offset-2"
                @click="viewProduct(product)"
                :aria-labelledby="`product-title-${product.id}`"
                tabindex="0"
                role="button"
                @keydown.enter="viewProduct(product)"
                @keydown.space.prevent="viewProduct(product)"
              >
                <!-- Product Image -->
                <div class="relative aspect-video bg-gradient-to-br from-slate-50 to-slate-100 overflow-hidden">
                  <img
                    :src="product.image"
                    :alt="`${product.title} 字型預覽`"
                    class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    loading="lazy"
                  />
                  <!-- Overlay on hover -->
                  <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <div class="bg-white/90 backdrop-blur-sm rounded-full px-4 py-2">
                      <span class="text-slate-800 font-medium">查看詳情</span>
                    </div>
                  </div>
                  <!-- Category Badge -->
                  <div class="absolute top-3 left-3">
                    <span class="bg-white/90 backdrop-blur-sm text-slate-700 px-3 py-1 rounded-full text-xs font-medium">
                      {{ product.category }}
                    </span>
                  </div>
                  <!-- Favorite Button -->
                  <button 
                    @click.stop="toggleFavorite(product.id)"
                    class="absolute top-3 right-3 p-2 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-colors duration-200 favorite-btn focus:outline-none focus:ring-2 focus:ring-[#3A6B60] focus:ring-offset-2"
                    :aria-label="`${product.isFavorite ? '取消收藏' : '加入收藏'} ${product.title}`"
                    :class="{ active: product.isFavorite }"
                  >
                    <svg 
                      :class="[
                        'w-4 h-4 transition-colors duration-200',
                        product.isFavorite ? 'text-red-500 fill-current' : 'text-slate-400'
                      ]"
                      fill="none" stroke="currentColor" viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                    </svg>
                  </button>
                </div>
                
                <!-- Product Info -->
                <div class="p-6">
                  <div class="flex items-start justify-between mb-3">
                    <h3 
                      :id="`product-title-${product.id}`"
                      class="font-bold text-lg text-slate-800 group-hover:text-[#3A6B60] transition-colors duration-200"
                    >
                      {{ product.title }}
                    </h3>
                    <div class="flex items-center gap-1 text-amber-500" :title="`評分 ${product.rating} 分`">
                      <svg class="w-4 h-4 fill-current star-filled" viewBox="0 0 20 20" aria-hidden="true">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                      </svg>
                      <span class="text-sm font-medium">{{ product.rating }}</span>
                    </div>
                  </div>
                  
                  <p class="text-slate-600 text-sm mb-3">{{ product.description }}</p>
                  
                  <div class="flex items-center justify-between mb-3">
                    <span class="text-slate-500 text-sm">作者：{{ product.author }}</span>
                    <div class="flex items-center gap-1 text-slate-500 text-sm" :title="`下載次數 ${product.downloads}`">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
                      </svg>
                      <span>{{ product.downloads }}</span>
                    </div>
                  </div>
                  
                  <!-- Style Tags -->
                  <div class="flex flex-wrap gap-1 mb-4">
                    <span
                      v-for="tag in product.tags.slice(0, 2)"
                      :key="tag"
                      class="bg-slate-100 text-slate-600 px-2 py-1 rounded text-xs"
                    >
                      {{ tag }}
                    </span>
                    <span v-if="product.tags.length > 2" class="bg-slate-100 text-slate-500 px-2 py-1 rounded text-xs">
                      +{{ product.tags.length - 2 }} 個標籤
                    </span>
                  </div>
                  
                  <!-- Price and Download Button -->
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <span :class="[
                        'text-xl font-bold',
                        (product.price === '免費' || product.price === 'Free') ? 'text-[#5EA897]' : 'text-slate-800'
                      ]">
                        {{ product.price }}
                      </span>
                      <span v-if="product.originalPrice && product.price !== '免費' && product.price !== 'Free'" class="text-sm text-slate-400 line-through">
                        {{ product.originalPrice }}
                      </span>
                    </div>
                    <button 
                      @click.stop="handleDownload(product)"
                      class="bg-gradient-to-r from-[#3A6B60] to-[#5EA897] text-white px-4 py-2 rounded-xl font-medium hover:shadow-lg hover:scale-105 transition-all duration-200 btn-primary focus:outline-none focus:ring-2 focus:ring-[#3A6B60] focus:ring-offset-2"
                      :aria-label="`${(product.price === '免費' || product.price === 'Free') ? '免費下載' : '購買'} ${product.title}`"
                    >
                      {{ (product.price === '免費' || product.price === 'Free') ? '免費下載' : '立即購買' }}
                    </button>
                  </div>
                </div>
              </article>
            </div>

            <!-- List View -->
            <div v-else class="space-y-4">
              <div
                v-for="product in paginatedProducts"
                :key="product.id"
                class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-all duration-300 cursor-pointer"
                @click="viewProduct(product)"
              >
                <div class="flex items-center gap-6">
                  <div class="w-24 h-24 rounded-xl overflow-hidden bg-slate-100 flex-shrink-0">
                    <img :src="product.image" :alt="product.title" class="w-full h-full object-cover">
                  </div>
                  <div class="flex-grow">
                    <div class="flex items-start justify-between mb-2">
                      <h3 class="font-bold text-xl text-slate-800">{{ product.title }}</h3>
                      <div class="flex items-center gap-4">
                        <div class="flex items-center gap-1 text-amber-500">
                          <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                          </svg>
                          <span class="text-sm font-medium">{{ product.rating }}</span>
                        </div>
                        <span :class="[
                          'text-xl font-bold',
                          (product.price === '免費' || product.price === 'Free') ? 'text-[#5EA897]' : 'text-slate-800'
                        ]">
                          {{ product.price }}
                        </span>
                      </div>
                    </div>
                    <p class="text-slate-600 mb-2">{{ product.description }}</p>
                    <div class="flex items-center justify-between">
                      <div class="flex items-center gap-4 text-sm text-slate-500">
                        <span>by {{ product.author }}</span>
                        <span>{{ product.category }}</span>
                        <span>{{ product.downloads }} 下載</span>
                      </div>
                      <button 
                        @click.stop="handleDownload(product)"
                        class="bg-gradient-to-r from-[#3A6B60] to-[#5EA897] text-white px-6 py-2 rounded-xl font-medium hover:shadow-lg hover:scale-105 transition-all duration-200"
                      >
                        {{ (product.price === '免費' || product.price === 'Free') ? '免費下載' : '立即購買' }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="flex justify-center mt-12">
              <div class="flex items-center gap-2">
                <button
                  @click="currentPage = Math.max(1, currentPage - 1)"
                  :disabled="currentPage === 1"
                  class="px-4 py-2 rounded-xl border border-gray-200 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  上一頁
                </button>
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="currentPage = page"
                  :class="[
                    'px-4 py-2 rounded-xl font-medium transition-all duration-200',
                    currentPage === page
                      ? 'bg-[#3A6B60] text-white shadow-lg'
                      : 'border border-gray-200 text-slate-600 hover:bg-slate-50'
                  ]"
                >
                  {{ page }}
                </button>
                <button
                  @click="currentPage = Math.min(totalPages, currentPage + 1)"
                  :disabled="currentPage === totalPages"
                  class="px-4 py-2 rounded-xl border border-gray-200 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  下一頁
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 通知系統 -->
    <div class="fixed top-4 right-4 z-50 space-y-2">
      <transition-group name="notification" tag="div">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="[
            'max-w-sm bg-white rounded-lg shadow-lg border-l-4 p-4 transition-all duration-300',
            {
              'border-green-500': notification.type === 'success',
              'border-red-500': notification.type === 'error',
              'border-blue-500': notification.type === 'info',
              'border-yellow-500': notification.type === 'warning'
            },
            notification.show ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-full'
          ]"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div :class="[
                'flex-shrink-0 w-5 h-5 mr-3',
                {
                  'text-green-500': notification.type === 'success',
                  'text-red-500': notification.type === 'error',
                  'text-blue-500': notification.type === 'info',
                  'text-yellow-500': notification.type === 'warning'
                }
              ]">
                <svg v-if="notification.type === 'success'" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <svg v-else-if="notification.type === 'error'" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                </svg>
                <svg v-else-if="notification.type === 'warning'" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                </svg>
                <svg v-else fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                </svg>
              </div>
              <p class="text-sm text-gray-700">{{ notification.message }}</p>
            </div>
            <button
              @click="removeNotification(notification.id)"
              class="ml-4 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";

// SEO Meta
useSeoMeta({
  title: 'Typersonal - 字型市集',
  description: '探索由全球創作者分享的精美字型，找到最適合您的設計風格'
})

// State Management
const searchQuery = ref('')
const selectedCategory = ref('全部')
const selectedTags = ref([])
const sortBy = ref('latest')
const viewMode = ref('grid')
const currentPage = ref(1)
const itemsPerPage = 12
const isLoading = ref(false)
const showEmptyState = computed(() => 
  !isLoading.value && filteredProducts.value.length === 0
)

// Categories with icons and enhanced data
const categories = [
  { name: '全部', icon: '🌟' },
  { name: '現代風格', icon: '✨' },
  { name: '經典復古', icon: '📜' },
  { name: '手寫風格', icon: '✍️' },
  { name: '藝術創意', icon: '🎨' },
  { name: '商業實用', icon: '💼' },
  { name: '裝飾字型', icon: '🎭' },
  { name: '中文字型', icon: '🀄' }
]

// Style tags
const styleTags = [
  '簡約', '優雅', '粗體', '細體', '圓體', '方體', 
  '手繪', '書法', '現代', '復古', '可愛', '正式',
  '創意', '藝術', '商務', '標題', '內文', '裝飾'
]

// Enhanced products data - 保留原本產品並新增可下載字體
const products = [
  // 原本的產品 (保留)
  {
    id: 1,
    title: "Elegant Modern",
    image: "/image1.png",
    price: "Free",
    originalPrice: null,
    category: "現代風格",
    author: "張設計師",
    rating: 4.8,
    downloads: "12.5k",
    description: "優雅的現代字型，適合各種設計場景",
    tags: ["現代", "優雅", "簡約", "標題"],
    isFavorite: false,
    uploadDate: "2024-12-01",
    popularity: 95,
    fontFile: null,
    fileName: null
  },
  {
    id: 2,
    title: "Classic Script",
    image: "/image2.png",
    price: "$15",
    originalPrice: "$25",
    category: "手寫風格",
    author: "李創作者",
    rating: 4.9,
    downloads: "8.3k",
    description: "經典的手寫風格字型，帶有溫暖的人文氣息",
    tags: ["手寫", "經典", "溫暖", "內文"],
    isFavorite: true,
    uploadDate: "2024-11-28",
    popularity: 88,
    fontFile: null,
    fileName: null
  },
  {
    id: 3,
    title: "Bold Display",
    image: "/image3.png",
    price: "$12",
    originalPrice: "$20",
    category: "商業實用",
    author: "王字體工作室",
    rating: 4.7,
    downloads: "15.2k",
    description: "粗體展示字型，完美的標題選擇",
    tags: ["粗體", "標題", "商務", "現代"],
    isFavorite: false,
    uploadDate: "2024-12-02",
    popularity: 92,
    fontFile: null,
    fileName: null
  },
  {
    id: 4,
    title: "Retro Vintage",
    image: "/image1.png",
    price: "Free",
    originalPrice: null,
    category: "經典復古",
    author: "復古設計社",
    rating: 4.6,
    downloads: "6.7k",
    description: "復古風格字型，重現黃金時代的設計美學",
    tags: ["復古", "經典", "裝飾", "藝術"],
    isFavorite: false,
    uploadDate: "2024-11-25",
    popularity: 75,
    fontFile: null,
    fileName: null
  },
  {
    id: 5,
    title: "Cute Rounded",
    image: "/image2.png",
    price: "$8",
    originalPrice: "$15",
    category: "裝飾字型",
    author: "可愛字型屋",
    rating: 4.5,
    downloads: "9.1k",
    description: "可愛的圓體字型，適合兒童相關設計",
    tags: ["可愛", "圓體", "兒童", "活潑"],
    isFavorite: true,
    uploadDate: "2024-11-30",
    popularity: 81,
    fontFile: null,
    fileName: null
  },
  {
    id: 6,
    title: "Artistic Brush",
    image: "/image3.png",
    price: "$18",
    originalPrice: null,
    category: "藝術創意",
    author: "筆觸藝術家",
    rating: 4.9,
    downloads: "4.2k",
    description: "藝術筆觸字型，每一筆都充滿創意靈感",
    tags: ["藝術", "筆觸", "創意", "手繪"],
    isFavorite: false,
    uploadDate: "2024-12-03",
    popularity: 67,
    fontFile: null,
    fileName: null
  },
  {
    id: 7,
    title: "Chinese Calligraphy",
    image: "/image1.png",
    price: "Free",
    originalPrice: null,
    category: "中文字型",
    author: "書法大師",
    rating: 4.8,
    downloads: "18.9k",
    description: "傳統中文書法字型，傳承千年文化精髓",
    tags: ["書法", "中文", "傳統", "文化"],
    isFavorite: false,
    uploadDate: "2024-11-20",
    popularity: 98,
    fontFile: null,
    fileName: null
  },
  {
    id: 8,
    title: "Business Sans",
    image: "/image2.png",
    price: "$10",
    originalPrice: "$16",
    category: "商業實用",
    author: "商業字型公司",
    rating: 4.7,
    downloads: "22.1k",
    description: "專業的商業無襯線字型，適合企業品牌使用",
    tags: ["商務", "無襯線", "專業", "品牌"],
    isFavorite: true,
    uploadDate: "2024-11-22",
    popularity: 94,
    fontFile: null,
    fileName: null
  },
  
  // 新增的可下載 Jason Handwriting 字體
  {
    id: 9,
    title: "Jason Handwriting 1",
    image: "/image1.png",
    price: "免費",
    originalPrice: null,
    category: "手寫風格",
    author: "Jason 設計師",
    rating: 4.8,
    downloads: "3.2k",
    description: "優雅的手寫字型，適合各種設計場景",
    tags: ["手寫", "優雅", "簡約", "標題"],
    isFavorite: false,
    uploadDate: "2024-12-05",
    popularity: 85,
    fontFile: "/fonts/JasonHandwriting1.woff2",
    fileName: "JasonHandwriting1.woff2"
  },
  {
    id: 10,
    title: "Jason Handwriting 2",
    image: "/image2.png",
    price: "免費",
    originalPrice: null,
    category: "手寫風格",
    author: "Jason 設計師",
    rating: 4.7,
    downloads: "2.8k",
    description: "經典的手寫風格字型，帶有溫暖的人文氣息",
    tags: ["手寫", "經典", "溫暖", "內文"],
    isFavorite: false,
    uploadDate: "2024-12-05",
    popularity: 82,
    fontFile: "/fonts/JasonHandwriting2.woff2",
    fileName: "JasonHandwriting2.woff2"
  },
  {
    id: 11,
    title: "Jason Handwriting 3",
    image: "/image3.png",
    price: "免費",
    originalPrice: null,
    category: "手寫風格",
    author: "Jason 設計師",
    rating: 4.6,
    downloads: "3.5k",
    description: "粗體手寫字型，完美的標題選擇",
    tags: ["手寫", "標題", "粗體", "現代"],
    isFavorite: false,
    uploadDate: "2024-12-05",
    popularity: 78,
    fontFile: "/fonts/JasonHandwriting3.woff2",
    fileName: "JasonHandwriting3.woff2"
  },
  {
    id: 12,
    title: "Jason Handwriting 4",
    image: "/image1.png",
    price: "免費",
    originalPrice: null,
    category: "手寫風格",
    author: "Jason 設計師",
    rating: 4.5,
    downloads: "2.1k",
    description: "復古風格手寫字型，重現黃金時代的設計美學",
    tags: ["手寫", "復古", "裝飾", "藝術"],
    isFavorite: false,
    uploadDate: "2024-12-05",
    popularity: 74,
    fontFile: "/fonts/JasonHandwriting4.woff2",
    fileName: "JasonHandwriting4.woff2"
  },
  {
    id: 13,
    title: "Jason Handwriting 5",
    image: "/image2.png",
    price: "免費",
    originalPrice: null,
    category: "手寫風格",
    author: "Jason 設計師",
    rating: 4.7,
    downloads: "2.9k",
    description: "可愛的手寫字型，適合兒童相關設計",
    tags: ["手寫", "可愛", "兒童", "活潑"],
    isFavorite: false,
    uploadDate: "2024-12-05",
    popularity: 80,
    fontFile: "/fonts/JasonHandwriting5.woff2",
    fileName: "JasonHandwriting5.woff2"
  },
  {
    id: 14,
    title: "Jason Handwriting 5 Plus",
    image: "/image3.png",
    price: "免費",
    originalPrice: null,
    category: "手寫風格",
    author: "Jason 設計師",
    rating: 4.8,
    downloads: "1.8k",
    description: "進階手寫字型，每一筆都充滿創意靈感",
    tags: ["手寫", "筆觸", "創意", "進階"],
    isFavorite: false,
    uploadDate: "2024-12-05",
    popularity: 76,
    fontFile: "/fonts/JasonHandwriting5p.woff2",
    fileName: "JasonHandwriting5p.woff2"
  }
]

// Methods
const selectCategory = (category) => {
  selectedCategory.value = category
  currentPage.value = 1
}

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tag)
  }
  currentPage.value = 1
}

const toggleFavorite = (id) => {
  const product = products.find(p => p.id === id)
  if (product) {
    product.isFavorite = !product.isFavorite
    // 這裡可以添加 API 調用來保存收藏狀態
    console.log(`${product.isFavorite ? '已收藏' : '已取消收藏'}: ${product.title}`)
  }
}

const viewProduct = (product) => {
  // 這裡可以導航到產品詳情頁面
  console.log('View product:', product.title)
  // 未來可以使用 navigateTo(`/market/${product.id}`)
}

const handleDownload = async (product) => {
  if ((product.price === '免費' || product.price === 'Free') && product.fontFile) {
    try {
      // 增加下載次數
      const currentDownloads = parseFloat(product.downloads.replace('k', '')) * 1000
      product.downloads = `${((currentDownloads + 1) / 1000).toFixed(1)}k`
      
      // 創建下載鏈接
      const link = document.createElement('a')
      link.href = product.fontFile
      link.download = product.fileName
      link.target = '_blank'
      
      // 觸發下載
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      // 顯示成功訊息
      showNotification(`正在下載 ${product.title}...`, 'success')
      
      console.log('開始下載免費字型:', product.title)
    } catch (error) {
      console.error('下載錯誤:', error)
      showNotification('下載失敗，請稍後再試', 'error')
    }
  } else if (product.price !== '免費' && product.price !== 'Free') {
    // 處理付費購買
    console.log('開始購買流程:', product.title)
    showNotification('即將導向購買頁面...', 'info')
    // 這裡可以導航到購買頁面或打開購買彈窗
  } else {
    showNotification('此字型暫時無法下載', 'warning')
  }
}

// 通知系統
const notifications = ref([])

const showNotification = (message, type = 'info') => {
  const id = Date.now()
  const notification = {
    id,
    message,
    type,
    show: true
  }
  
  notifications.value.push(notification)
  
  // 3秒後自動移除通知
  setTimeout(() => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value[index].show = false
      setTimeout(() => {
        notifications.value.splice(index, 1)
      }, 300)
    }
  }, 3000)
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value[index].show = false
    setTimeout(() => {
      notifications.value.splice(index, 1)
    }, 300)
  }
}

const performSearch = () => {
  // 執行搜尋邏輯
  if (searchQuery.value.trim()) {
    console.log('搜尋:', searchQuery.value)
    currentPage.value = 1
  }
}

const clearAllFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = '全部'
  selectedTags.value = []
  sortBy.value = 'latest'
  currentPage.value = 1
}

// Computed Properties
const filteredProducts = computed(() => {
  let filtered = [...products] // 創建副本以避免修改原始數據

  // Filter by search query with improved performance
  if (searchQuery.value?.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    const queryTerms = query.split(/\s+/) // 支援多關鍵字搜尋
    
    filtered = filtered.filter(product => {
      const searchText = [
        product.title,
        product.author,
        product.description,
        product.category,
        ...product.tags
      ].join(' ').toLowerCase()
      
      return queryTerms.every(term => searchText.includes(term))
    })
  }

  // Filter by category
  if (selectedCategory.value && selectedCategory.value !== '全部') {
    filtered = filtered.filter(product => product.category === selectedCategory.value)
  }

  // Filter by tags
  if (selectedTags.value.length > 0) {
    filtered = filtered.filter(product =>
      selectedTags.value.some(tag => product.tags.includes(tag))
    )
  }

  // Sort products with improved logic
  const sortFunctions = {
    latest: (a, b) => new Date(b.uploadDate) - new Date(a.uploadDate),
    popular: (a, b) => b.popularity - a.popularity,
    downloads: (a, b) => {
      const parseDownloads = (str) => {
        const num = parseFloat(str.replace('k', ''))
        return str.includes('k') ? num * 1000 : num
      }
      return parseDownloads(b.downloads) - parseDownloads(a.downloads)
    },
    rating: (a, b) => b.rating - a.rating
  }

  if (sortFunctions[sortBy.value]) {
    filtered.sort(sortFunctions[sortBy.value])
  }

  return filtered
})

const getCategoryCount = (categoryName) => {
  if (categoryName === '全部') return products.length
  return products.filter(product => product.category === categoryName).length
}

const totalPages = computed(() => {
  return Math.ceil(filteredProducts.value.length / itemsPerPage)
})

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredProducts.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value

  // Always show first page
  if (total > 0) pages.push(1)

  // Show pages around current page
  for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
    if (!pages.includes(i)) pages.push(i)
  }

  // Always show last page if there are multiple pages
  if (total > 1 && !pages.includes(total)) pages.push(total)

  return pages.sort((a, b) => a - b)
})

// Keyboard shortcuts
const handleKeydown = (event) => {
  // Ctrl/Cmd + K to focus search
  if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
    event.preventDefault()
    document.getElementById('font-search')?.focus()
  }
  
  // Escape to clear search when focused on search input
  if (event.key === 'Escape' && document.activeElement?.id === 'font-search') {
    searchQuery.value = ''
  }
  
  // Arrow keys for pagination
  if (!event.target.closest('input, select, button')) {
    if (event.key === 'ArrowLeft' && currentPage.value > 1) {
      currentPage.value--
    } else if (event.key === 'ArrowRight' && currentPage.value < totalPages.value) {
      currentPage.value++
    }
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Custom scrollbar for filter sidebar */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 2px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Enhanced card hover animations */
.product-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Search input focus styles */
.search-input:focus {
  transform: scale(1.01);
  box-shadow: 0 0 0 3px rgba(88, 168, 151, 0.1);
}

/* Category active state */
.category-active {
  background: linear-gradient(135deg, #58a897 0%, #3a6b60 100%);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(58, 107, 96, 0.2);
}

/* Tag chips animation */
.tag-chip {
  transition: all 0.2s ease-in-out;
}

.tag-chip:hover {
  transform: scale(1.05);
}

.tag-chip.active {
  background: linear-gradient(135deg, #e29930 0%, #d97706 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(226, 153, 48, 0.3);
}

/* Rating stars */
.star-filled {
  color: #fbbf24;
}

.star-empty {
  color: #d1d5db;
}

/* Price badge styles */
.price-badge {
  background: linear-gradient(135deg, #58a897 0%, #3a6b60 100%);
  color: white;
  font-weight: 600;
}

.free-badge {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

/* Favorite heart animation */
.favorite-btn {
  transition: all 0.2s ease-in-out;
}

.favorite-btn.active {
  color: #ef4444;
  transform: scale(1.1);
}

.favorite-btn:hover {
  transform: scale(1.1);
}

/* View mode toggle */
.view-toggle.active {
  background: #58a897;
  color: white;
}

/* Pagination styles */
.pagination-btn {
  transition: all 0.2s ease-in-out;
}

.pagination-btn:hover {
  background: #f1f5f9;
  transform: translateY(-1px);
}

.pagination-btn.active {
  background: #58a897;
  color: white;
  box-shadow: 0 2px 4px rgba(88, 168, 151, 0.3);
}

/* Hero section gradient */
.hero-gradient {
  background: linear-gradient(135deg, #58a897 0%, #3a6b60 100%);
}

/* Loading animation */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Improved focus states */
*:focus {
  outline: none;
}

button:focus-visible,
input:focus-visible,
select:focus-visible {
  outline: 2px solid #3A6B60;
  outline-offset: 2px;
}

/* Smooth transitions for all interactive elements */
button, input, select, [role="button"] {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Filter sidebar slide animation */
.filter-sidebar {
  transition: transform 0.3s ease-in-out;
}

/* Responsive grid adjustments */
@media (max-width: 640px) {
  .mobile-grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 641px) and (max-width: 1024px) {
  .tablet-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1025px) {
  .desktop-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* List view specific styles */
.list-item {
  transition: all 0.2s ease-in-out;
}

.list-item:hover {
  background: #f8fafc;
  border-color: #58a897;
}

/* Notification animations */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}

/* Download button pulse animation */
@keyframes download-pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(58, 107, 96, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(58, 107, 96, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(58, 107, 96, 0);
  }
}

.btn-primary:active {
  animation: download-pulse 0.6s ease-out;
}

.btn-secondary {
  border: 1px solid #58a897;
  color: #58a897;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #58a897;
  color: white;
  transform: translateY(-1px);
}
</style>
