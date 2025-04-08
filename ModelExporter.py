import os
import shutil
import gradio as gr
from modules import scripts, script_callbacks, shared

class ModelExporter(scripts.Script):
    def title(self):
        return "Custom Model Exporter"
    
    def show(self, is_img2img):
        return scripts.AlwaysVisible
    
    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("📦 Model Exporter", open=False):
                # 模型类型映射
                self.model_types = {
                    "Checkpoints": "Stable-diffusion",
                    "LoRA": "Lora",
                    "VAE": "VAE",
                    "Embeddings": "embeddings"
                }
                
                # 目录选择组件
                model_dir = gr.Textbox(
                    label="模型目录",
                    placeholder="点击右侧按钮选择目录",
                    interactive=False
                )
                dir_btn = gr.Button("📁 选择目录", variant="secondary")
                
                # 模型类型选择
                model_type = gr.Dropdown(
                    label="模型类型",
                    choices=list(self.model_types.keys()),
                    value="Checkpoints"
                )
                
                # 模型文件列表
                model_file = gr.Dropdown(
                    label="选择模型",
                    choices=self.scan_models("Checkpoints", ""),
                    interactive=True
                )
                
                # 导出路径组件
                export_path = gr.Textbox(
                    label="导出路径",
                    placeholder="D:/backup",
                    interactive=True
                )
                export_btn = gr.Button("🚀 开始导出", variant="primary")
                
                # 状态显示
                status = gr.Textbox(label="操作状态", interactive=False)

        # 交互逻辑
        dir_btn.click(
            fn=lambda: gr.Files(visible=True),
            outputs=dir_btn
        ).then(
            fn=self.select_directory,
            outputs=[model_dir, model_file]
        )
        
        model_type.change(
            fn=lambda t,d: gr.Dropdown(choices=self.scan_models(t,d)),
            inputs=[model_type, model_dir],
            outputs=model_file
        )
        
        export_btn.click(
            fn=self.export_model,
            inputs=[model_dir, model_type, model_file, export_path],
            outputs=status
        )

        return [dir_btn, model_dir, model_type, model_file, export_path, export_btn, status]

    def select_directory(self):
        try:
            # 调用系统目录选择对话框
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            path = filedialog.askdirectory()
            return path if path else ""
        except:
            return "[ERROR] 需要桌面环境支持"

    def scan_models(self, model_type, base_dir):
        if not base_dir:
            return []
        target_dir = os.path.join(base_dir, self.model_types[model_type])
        if not os.path.exists(target_dir):
            return []
        return [f for f in os.listdir(target_dir) 
               if f.endswith(('.ckpt','.safetensors','.pt','.bin'))]

    def export_model(self, base_dir, model_type, model_file, export_path):
        try:
            # 路径验证
            if not all([base_dir, model_file, export_path]):
                return "❌ 缺少必要参数"
                
            src_path = os.path.join(base_dir, self.model_types[model_type], model_file)
            if not os.path.exists(src_path):
                return "❌ 源文件不存在"
                
            # 创建目标目录
            os.makedirs(export_path, exist_ok=True)
            
            # 执行复制
            shutil.copy2(src_path, os.path.join(export_path, model_file))
            return f"✅ 导出成功 → {export_path}"
            
        except Exception as e:
            return f"❌ 错误: {str(e)}"

# 注册到设置页
def on_ui_settings():
    shared.opts.add_option(
        "default_export_path", 
        shared.OptionInfo(
            "D:/sd_models/exports",
            "默认导出目录",
            gr.Textbox,
            section=("model_exporter", "模型导出器")
        )
    )

script_callbacks.on_ui_settings(on_ui_settings)
