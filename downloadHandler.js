// 文件下载处理器
export const DownloadHandler = {
  /**
   * 生成ZIP压缩包并触发下载
   * @param {Array<File>} files - 待下载文件数组
   * @param {string} zipName - 压缩包名称
   */
  async downloadAsZip(files, zipName = 'archive.zip') {
    try {
      const zipBlob = await this.#generateZip(files);
      this.#triggerDownload(zipBlob, zipName);
    } catch (error) {
      console.error('[Download Error]', error);
      this.#handleError('ZIP_GENERATION_FAILED');
    }
  },

  // 私有方法：生成ZIP文件
  async #generateZip(files) {
    const zip = new JSZip();
    files.forEach(file => {
      zip.file(file.name, file);
    });
    return zip.generateAsync({ type: 'blob' });
  },

  // 私有方法：触发浏览器下载
  #triggerDownload(blob, fileName) {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    window.URL.revokeObjectURL(url);
    link.remove();
  },

  // 错误处理
  #handleError(code) {
    const errorMap = {
      'ZIP_GENERATION_FAILED': '文件压缩失败，请检查文件格式',
      'INVALID_SIZE': '文件大小超过500MB限制'
    };
    alert(errorMap[code] || '未知错误');
  }
};
