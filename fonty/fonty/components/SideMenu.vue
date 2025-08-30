<template>
  <div class="side-menu">
    <!-- Header Section -->
    <div class="menu-header">
      <div class="close-button-area">
        <button @click="$emit('close')" class="close-btn">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      
      <!-- Brand Section -->
      <div class="brand-section">
        <div class="brand-icon">
          <img src="/typersonal2.png" alt="Typersonal Logo" class="w-10 h-10 object-contain" />
        </div>
        <h2 class="brand-title">
          <span class="text-[#E29930]">Type</span>
          <span class="text-[#3A6B60]">rsonal</span>
        </h2>
      </div>
    </div>

    <!-- Navigation Section -->
    <nav class="menu-nav">
      <div class="nav-section">
        <h3 class="nav-section-title">主要功能</h3>
        <div class="nav-items">
          <NuxtLink 
            v-for="item in mainNavItems" 
            :key="item.path" 
            :to="item.path" 
            @click="$emit('close')"
            class="nav-item"
          >
            <div class="nav-item-icon">
              <component :is="item.icon" class="w-5 h-5" />
            </div>
            <span class="nav-item-text">{{ item.name }}</span>
            <div class="nav-item-arrow">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </div>
          </NuxtLink>
        </div>
      </div>

      <div class="nav-section">
        <h3 class="nav-section-title">工具</h3>
        <div class="nav-items">
          <NuxtLink 
            v-for="item in toolNavItems" 
            :key="item.path" 
            :to="item.path" 
            @click="$emit('close')"
            class="nav-item"
          >
            <div class="nav-item-icon">
              <component :is="item.icon" class="w-5 h-5" />
            </div>
            <span class="nav-item-text">{{ item.name }}</span>
            <div class="nav-item-arrow">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </div>
          </NuxtLink>
        </div>
      </div>
    </nav>

    <!-- Footer Section -->
    <div class="menu-footer">
      <div class="footer-info">
        <p class="text-sm text-gray-500">版本 1.0.0</p>
        <p class="text-xs text-gray-400">© 2024 Typersonal</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineComponent } from 'vue'

// Define custom icons as proper Vue components
const HomeIcon = defineComponent({
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>`
})

const CreateIcon = defineComponent({
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>`
})

const MarketIcon = defineComponent({
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l-1 12H6L5 9z"></path></svg>`
})

const UploadIcon = defineComponent({
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>`
})

const TestIcon = defineComponent({
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>`
})

const mainNavItems = ref([
  { name: '首頁', path: '/', icon: HomeIcon },
  { name: '模板應用', path: '/template', icon: CreateIcon },
  { name: '字型工坊', path: '/workshop', icon: CreateIcon },
  { name: '字型市集', path: '/market', icon: MarketIcon }
])

const toolNavItems = ref([
  { name: '字型工坊', path: '/workshop', icon: UploadIcon },
  { name: '測試頁面', path: '/test', icon: TestIcon },
  { name: '模板', path: '/template', icon: CreateIcon }
])
</script>

<style scoped>
.side-menu {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px) saturate(180%);
  border-left: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: -10px 0 50px rgba(0, 0, 0, 0.1);
  width: 320px;
  overflow: hidden;
}

/* Header Section */
.menu-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(58, 107, 96, 0.1);
  background: linear-gradient(135deg, rgba(248, 243, 234, 0.5), rgba(255, 255, 255, 0.8));
}

.close-button-area {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.close-btn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.close-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
}

.brand-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(58, 107, 96, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(58, 107, 96, 0.15);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.brand-icon:hover {
  transform: scale(1.05);
  border-color: rgba(58, 107, 96, 0.3);
  box-shadow: 0 12px 35px rgba(58, 107, 96, 0.25);
}

.brand-title {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.025em;
}

/* Navigation Section */
.menu-nav {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(58, 107, 96, 0.3) transparent;
}

.menu-nav::-webkit-scrollbar {
  width: 4px;
}

.menu-nav::-webkit-scrollbar-track {
  background: transparent;
}

.menu-nav::-webkit-scrollbar-thumb {
  background: rgba(58, 107, 96, 0.3);
  border-radius: 2px;
}

.menu-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(58, 107, 96, 0.5);
}

.nav-section {
  margin-bottom: 32px;
}

.nav-section:last-child {
  margin-bottom: 0;
}

.nav-section-title {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #6B7280;
  margin-bottom: 12px;
  padding: 0 8px;
}

.nav-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  color: #374151;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  border: 1px solid transparent;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #3A6B60, #5EA897);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-item:hover::before {
  opacity: 0.08;
}

.nav-item:hover {
  transform: translateX(4px);
  border-color: rgba(58, 107, 96, 0.2);
  box-shadow: 0 4px 12px rgba(58, 107, 96, 0.15);
}

.nav-item.router-link-active {
  background: rgba(58, 107, 96, 0.1);
  color: #3A6B60;
  border-color: rgba(58, 107, 96, 0.3);
  font-weight: 600;
}

.nav-item.router-link-active::before {
  opacity: 0.1;
}

.nav-item-icon {
  position: relative;
  z-index: 1;
  color: #6B7280;
  transition: color 0.3s ease;
}

.nav-item:hover .nav-item-icon,
.nav-item.router-link-active .nav-item-icon {
  color: #3A6B60;
}

.nav-item-text {
  position: relative;
  z-index: 1;
  flex: 1;
  font-size: 0.95rem;
}

.nav-item-arrow {
  position: relative;
  z-index: 1;
  color: #9CA3AF;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s ease;
}

.nav-item:hover .nav-item-arrow {
  opacity: 1;
  transform: translateX(0);
  color: #3A6B60;
}

/* Footer Section */
.menu-footer {
  padding: 20px;
  border-top: 1px solid rgba(58, 107, 96, 0.1);
  background: linear-gradient(135deg, rgba(248, 243, 234, 0.3), rgba(255, 255, 255, 0.6));
}

.footer-info {
  text-align: center;
}

.footer-info p {
  margin: 4px 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .side-menu {
    width: 100vw;
  }
  
  .brand-title {
    font-size: 1.25rem;
  }
  
  .nav-item {
    padding: 12px 14px;
  }
}

/* Enhanced Animations */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.side-menu {
  animation: slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.nav-item {
  animation: fadeInUp 0.5s ease forwards;
  opacity: 0;
}

.nav-item:nth-child(1) { animation-delay: 0.1s; }
.nav-item:nth-child(2) { animation-delay: 0.15s; }
.nav-item:nth-child(3) { animation-delay: 0.2s; }
.nav-item:nth-child(4) { animation-delay: 0.25s; }
.nav-item:nth-child(5) { animation-delay: 0.3s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Focus states for accessibility */
.nav-item:focus,
.close-btn:focus {
  outline: 2px solid #E29930;
  outline-offset: 2px;
}

/* Hover effects enhancement */
.nav-item:hover {
  background: rgba(255, 255, 255, 0.8);
}

/* Loading state */
.nav-item.loading {
  pointer-events: none;
  opacity: 0.6;
}

.nav-item.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 16px;
  width: 16px;
  height: 16px;
  border: 2px solid #3A6B60;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  transform: translateY(-50%);
}

@keyframes spin {
  to {
    transform: translateY(-50%) rotate(360deg);
  }
}
</style>
