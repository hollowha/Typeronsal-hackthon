export default defineNuxtPlugin(() => {
    const cookieSecure = useRuntimeConfig().public.cookieSecure
    useCookie('isSideMenuOpen', { 
        maxAge: 60 * 60, 
        secure: cookieSecure, 
        watch: true, 
        default: () => false 
    })
})