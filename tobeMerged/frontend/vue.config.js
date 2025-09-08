const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    },
    static: {
      directory: path.join(__dirname, 'public'),
      publicPath: '/'
    }
  },
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  },
  // 配置静态文件服务
  configureWebpack: {
    devServer: {
      static: {
        directory: path.join(__dirname, 'node_modules'),
        publicPath: '/node_modules'
      }
    }
  }
})
