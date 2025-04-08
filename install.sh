# install.sh
#!/bin/bash
PLUGIN_DIR="extensions/sd-folder-download"

# 创建必要目录
mkdir -p $PLUGIN_DIR/{javascript,styles,scripts}

# 设置权限
chmod 755 $PLUGIN_DIR
chmod 644 $PLUGIN_DIR/config.json

# 安装Python依赖
pip install -r requirements.txt
