// API服务
export async function getPublishedDocuments() {
  // 简单的模拟实现，返回模拟数据
  return {
    data: {
      documents: [
        {
          id: 1,
          title: '系统使用指南',
          content: '<p>欢迎使用本系统！本指南将帮助您快速了解系统的各项功能和操作方法。</p><p>系统主要包括课件/知识库管理、考试系统和人员管理三大模块。</p><p>如需更多帮助，请联系系统管理员。</p>',
          published_at: '2023-01-15T08:00:00Z'
        },
        {
          id: 2,
          title: '考试系统操作手册',
          content: '<p>本手册详细介绍了考试系统的使用方法，包括如何创建试卷、分配考试和查看成绩。</p><p>系统支持多种题型，包括选择题、填空题、简答题等。</p>',
          published_at: '2023-01-10T10:30:00Z'
        }
      ]
    }
  };
}

// 其他API函数可以在这里添加
export async function publishDocumentToHomepage(documentId) {
  // 模拟发布文档到主页的API调用
  return Promise.resolve({ success: true });
}

export async function uploadDocument(documentData) {
  // 模拟上传文档的API调用
  return Promise.resolve({ success: true });
}