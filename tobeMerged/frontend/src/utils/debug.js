// 调试工具
export const debugAPI = {
  // 检查API响应
  checkResponse: (response, endpoint) => {
    console.log(`🔍 API调试 - ${endpoint}:`, {
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers.entries()),
      url: response.url
    })
  },

  // 检查API数据
  checkData: (data, endpoint) => {
    console.log(`📊 数据调试 - ${endpoint}:`, {
      type: typeof data,
      isArray: Array.isArray(data),
      length: Array.isArray(data) ? data.length : 'N/A',
      hasResults: data && data.results ? Array.isArray(data.results) : false,
      data: data
    })
  },

  // 检查表格数据
  checkTableData: (data, componentName) => {
    console.log(`📋 表格数据调试 - ${componentName}:`, {
      type: typeof data,
      isArray: Array.isArray(data),
      length: Array.isArray(data) ? data.length : 'N/A',
      firstItem: Array.isArray(data) && data.length > 0 ? data[0] : 'N/A',
      data: data
    })
  }
}
