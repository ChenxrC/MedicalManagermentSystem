// Dify API 服务

// Dify API 基础配置
const DIFY_API_BASE = process.env.VUE_APP_DIFY_API_BASE_URL || 'https://api.dify.ai/v1'
const DIFY_API_KEY = process.env.VUE_APP_DIFY_API_KEY || 'your-dify-api-key'

// 发送消息到Dify API
export async function sendMessageToDify(inputs, query, conversationId = null) {
  try {
    // 检查API密钥是否已配置
    if (!DIFY_API_KEY || DIFY_API_KEY === 'your-dify-api-key') {
      throw new Error('Dify API密钥未正确配置，请检查环境变量设置')
    }
    
    const requestBody = {
      inputs,
      query,
      conversation_id: conversationId,
      user: 'edu-system-user', // 使用固定的用户ID
      response_mode: 'blocking'
    }
    
    console.log('Sending request to Dify API:', {
      url: `${DIFY_API_BASE}/chat-messages`,
      headers: {
        'Authorization': `Bearer ${DIFY_API_KEY.substring(0, 5)}...`, // 只记录API密钥的前5位用于调试
        'Content-Type': 'application/json'
      },
      body: requestBody
    })
    
    const response = await fetch(`${DIFY_API_BASE}/chat-messages`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${DIFY_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Dify API error response:', errorData)
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.message || 'Unknown error'}`)
    }

    const data = await response.json()
    console.log('Dify API response:', data)
    return data
  } catch (error) {
    console.error('Error sending message to Dify:', error)
    throw error
  }
}

// 获取对话历史
export async function getConversationMessages(conversationId) {
  try {
    // 检查API密钥是否已配置
    if (!DIFY_API_KEY || DIFY_API_KEY === 'your-dify-api-key') {
      throw new Error('Dify API密钥未正确配置，请检查环境变量设置')
    }
    
    const response = await fetch(`${DIFY_API_BASE}/messages?conversation_id=${conversationId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${DIFY_API_KEY}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Dify API error response:', errorData)
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.message || 'Unknown error'}`)
    }

    const data = await response.json()
    console.log('Dify API response:', data)
    return data
  } catch (error) {
    console.error('Error fetching conversation messages:', error)
    throw error
  }
}

// 创建反馈
export async function createFeedback(messageId, rating) {
  try {
    // 检查API密钥是否已配置
    if (!DIFY_API_KEY || DIFY_API_KEY === 'your-dify-api-key') {
      throw new Error('Dify API密钥未正确配置，请检查环境变量设置')
    }
    
    const response = await fetch(`${DIFY_API_BASE}/messages/${messageId}/feedbacks`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${DIFY_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        rating
      })
    })

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Dify API error response:', errorData)
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.message || 'Unknown error'}`)
    }

    const data = await response.json()
    console.log('Dify API response:', data)
    return data
  } catch (error) {
    console.error('Error creating feedback:', error)
    throw error
  }
}