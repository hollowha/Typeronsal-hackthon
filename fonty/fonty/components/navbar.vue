<template>
  <div class="fixed top-0 left-0 right-0 z-40">
    <!-- Glassmorphism Navbar -->
    <nav class="backdrop-blur-md bg-white/80 border-b border-white/20 shadow-lg transition-all duration-300" :class="{ 'nav-scrolled': isScrolled, 'shrinked-nav': isSideMenuOpen }">
      <div class="flex h-14 md:h-16 lg:h-20 items-center justify-between px-3 md:px-6 lg:px-12 transition-all duration-700">
        <!-- Left Side: Enhanced Logo -->
        <NuxtLink to="/" class="group">
          <div class="flex items-center gap-1.5 sm:gap-1.5 md:gap-2 lg:gap-3 transition-all duration-300 hover:scale-105">
            <!-- Clean Logo Icon -->
            <div class="relative h-full flex items-center">
              <img src="/typersonal2.png" alt="Typersonal Logo" class="h-full w-auto object-contain transition-transform duration-300 group-hover:scale-110 max-h-10 sm:max-h-8 md:max-h-10 lg:max-h-12" />
            </div>
            
            <!-- Enhanced Brand Name - Hidden on mobile -->
            <div class="logo-text hidden sm:block">
              <h1 class="text-base md:text-xl lg:text-2xl xl:text-3xl font-black tracking-tight">
                <span class="text-[#E29930] group-hover:text-[#d48826] transition-colors duration-300">Type</span>
                <span class="bg-gradient-to-r from-[#3A6B60] to-[#5EA897] bg-clip-text text-transparent">rsonal</span>
              </h1>
              <div class="h-0.5 bg-gradient-to-r from-[#E29930] to-transparent rounded-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></div>
            </div>
          </div>
        </NuxtLink>

        <!-- Center Navigation Links (Hidden on mobile) -->
        <div class="hidden lg:flex items-center space-x-8">
          <NuxtLink v-for="link in navLinks" :key="link.path" :to="link.path" 
                    class="nav-link relative px-4 py-2 text-[#3A6B60] font-medium transition-all duration-300 hover:text-[#E29930] group">
            {{ link.name }}
            <div class="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-[#E29930] to-[#5EA897] rounded-full transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
          </NuxtLink>
        </div>

        <!-- Right Side: Enhanced Auth and Menu -->
        <div class="flex items-center gap-2 md:gap-4">
          <!-- Enhanced Auth Component -->
          <div class="auth-wrapper scale-90 md:scale-100">
            <AuthComponent />
          </div>
          
          <!-- Enhanced Menu Button -->
          <button
            @click="toggleMenu"
            class="menu-button relative p-2 md:p-3 rounded-full transition-all duration-300 hover:bg-white/20 group"
            :class="{ 'menu-active': isSideMenuOpen }"
          >
            <div class="menu-icon">
              <span class="menu-line top"></span>
              <span class="menu-line middle"></span>
              <span class="menu-line bottom"></span>
            </div>
          </button>
        </div>
      </div>
      
      <!-- Animated Border -->
      <div class="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#E29930]/30 to-transparent"></div>
    </nav>
    <!-- Enhanced Overlay with Blur Effect -->
    <transition name="fade">
      <div v-if="isSideMenuOpen" class="overlay backdrop-blur-sm" @click="closeMenu"></div>
    </transition>
    
    <!-- Enhanced Side Menu -->
    <transition name="slide">
      <SideMenu
        class="fixed right-0 top-0 z-50 flex h-full bg-white/95 backdrop-blur-lg px-6 py-6 shadow-2xl border-l border-white/20"
        v-if="isSideMenuOpen"
        @close="isSideMenuOpen = false"
      />
    </transition>
  </div>
  
  <!-- Spacer for Fixed Navbar -->
  <div class="h-14 md:h-16 lg:h-20"></div>
  <slot />
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

const isSideMenuOpen = ref(false);
const isScrolled = ref(false);

// Navigation Links
const navLinks = ref([
  { name: '首頁', path: '/' },
  { name: '字訂藝', path: '/workshop' },
  { name: '模板', path: '/template' },
  { name: '市集', path: '/market' }
  
]);

const toggleMenu = () => {
  isSideMenuOpen.value = !isSideMenuOpen.value;
};

const closeMenu = () => {
  isSideMenuOpen.value = false;
};

