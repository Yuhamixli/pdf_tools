import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import importlib
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pdf_tools.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PDFToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 工具集")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", font=("Helvetica", 10))
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        header = ttk.Label(main_frame, text="PDF 工具集", style="Header.TLabel")
        header.pack(pady=10)
        
        # 介绍文本
        intro = ttk.Label(main_frame, text="请选择要使用的工具：", wraplength=450)
        intro.pack(pady=10)
        
        # 工具按钮框架
        tools_frame = ttk.LabelFrame(main_frame, text="可用工具", padding=10)
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 工具列表
        tools = [
            {
                "name": "PDF合并工具 - 文件夹模式",
                "description": "选择一个文件夹，合并其中所有PDF文件",
                "module": "pdf_merger",
                "function": self.run_pdf_merger
            },
            {
                "name": "PDF合并工具 - 拖放模式",
                "description": "通过拖放方式选择并合并PDF文件",
                "module": "pdf_drag_drop",
                "function": self.run_pdf_drag_drop
            },
            {
                "name": "PDF合并工具 - 命令行模式",
                "description": "以命令行方式合并指定文件夹中的PDF文件",
                "module": "pdf_merger_cli",
                "function": self.run_pdf_merger_cli
            },
            {
                "name": "PDF合并工具 - 文件列表模式",
                "description": "以命令行方式合并指定的PDF文件列表",
                "module": "pdf_merger_files",
                "function": self.run_pdf_merger_files
            }
        ]
        
        # 创建工具按钮
        for tool in tools:
            tool_frame = ttk.Frame(tools_frame)
            tool_frame.pack(fill=tk.X, pady=5)
            
            tool_button = ttk.Button(
                tool_frame, 
                text=tool["name"], 
                command=tool["function"],
                width=30
            )
            tool_button.pack(side=tk.LEFT, padx=5)
            
            tool_desc = ttk.Label(tool_frame, text=tool["description"], wraplength=250)
            tool_desc.pack(side=tk.LEFT, padx=5)
        
        # 底部按钮框架
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        # 退出按钮
        exit_button = ttk.Button(bottom_frame, text="退出", command=self.root.quit)
        exit_button.pack(side=tk.RIGHT)
        
        # 检查工具可用性
        self.check_tools_availability(tools)
    
    def check_tools_availability(self, tools):
        """检查各个工具模块是否可用"""
        for tool in tools:
            try:
                importlib.import_module(tool["module"])
                logger.info(f"工具 {tool['name']} 可用")
            except ImportError as e:
                logger.warning(f"工具 {tool['name']} 不可用: {str(e)}")
                messagebox.showwarning(
                    "工具不可用", 
                    f"工具 '{tool['name']}' 不可用，请确认所有文件都在当前目录中。\n错误: {str(e)}"
                )
    
    def run_module(self, module_name):
        """运行指定的模块"""
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'main'):
                module.main()
            else:
                logger.error(f"模块 {module_name} 没有main函数")
                messagebox.showerror("错误", f"无法启动 {module_name} 工具，模块没有main函数")
        except Exception as e:
            logger.error(f"运行 {module_name} 时出错: {str(e)}")
            messagebox.showerror("错误", f"运行工具时出错:\n{str(e)}")
    
    def run_pdf_merger(self):
        """运行文件夹模式PDF合并工具"""
        logger.info("启动PDF合并工具 - 文件夹模式")
        self.root.withdraw()  # 隐藏主窗口
        
        try:
            self.run_module("pdf_merger")
        finally:
            self.root.deiconify()  # 恢复主窗口
    
    def run_pdf_drag_drop(self):
        """运行拖放模式PDF合并工具"""
        logger.info("启动PDF合并工具 - 拖放模式")
        self.root.withdraw()  # 隐藏主窗口
        
        try:
            self.run_module("pdf_drag_drop")
        finally:
            self.root.deiconify()  # 恢复主窗口
    
    def run_pdf_merger_cli(self):
        """运行命令行模式PDF合并工具"""
        logger.info("启动PDF合并工具 - 命令行模式")
        
        folder_path = self.prompt_for_folder()
        if not folder_path:
            return
        
        output_path = self.prompt_for_output_file("合并后的文件.pdf")
        if not output_path:
            return
        
        sort_method = self.prompt_for_sort_method()
        if sort_method is None:
            return
        
        try:
            from pdf_merger_cli import merge_pdfs_from_folder
            result = merge_pdfs_from_folder(folder_path, output_path, sort_method)
            messagebox.showinfo("成功", f"PDF文件合并成功！\n输出文件: {result}")
        except Exception as e:
            logger.error(f"合并PDF文件时出错: {str(e)}")
            messagebox.showerror("错误", f"合并PDF文件时出错:\n{str(e)}")
    
    def run_pdf_merger_files(self):
        """运行文件列表模式PDF合并工具"""
        logger.info("启动PDF合并工具 - 文件列表模式")
        
        from tkinter import filedialog
        
        files = filedialog.askopenfilenames(
            title="选择要合并的PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        
        if not files:
            return
        
        output_path = self.prompt_for_output_file("合并后的文件.pdf")
        if not output_path:
            return
        
        try:
            from pdf_merger_files import merge_pdf_files
            result = merge_pdf_files(files, output_path)
            messagebox.showinfo("成功", f"PDF文件合并成功！\n输出文件: {result}")
        except Exception as e:
            logger.error(f"合并PDF文件时出错: {str(e)}")
            messagebox.showerror("错误", f"合并PDF文件时出错:\n{str(e)}")
    
    def prompt_for_folder(self):
        """提示用户选择文件夹"""
        from tkinter import filedialog
        folder_path = filedialog.askdirectory(title="选择包含PDF文件的文件夹")
        return folder_path
    
    def prompt_for_output_file(self, default_name):
        """提示用户选择输出文件路径"""
        from tkinter import filedialog
        output_path = filedialog.asksaveasfilename(
            title="选择输出文件路径",
            initialfile=default_name,
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf")]
        )
        return output_path
    
    def prompt_for_sort_method(self):
        """提示用户选择排序方式"""
        dialog = tk.Toplevel(self.root)
        dialog.title("选择排序方式")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        sort_var = tk.StringVar(value="name")
        reverse_var = tk.BooleanVar(value=False)
        result = [None]  # 使用列表存储结果，便于在内部函数中修改
        
        def on_ok():
            result[0] = (sort_var.get(), reverse_var.get())
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="请选择排序方式:").pack(anchor=tk.W, pady=5)
        
        ttk.Radiobutton(frame, text="按文件名排序", variable=sort_var, value="name").pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="按修改时间排序", variable=sort_var, value="time").pack(anchor=tk.W)
        
        ttk.Checkbutton(frame, text="反向排序", variable=reverse_var).pack(anchor=tk.W, pady=5)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="确定", command=on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=on_cancel).pack(side=tk.RIGHT, padx=5)
        
        dialog.wait_window()
        
        return result[0]

def main():
    # 配置高DPI支持
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass  # 忽略错误
    
    root = tk.Tk()
    app = PDFToolsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 