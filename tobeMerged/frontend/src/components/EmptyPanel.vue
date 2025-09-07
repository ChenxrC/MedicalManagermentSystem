<template>
  <div class="empty-panel">
    <div class="empty-content">
      <Document class="empty-icon" />
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmptyPanel',
  props: {
    message: {
      type: String,
      default: '暂无内容'
    }
  }
}
</script>

<style lang="scss" scoped>
.empty-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.2);
}

.empty-content {
  text-align: center;
  padding: $spacing-sm; // 减小padding
  
  .empty-icon {
    font-size: 24px; // 减小图标
    color: rgba(255, 255, 255, 0.4);
    margin-bottom: $spacing-sm;
  }
  
  p {
    margin: 0;
    font-size: 12px; // 减小文本
    color: rgba(255, 255, 255, 0.6);
  }
  
  // 在分屏/小屏幕下进一步优化
  @media (max-width: 1200px) or (max-height: 600px) {
    padding: $spacing-xs;
    .empty-icon { font-size: 20px; margin-bottom: $spacing-xs; }
    p { font-size: 11px; }
  }
}
</style>