// Scroll detection for navbar styling
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  handleScroll(); // Check initial scroll position
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

// Close menu when clicking outside or pressing Escape
const handleKeydown = (e) => {
  if (e.key === 'Escape' && isSideMenuOpen.value) {
    closeMenu();
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
});
</script>

<style scoped>
/* Enhanced Navbar Styles */
.shrinked-nav {
  width: 80vw;
  transform: translateX(20vw);
}

.nav-scrolled {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

/* Logo Animation */
.logo-text {
  position: relative;
}

/* Navigation Links */
.nav-link {
  position: relative;
  font-weight: 500;
  letter-spacing: 0.025em;
}

.nav-link:hover {
  transform: translateY(-1px);
}

/* Enhanced Menu Button */
.menu-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(58, 107, 96, 0.1), rgba(94, 168, 151, 0.1));
  border: 1px solid rgba(58, 107, 96, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@media (min-width: 768px) {
  .menu-button {
    width: 48px;
    height: 48px;
  }
}

.menu-button:hover {
  background: linear-gradient(135deg, rgba(58, 107, 96, 0.2), rgba(94, 168, 151, 0.2));
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(58, 107, 96, 0.15);
}

/* Animated Menu Icon */
.menu-icon {
  width: 16px;
  height: 12px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

@media (min-width: 768px) {
  .menu-icon {
    width: 20px;
    height: 14px;
  }
}

.menu-line {
  height: 2px;
  background: linear-gradient(90deg, #3A6B60, #5EA897);
  border-radius: 1px;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  transform-origin: center;
}

.menu-line.top {
  width: 100%;
}

.menu-line.middle {
  width: 80%;
  align-self: center;
}

.menu-line.bottom {
  width: 100%;
}

.menu-button:hover .menu-line.top {
  width: 100%;
  transform: translateY(-1px);
}

.menu-button:hover .menu-line.middle {
  width: 100%;
  transform: scaleX(1.1);
}

.menu-button:hover .menu-line.bottom {
  width: 100%;
  transform: translateY(1px);
}

.menu-active .menu-line.top {
  transform: translateY(6px) rotate(45deg);
  width: 100%;
}

.menu-active .menu-line.middle {
  opacity: 0;
  transform: scaleX(0);
}

.menu-active .menu-line.bottom {
  transform: translateY(-6px) rotate(-45deg);
  width: 100%;
}

/* Enhanced Auth Component Wrapper */
.auth-wrapper {
  position: relative;
}

.auth-wrapper::before {
  content: '';
  position: absolute;
  inset: -4px;
  background: linear-gradient(135deg, #E29930, #5EA897);
  border-radius: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.auth-wrapper:hover::before {
  opacity: 0.1;
}

/* Enhanced Overlay */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: 30;
}

/* Enhanced Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  backdrop-filter: blur(0px);
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  backdrop-filter: blur(8px);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.slide-enter-to,
.slide-leave-from {
  transform: translateX(0%);
  opacity: 1;
}

/* Responsive Design */
@media (max-width: 640px) {
  /* 手機版只顯示 logo，確保有足夠空間給帳戶資訊 */
  .logo-text {
    display: none;
  }
  
  /* 手機版 logo 稍微大一點來補償文字的消失 */
  .logo-text + * {
    margin-left: 0;
  }
}

@media (max-width: 768px) {
  .logo-text h1 {
    font-size: 1.5rem;
  }
  
  .nav-scrolled {
    background: rgba(255, 255, 255, 0.98);
  }
}

/* Smooth scroll behavior for anchor links */
html {
  scroll-behavior: smooth;
}

/* Glass morphism effect enhancement */
@supports (backdrop-filter: blur(20px)) {
  .nav-scrolled {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px) saturate(180%);
  }
}

/* Gradient text animation */
@keyframes gradient-shift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.logo-text h1 span:last-child {
  background: linear-gradient(45deg, #3A6B60, #5EA897, #3A6B60, #5EA897);
  background-size: 300% 300%;
  animation: gradient-shift 4s ease infinite;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Micro-interactions */
.nav-link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #E29930, #5EA897);
  transform: translateX(-50%);
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

/* Focus states for accessibility */
.menu-button:focus,
.nav-link:focus {
  outline: 2px solid #E29930;
  outline-offset: 2px;
}

/* Loading states */
.nav-link.router-link-active {
  color: #E29930;
}

.nav-link.router-link-active::after {
  width: 100%;
  background: #E29930;
}
</style>
