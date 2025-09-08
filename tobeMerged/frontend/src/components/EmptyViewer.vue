<template>
  <div class="empty-viewer">
    <div class="empty-content">
      <VideoPlay class="empty-icon" />
      <h2>欢迎使用视频和PDF浏览系统</h2>
      <p>请从左侧文件列表中选择要查看的文件，或上传新文件开始使用</p>
      
      <div class="features">
        <div class="feature-item">
          <VideoPlay />
          <span>支持多种视频格式</span>
        </div>
        <div class="feature-item">
          <Document />
          <span>PDF文档查看</span>
        </div>
        <div class="feature-item">
          <FullScreen />
          <span>全屏播放模式</span>
        </div>
        <div class="feature-item">
          <Grid />
          <span>分屏对照查看</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmptyViewer'
}
</script>

<style lang="scss" scoped>
.empty-viewer {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
}

.empty-content {
  text-align: center;
  max-width: 500px;
  padding: $spacing-xxl;
  
  .empty-icon {
    font-size: 80px;
    color: $tech-blue;
    margin-bottom: $spacing-lg;
    opacity: 0.8;
  }
  
  h2 {
    margin: 0 0 $spacing-md 0;
    font-size: 24px;
    font-weight: 600;
    color: #ffffff;
    background: $gradient-primary;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  p {
    margin: 0 0 $spacing-xl 0;
    font-size: 16px;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
  }
  
  .features {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: $spacing-lg;
    
    .feature-item {
      display: flex;
      align-items: center;
      gap: $spacing-sm;
      padding: $spacing-md;
      background: rgba(255, 255, 255, 0.05);
      border-radius: $border-radius-medium;
      border: 1px solid rgba(255, 255, 255, 0.1);
      transition: all 0.3s ease;
      
      &:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: $tech-blue;
        transform: translateY(-2px);
        box-shadow: $shadow-light;
      }
      
      svg {
        font-size: 20px;
        color: $tech-cyan;
      }
      
      span {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
      }
    }
  }
}
</style>
