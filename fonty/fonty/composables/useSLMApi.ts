/**
 * SLM NPU API 工具
 * 專門用於與獨立的SLM後端服務通信
 */

export const useSLMApi = () => {
  // SLM後端服務地址（獨立端口8001）
  const SLM_API_BASE = 'http://localhost:8001'
  
  /**
   * 構建SLM API的完整URL
   */
  const getSLMApiUrl = (endpoint: string): string => {
    // 移除開頭的斜線（如果有的話）
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint
    return `${SLM_API_BASE}/${cleanEndpoint}`
  }
  
  /**
   * 檢查SLM服務健康狀態
   */
  const checkSLMHealth = async () => {
    try {
      const response = await fetch(getSLMApiUrl('health'))
      if (response.ok) {
        return await response.json()
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
    } catch (error) {
      console.error('SLM健康檢查失敗:', error)
      throw error
    }
  }
  
  /**
   * 獲取SLM服務狀態
   */
  const getSLMStatus = async () => {
    try {
      const response = await fetch(getSLMApiUrl('status'))
      if (response.ok) {
        return await response.json()
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
    } catch (error) {
      console.error('獲取SLM狀態失敗:', error)
      throw error
    }
  }
  
  /**
   * 單個字型生成
   */
  const generateSLMFont = async (params: {
    character: string
    reference_image: File
    sampling_steps: number
    style_strength: number
  }) => {
    try {
      const formData = new FormData()
      formData.append('character', params.character)
      formData.append('reference_image', params.reference_image)
      formData.append('sampling_steps', params.sampling_steps.toString())
      formData.append('style_strength', params.style_strength.toString())
      
      const response = await fetch(getSLMApiUrl('generate'), {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('SLM單字生成失敗:', error)
      throw error
    }
  }
  
  /**
   * 批量字型生成
   */
  const batchGenerateSLMFonts = async (params: {
    characters: string
    reference_image: File
    sampling_steps: number
    style_strength: number
  }) => {
    try {
      const formData = new FormData()
      formData.append('characters', params.characters)
      formData.append('reference_image', params.reference_image)
      formData.append('sampling_steps', params.sampling_steps.toString())
      formData.append('style_strength', params.style_strength.toString())
      
      const response = await fetch(getSLMApiUrl('batch-generate'), {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('SLM批量生成失敗:', error)
      throw error
    }
  }
  
  /**
   * 清理SLM資源
   */
  const cleanupSLM = async () => {
    try {
      const response = await fetch(getSLMApiUrl('cleanup'), {
        method: 'POST',
      })
      
      if (response.ok) {
        return await response.json()
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
    } catch (error) {
      console.error('SLM清理失敗:', error)
      throw error
    }
  }
  
  /**
   * 簡單SLM測試 - 不需要圖片
   */
  const testSLMSimple = async (characters: string, message?: string) => {
    try {
      const formData = new FormData()
      formData.append('characters', characters)
      if (message) {
        formData.append('message', message)
      }
      
      const response = await fetch(getSLMApiUrl('test-simple'), {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('SLM簡單測試失敗:', error)
      throw error
    }
  }

  /**
   * SLM LLM對話 - 專注於文字回應，不需要圖片
   */
  const slmChat = async (params: {
    characters: string
    user_message?: string
    context?: string
  }) => {
    try {
      const formData = new FormData()
      formData.append('characters', params.characters)
      if (params.user_message) {
        formData.append('user_message', params.user_message)
      }
      if (params.context) {
        formData.append('context', params.context)
      }
      
      const response = await fetch(getSLMApiUrl('slm-chat'), {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('SLM對話失敗:', error)
      throw error
    }
  }

  return {
    SLM_API_BASE,
    getSLMApiUrl,
    checkSLMHealth,
    getSLMStatus,
    generateSLMFont,
    batchGenerateSLMFonts,
    testSLMSimple,
    slmChat,
    cleanupSLM,
  }
}
