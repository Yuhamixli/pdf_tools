import os
import sys
import argparse
from PyPDF2 import PdfMerger
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pdf_merger_cli.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def merge_pdfs_from_folder(folder_path, output_path, sort_by="name", reverse=False):
    """
    从指定文件夹合并PDF文件
    
    参数:
        folder_path: PDF文件所在的文件夹路径
        output_path: 输出的PDF文件路径
        sort_by: 排序方式，可选值：'name'（按文件名）或'time'（按修改时间）
        reverse: 是否反向排序
    """
    logger.info(f"开始从文件夹 {folder_path} 合并PDF文件")
    
    # 确保文件夹存在
    if not os.path.isdir(folder_path):
        logger.error(f"文件夹 {folder_path} 不存在")
        raise FileNotFoundError(f"文件夹 {folder_path} 不存在")
    
    # 获取文件夹中所有PDF文件
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        logger.error(f"在文件夹 {folder_path} 中未找到PDF文件")
        raise FileNotFoundError(f"在文件夹 {folder_path} 中未找到PDF文件")
    
    # 排序PDF文件
    if sort_by.lower() == 'name':
        pdf_files.sort(reverse=reverse)
        logger.info("按文件名排序PDF文件")
    elif sort_by.lower() == 'time':
        pdf_files.sort(key=lambda f: os.path.getmtime(os.path.join(folder_path, f)), reverse=reverse)
        logger.info("按修改时间排序PDF文件")
    else:
        logger.warning(f"未知的排序方式: {sort_by}，使用默认的文件名排序")
        pdf_files.sort(reverse=reverse)
    
    # 初始化PdfMerger对象
    merger = PdfMerger()
    
    # 合并PDF文件
    for i, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(folder_path, pdf_file)
        logger.info(f"添加文件 ({i+1}/{len(pdf_files)}): {pdf_path}")
        try:
            merger.append(pdf_path)
        except Exception as e:
            logger.error(f"添加文件 {pdf_path} 时出错: {str(e)}")
            raise
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 写入合并后的PDF文件
    logger.info(f"写入合并后的PDF文件: {output_path}")
    merger.write(output_path)
    merger.close()
    
    logger.info(f"PDF合并完成，共合并了 {len(pdf_files)} 个文件")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='PDF文件合并工具')
    parser.add_argument('folder', help='包含PDF文件的文件夹路径')
    parser.add_argument('-o', '--output', help='输出文件路径，默认为"合并后的文件.pdf"', default='合并后的文件.pdf')
    parser.add_argument('-s', '--sort', choices=['name', 'time'], default='name', help='排序方式: name(文件名) 或 time(修改时间)')
    parser.add_argument('-r', '--reverse', action='store_true', help='反向排序')
    
    args = parser.parse_args()
    
    try:
        output_path = args.output
        # 如果输出路径不是绝对路径，则相对于当前工作目录
        if not os.path.isabs(output_path):
            output_path = os.path.join(os.getcwd(), output_path)
        
        # 确保输出文件名以.pdf结尾
        if not output_path.lower().endswith('.pdf'):
            output_path += '.pdf'
        
        # 合并PDF文件
        result_path = merge_pdfs_from_folder(args.folder, output_path, args.sort, args.reverse)
        print(f"PDF文件合并成功! 输出文件: {result_path}")
        
    except Exception as e:
        logger.error(f"合并PDF文件时出错: {str(e)}")
        print(f"错误: {str(e)}")
        sys.exit(1)
    
if __name__ == "__main__":
    main() 