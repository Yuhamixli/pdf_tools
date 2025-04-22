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
        logging.FileHandler("pdf_merger.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF合并工具")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 设置应用程序图标（可选）
        # self.root.iconbitmap("icon.ico")  # 如果有图标文件，可以取消注释
        
        # 源文件夹路径
        self.source_folder_var = tk.StringVar()
        
        # 输出文件名
        self.output_filename_var = tk.StringVar(value="合并后的文件.pdf")
        
        # 排序方式
        self.sort_method_var = tk.StringVar(value="按文件名")
        
        # PDF文件列表
        self.pdf_files = []
        
        # 创建UI
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 源文件夹选择
        folder_frame = ttk.LabelFrame(main_frame, text="选择源文件夹", padding="5")
        folder_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Entry(folder_frame, textvariable=self.source_folder_var, width=70).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        ttk.Button(folder_frame, text="浏览...", command=self.browse_source_folder).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 输出文件设置
        output_frame = ttk.LabelFrame(main_frame, text="输出文件设置", padding="5")
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(output_frame, text="输出文件名:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.output_filename_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(output_frame, text="排序方式:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        sort_options = ["按文件名", "按修改时间", "自定义排序"]
        ttk.Combobox(output_frame, textvariable=self.sort_method_var, values=sort_options, state="readonly", width=15).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 文件列表框架
        files_frame = ttk.LabelFrame(main_frame, text="PDF文件列表", padding="5")
        files_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 文件列表和滚动条
        files_scrollbar = ttk.Scrollbar(files_frame)
        files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(files_frame, yscrollcommand=files_scrollbar.set, selectmode=tk.EXTENDED)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        files_scrollbar.config(command=self.files_listbox.yview)
        
        # 文件列表按钮框架
        list_buttons_frame = ttk.Frame(files_frame)
        list_buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        ttk.Button(list_buttons_frame, text="↑", command=self.move_up, width=3).pack(padx=2, pady=2)
        ttk.Button(list_buttons_frame, text="↓", command=self.move_down, width=3).pack(padx=2, pady=2)
        ttk.Button(list_buttons_frame, text="✕", command=self.remove_selected, width=3).pack(padx=2, pady=2)
        ttk.Button(list_buttons_frame, text="刷新", command=self.refresh_file_list).pack(padx=2, pady=20)
        
        # 操作按钮框架
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(buttons_frame, text="合并PDF", command=self.merge_pdfs).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="退出", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
    def browse_source_folder(self):
        folder_path = filedialog.askdirectory(title="选择PDF文件所在文件夹")
        if folder_path:
            self.source_folder_var.set(folder_path)
            self.refresh_file_list()
    
    def refresh_file_list(self):
        folder_path = self.source_folder_var.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("错误", "请选择有效的文件夹")
            return
        
        # 清空列表框和文件列表
        self.files_listbox.delete(0, tk.END)
        self.pdf_files.clear()
        
        # 获取所有PDF文件
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        
        # 根据选择的排序方式进行排序
        sort_method = self.sort_method_var.get()
        if sort_method == "按文件名":
            pdf_files.sort()
        elif sort_method == "按修改时间":
            pdf_files.sort(key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
        
        # 更新文件列表和列表框
        self.pdf_files = pdf_files
        for pdf_file in self.pdf_files:
            self.files_listbox.insert(tk.END, pdf_file)
    
    def move_up(self):
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
        selected_indices = list(self.files_listbox.curselection())
        if not selected_indices:
            return
        
        # 从后往前删除，避免索引变化问题
        selected_indices.sort(reverse=True)
        for idx in selected_indices:
            self.files_listbox.delete(idx)
            self.pdf_files.pop(idx)
    
    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showerror("错误", "没有找到PDF文件，请选择包含PDF文件的文件夹")
            return
        
        folder_path = self.source_folder_var.get()
        output_filename = self.output_filename_var.get()
        
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'
        
        # 获取输出文件的保存位置
        output_path = filedialog.asksaveasfilename(
            initialdir=folder_path,
            initialfile=output_filename,
            defaultextension=".pdf",
            filetypes=[("PDF 文件", "*.pdf")]
        )
        
        if not output_path:
            return  # 用户取消了保存
        
        try:
            # 初始化进度条窗口
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
            
            for i, pdf_file in enumerate(self.pdf_files):
                pdf_path = os.path.join(folder_path, pdf_file)
                progress_label.config(text=f"正在添加: {pdf_file} ({i+1}/{len(self.pdf_files)})")
                self.root.update()
                
                try:
                    merger.append(pdf_path)
                    logger.info(f"添加文件: {pdf_path}")
                except Exception as e:
                    logger.error(f"添加文件 {pdf_path} 时出错: {str(e)}")
                    progress_window.destroy()
                    messagebox.showerror("错误", f"处理文件 {pdf_file} 时出错:\n{str(e)}")
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

def main():
    try:
        root = tk.Tk()
        app = PDFMergerApp(root)
        root.mainloop()
    except Exception as e:
        logger.critical(f"应用程序出现严重错误: {str(e)}")
        messagebox.showerror("严重错误", f"应用程序出现严重错误:\n{str(e)}")

if __name__ == "__main__":
    main() 