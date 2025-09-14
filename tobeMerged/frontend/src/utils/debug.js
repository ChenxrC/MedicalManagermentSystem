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
  },

  // 检测浏览器环境信息
  logBrowserEnvironment: () => {
    console.log('=== 浏览器环境信息 ===');
    console.log('浏览器:', navigator.userAgent);
    console.log('当前URL:', window.location.href);
    console.log('localStorage可用:', typeof localStorage !== 'undefined');
    console.log('sessionStorage可用:', typeof sessionStorage !== 'undefined');
    
    // 检测常见扩展可能注入的对象
    const commonExtensions = [
      'ethereum', 'web3', 'bitcoin', 'MetaMask', 'BinanceChain', 
      'coinbaseWalletExtension', 'phantom' 
    ];
    
    console.log('=== 检测到的可能扩展对象 ===');
    commonExtensions.forEach(key => {
      if (window[key]) {
        console.log(`检测到: window.${key}`);
      }
    });
  },

  // 处理可能的扩展冲突
  handleExtensionErrors: (error) => {
    if (error.message && error.message.includes('MetaMask')) {
      console.warn('\n=== 关于MetaMask错误的说明 ===');
      console.warn('这个错误可能是由MetaMask浏览器扩展引起的，不是应用本身的问题。');
      console.warn('解决方案:');
      console.warn('1. 尝试禁用MetaMask扩展后刷新页面');
      console.warn('2. 或者更新MetaMask到最新版本');
      console.warn('3. 或者在隐私模式下打开应用');
      console.warn('应用应该仍然可以正常使用，这个错误通常不影响核心功能。\n');
      return true;
    }
    return false;
  }
}
