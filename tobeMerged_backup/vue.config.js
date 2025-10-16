const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = {
  transpileDependencies: true,
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
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
  }
}
