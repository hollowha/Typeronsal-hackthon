export const useApi = () => {
  const config = useRuntimeConfig()
  
  // 获取API基础地址
  const getApiBaseUrl = () => {
    return config.public.apiBaseUrl
  }
  
  // 生成完整的API URL
  const getApiUrl = (endpoint: string) => {
    const baseUrl = getApiBaseUrl()
    return `${baseUrl}${endpoint}`
  }
  
  // AI生成API
  const generateImage = async (data: FormData) => {
    const url = getApiUrl('/ai/generate')
    const response = await fetch(url, {
      method: 'POST',
      body: data
    })
    
    if (!response.ok) {
      throw new Error(`API调用失败: ${response.status}`)
    }
    
    return await response.json()
  }
  
  // AI混合API
  const blendImage = async (data: FormData) => {
    const url = getApiUrl('/ai/blend')
    const response = await fetch(url, {
      method: 'POST',
      body: data
    })
    
    if (!response.ok) {
      throw new Error(`API调用失败: ${response.status}`)
    }
    
    return await response.json()
  }
  
  // 获取用户列表
  const getUsers = async () => {
    const url = getApiUrl('/users')
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`获取用户失败: ${response.status}`)
    }
    
    return await response.json()
  }
  
  // 创建用户
  const createUser = async (userData: any) => {
    const url = getApiUrl('/users')
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    })
    
    if (!response.ok) {
      throw new Error(`创建用户失败: ${response.status}`)
    }
    
    return await response.json()
  }
  
  return {
    getApiBaseUrl,
    getApiUrl,
    generateImage,
    blendImage,
    getUsers,
    createUser
  }
}
