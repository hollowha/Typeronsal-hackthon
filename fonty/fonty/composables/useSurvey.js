import { ref } from 'vue'
import { doc, setDoc, getDoc, collection, addDoc, serverTimestamp } from 'firebase/firestore'
import { db } from '~/plugins/firebase.js'
import { userState } from '~/composables/useAuth.js'

export const useSurvey = () => {
  const isSubmitting = ref(false)
  const hasVoted = ref(false)
  const isChecking = ref(false)

  // 檢查用戶是否已經投過票
  const checkUserHasVoted = async () => {
    if (!userState.isAuthenticated || !userState.user?.uid) {
      return false
    }

    isChecking.value = true
    
    try {
      const userVoteRef = doc(db, 'user_surveys', userState.user.uid)
      const docSnap = await getDoc(userVoteRef)
      
      hasVoted.value = docSnap.exists()
      return hasVoted.value
    } catch (error) {
      console.error('檢查投票狀態失敗:', error)
      return false
    } finally {
      isChecking.value = false
    }
  }

  // 提交問卷回應
  const submitSurveyResponse = async (response) => {
    if (!userState.isAuthenticated || !userState.user?.uid) {
      throw new Error('用戶未登入')
    }

    if (hasVoted.value) {
      throw new Error('用戶已經投過票了')
    }

    isSubmitting.value = true

    try {
      const surveyData = {
        userId: userState.user.uid,
        userEmail: userState.user.email,
        userDisplayName: userState.user.displayName,
        response: response, // 'very_interested', 'maybe_interested', 'not_interested'
        timestamp: serverTimestamp(),
        userAgent: navigator.userAgent,
        // 可以添加更多元數據
        surveyVersion: '1.0'
      }

      // 1. 將回應存到 surveys collection (用於統計分析)
      await addDoc(collection(db, 'surveys'), surveyData)

      // 2. 記錄用戶已投票的狀態 (防重複投票)
      const userVoteData = {
        userId: userState.user.uid,
        hasVoted: true,
        response: response,
        votedAt: serverTimestamp()
      }
      
      await setDoc(doc(db, 'user_surveys', userState.user.uid), userVoteData)

      hasVoted.value = true
      console.log('問卷提交成功:', surveyData)

      return true
    } catch (error) {
      console.error('提交問卷失敗:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  // 獲取問卷統計數據 (管理員功能，可選)
  const getSurveyStats = async () => {
    try {
      // 這個功能需要管理員權限，暫時先保留架構
      // 實際使用時可以配置 Firebase Rules 限制存取
      const statsRef = doc(db, 'survey_stats', 'general')
      const docSnap = await getDoc(statsRef)
      
      if (docSnap.exists()) {
        return docSnap.data()
      }
      return null
    } catch (error) {
      console.error('獲取統計數據失敗:', error)
      return null
    }
  }

  return {
    hasVoted,
    isSubmitting,
    isChecking,
    checkUserHasVoted,
    submitSurveyResponse,
    getSurveyStats
  }
}
