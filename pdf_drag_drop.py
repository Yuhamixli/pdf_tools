import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfMerger
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pdf_drag_drop.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 全局变量，控制是否启用拖放功能
ENABLE_DND = False

# 尝试导入拖放库
try:
    import tkinterdnd2
    ENABLE_DND = True
    logger.info("成功加载tkinterdnd2库，拖放功能已启用")
except ImportError:
    logger.warning("未找到tkinterdnd2库，拖放功能将不可用")
    pass  # 忽略错误，应用将在没有拖放功能的情况下运行

class PDFDragDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF拖放合并工具")
        self.root.geometry("600x400")
        
        # 设置应用程序图标（可选）
        # self.root.iconbitmap("icon.ico")
        
        # PDF文件列表
        self.pdf_files = []
        
        # 创建UI
        self.create_widgets()
        
        # 设置拖放功能
        if ENABLE_DND:
            self.setup_drag_drop()
        else:
            # 如果不支持拖放，显示提示信息
            text = "拖放功能不可用 (需要安装tkinterdnd2库)\n请使用\"添加文件\"按钮选择文件"
            self.show_dnd_not_available(text)
    
    def show_dnd_not_available(self, message):
        """在拖放区域显示提示信息"""
        warning_label = ttk.Label(
            self.drop_frame,
            text=message,
            foreground="red",
            justify="center",
            wraplength=500
        )
        warning_label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 顶部说明标签
        instruction_text = "将PDF文件拖放到下方区域，或点击\"添加文件\"按钮选择文件"
        instruction_label = ttk.Label(main_frame, text=instruction_text, font=("Helvetica", 10))
        instruction_label.pack(pady=10)
        
        # 拖放区域框架
        self.drop_frame = ttk.LabelFrame(main_frame, text="拖放区域")
        self.drop_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建一个滚动条
        scrollbar = ttk.Scrollbar(self.drop_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建列表框来显示文件
        self.files_listbox = tk.Listbox(
            self.drop_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED,
            font=("Courier", 10)
        )
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 添加文件按钮
        add_btn = ttk.Button(button_frame, text="添加文件", command=self.add_files)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空列表按钮
        clear_btn = ttk.Button(button_frame, text="清空列表", command=self.clear_list)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 上移按钮
        up_btn = ttk.Button(button_frame, text="上移", command=self.move_up)
        up_btn.pack(side=tk.LEFT, padx=5)
        
        # 下移按钮
        down_btn = ttk.Button(button_frame, text="下移", command=self.move_down)
        down_btn.pack(side=tk.LEFT, padx=5)
        
        # 移除选中按钮
        remove_btn = ttk.Button(button_frame, text="移除选中", command=self.remove_selected)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # 合并按钮
        merge_btn = ttk.Button(button_frame, text="合并PDF", command=self.merge_pdfs)
        merge_btn.pack(side=tk.RIGHT, padx=5)
    
    def setup_drag_drop(self):
        """
        设置拖放功能，仅在tkinterdnd2可用时被调用
        """
        if not ENABLE_DND:
            return
            
        try:
            # 绑定拖放事件
            self.files_listbox.drop_target_register("DND_Files")
            self.files_listbox.dnd_bind('<<Drop>>', self.handle_drop)
            logger.info("拖放功能已设置")
        except Exception as e:
            logger.error(f"设置拖放功能时出错: {str(e)}")
            self.show_dnd_not_available(f"设置拖放功能时出错: {str(e)}\n请使用\"添加文件\"按钮选择文件")
    
    def handle_drop(self, event):
        """
        处理拖放事件
        """
        try:
            # 获取拖放的文件路径
            files = self.files_listbox.tk.splitlist(event.data)
            self.add_files_to_list(files)
        except Exception as e:
            logger.error(f"处理拖放事件时出错: {str(e)}")
            messagebox.showerror("错误", f"处理拖放文件时出错:\n{str(e)}")
    
    def add_files_to_list(self, file_paths):
        # 过滤并添加PDF文件
        for file_path in file_paths:
            if file_path.lower().endswith('.pdf') and os.path.isfile(file_path):
                if file_path not in self.pdf_files:
                    self.pdf_files.append(file_path)
                    self.files_listbox.insert(tk.END, os.path.basename(file_path))
                    logger.info(f"添加文件: {file_path}")
            else:
                logger.warning(f"忽略非PDF文件: {file_path}")
    
    def add_files(self):
        # 打开文件选择对话框
        file_paths = filedialog.askopenfilenames(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        
        if file_paths:
            self.add_files_to_list(file_paths)
    
    def clear_list(self):
        # 清空文件列表
        self.pdf_files.clear()
        self.files_listbox.delete(0, tk.END)
        logger.info("清空文件列表")
    
    def move_up(self):
        # 上移选中的文件
        selected_indices = self.files_listbox.curselection()
        if not selected_indices or selected_indices[0] == 0:
            return
        
        for idx in selected_indices:
            # 交换文件列表中的项
            self.pdf_files[idx], self.pdf_files[idx-1] = self.pdf_files[idx-1], self.pdf_files[idx]
            
            # 更新列表框显示
            item_text = self.files_listbox.get(idx)
            self.files_listbox.delete(idx)
            self.files_listbox.insert(idx-1, item_text)
            self.files_listbox.selection_set(idx-1)
    
    def move_down(self):
        # 下移选中的文件
        selected_indices = list(self.files_listbox.curselection())
        if not selected_indices or selected_indices[-1] == len(self.pdf_files) - 1:
            return
        
        # 从下往上处理，避免索引变化问题
        selected_indices.reverse()
        for idx in selected_indices:
            if idx < len(self.pdf_files) - 1:
                # 交换文件列表中的项
                self.pdf_files[idx], self.pdf_files[idx+1] = self.pdf_files[idx+1], self.pdf_files[idx]
                
                # 更新列表框显示
                item_text = self.files_listbox.get(idx)
                self.files_listbox.delete(idx)
                self.files_listbox.insert(idx+1, item_text)
                self.files_listbox.selection_set(idx+1)
    
    def remove_selected(self):
        # 移除选中的文件
        selected_indices = list(self.files_listbox.curselection())
        if not selected_indices:
            return
        
        # 从后往前删除，避免索引变化问题
        selected_indices.sort(reverse=True)
        for idx in selected_indices:
            self.files_listbox.delete(idx)
            self.pdf_files.pop(idx)
    
    def merge_pdfs(self):
        # 合并PDF文件
        if not self.pdf_files:
            messagebox.showerror("错误", "没有选择PDF文件")
            return
        
        # 获取输出文件的保存位置
        output_path = filedialog.asksaveasfilename(
            title="保存合并后的PDF",
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf")]
        )
        
        if not output_path:
            return  # 用户取消了保存
        
        try:
            # 显示进度窗口
            progress_window = tk.Toplevel(self.root)
            progress_window.title("合并进度")
            progress_window.geometry("300x100")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            progress_label = ttk.Label(progress_window, text="正在合并PDF文件...")
            progress_label.pack(pady=10)
            
            progress_bar = ttk.Progressbar(progress_window, mode="indeterminate")
            progress_bar.pack(fill=tk.X, padx=20, pady=10)
            progress_bar.start()
            
            # 更新UI
            self.root.update()
            
            # 合并PDF文件
            merger = PdfMerger()
            
            for i, pdf_path in enumerate(self.pdf_files):
                progress_label.config(text=f"正在添加: {os.path.basename(pdf_path)} ({i+1}/{len(self.pdf_files)})")
                self.root.update()
                
                try:
                    merger.append(pdf_path)
                    logger.info(f"添加文件: {pdf_path}")
                except Exception as e:
                    logger.error(f"添加文件 {pdf_path} 时出错: {str(e)}")
                    progress_window.destroy()
                    messagebox.showerror("错误", f"处理文件 {os.path.basename(pdf_path)} 时出错:\n{str(e)}")
                    return
            
            # 写入合并后的PDF文件
            merger.write(output_path)
            merger.close()
            
            # 销毁进度条窗口
            progress_window.destroy()
            
            # 显示成功消息
            logger.info(f"PDF合并成功，已保存为: {output_path}")
            messagebox.showinfo("成功", f"所有PDF文件已成功合并并保存为:\n{output_path}")
            
        except Exception as e:
            logger.error(f"PDF合并过程中出错: {str(e)}")
            messagebox.showerror("错误", f"合并PDF时出错:\n{str(e)}")

def create_tk_instance():
    """
    创建一个适当的Tk实例，根据是否可以使用tkinterdnd2
    """
    if ENABLE_DND:
        try:
            # 使用tkinterdnd2的Tk
            root = tkinterdnd2.TkinterDnD.Tk()
            logger.info("使用tkinterdnd2.TkinterDnD.Tk实例")
            return root
        except Exception as e:
            logger.error(f"创建tkinterdnd2.TkinterDnD.Tk实例时出错: {str(e)}")
            # 如果失败，回退到标准Tk
            ENABLE_DND = False
    
    # 使用标准Tk
    logger.info("使用标准tk.Tk实例")
    return tk.Tk()

def main():
    # 配置高DPI支持
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
        logger.info("已启用高DPI支持")
    except Exception:
        logger.info("未启用高DPI支持")
        pass  # 忽略错误
    
    try:
        # 创建主窗口
        root = create_tk_instance()
        
        # 创建应用
        app = PDFDragDropApp(root)
        
        # 启动主循环
        root.mainloop()
    except Exception as e:
        logger.critical(f"应用程序启动时出现严重错误: {str(e)}")
        messagebox.showerror("严重错误", f"应用程序启动时出现错误:\n{str(e)}")

if __name__ == "__main__":
    main() 