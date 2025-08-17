<template>
  <div class="chatbot-container">
    <el-card class="chatbot-card">
      <template #header>
        <div class="card-header">
          <span>知识库问答</span>
        </div>
      </template>
      <div class="chatbot-content">
        <div ref="chatContainer" class="chat-messages">
          <div v-for="message in messages" :key="message.id" class="message" :class="message.sender">
            <div class="message-content">{{ message.text }}</div>
            <div class="message-time">{{ message.time }}</div>
          </div>
        </div>
        <div class="chat-input">
          <el-input
            v-model="inputMessage"
            placeholder="请输入您的问题..."
            @keyup.enter="sendMessage"
          />
          <el-button type="primary" @click="sendMessage">发送</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { sendMessageToDify } from '@/services/dify.js'

export default {
  name: 'ChatbotView',
  data() {
    return {
      messages: [
        {
          id: 1,
          text: '您好！我是基于知识库的智能问答助手，请问有什么可以帮助您的吗？',
          sender: 'bot',
          time: new Date().toLocaleTimeString()
        }
      ],
      inputMessage: '',
      conversationId: null
    }
  },
  methods: {
    async sendMessage() {
      if (this.inputMessage.trim() === '') return
      
      // 添加用户消息
      const userMessage = {
        id: this.messages.length + 1,
        text: this.inputMessage,
        sender: 'user',
        time: new Date().toLocaleTimeString()
      }
      
      this.messages.push(userMessage)
      const query = this.inputMessage
      this.inputMessage = ''
      
      try {
        // 调用Dify API
        const response = await sendMessageToDify({}, query, this.conversationId)
        
        // 更新对话ID
        if (!this.conversationId && response.conversation_id) {
          this.conversationId = response.conversation_id
        }
        
        // 添加机器人回复
        const botMessage = {
          id: this.messages.length + 1,
          text: response.answer,
          sender: 'bot',
          time: new Date().toLocaleTimeString()
        }
        
        this.messages.push(botMessage)
      } catch (error) {
        // 错误处理
        let errorMessageText = '抱歉，我在处理您的问题时遇到了错误。请稍后再试。'
        
        // 检查是否有具体的错误信息
        if (error.response && error.response.data && error.response.data.message) {
          errorMessageText = `错误: ${error.response.data.message}`
        } else if (error.message) {
          errorMessageText = `错误: ${error.message}`
        }
        
        const errorMessage = {
          id: this.messages.length + 1,
          text: errorMessageText,
          sender: 'bot',
          time: new Date().toLocaleTimeString()
        }
        
        this.messages.push(errorMessage)
        console.error('Error sending message to Dify:', error)
      } finally {
        // 滚动到最新消息
        this.$nextTick(() => {
          const container = this.$refs.chatContainer
          container.scrollTop = container.scrollHeight
        })
      }
    }
  },
  mounted() {
    // 滚动到最新消息
    this.$nextTick(() => {
      const container = this.$refs.chatContainer
      container.scrollTop = container.scrollHeight
    })
  }
}
</script>

<style scoped>
.chatbot-container {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.chatbot-card {
  width: 100%;
  max-width: 800px;
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.card-header {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.chatbot-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin-bottom: 20px;
  background-color: #f5f7fa;
}

.message {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

.message.user {
  align-items: flex-end;
}

.message.bot {
  align-items: flex-start;
}

.message-content {
  padding: 10px 15px;
  border-radius: 15px;
  max-width: 70%;
  word-wrap: break-word;
}

.message.user .message-content {
  background-color: #409eff;
  color: white;
}

.message.bot .message-content {
  background-color: #ffffff;
  border: 1px solid #ebeef5;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input .el-input {
  flex: 1;
}
</style>