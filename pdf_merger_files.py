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
        logging.FileHandler("pdf_merger_files.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def merge_pdf_files(pdf_files, output_path):
    """
    合并指定的PDF文件
    
    参数:
        pdf_files: PDF文件路径列表
        output_path: 输出的PDF文件路径
    """
    if not pdf_files:
        logger.error("没有提供PDF文件")
        raise ValueError("没有提供PDF文件")
    
    # 验证所有文件是否存在
    for pdf_path in pdf_files:
        if not os.path.isfile(pdf_path):
            logger.error(f"文件 {pdf_path} 不存在")
            raise FileNotFoundError(f"文件 {pdf_path} 不存在")
    
    # 初始化PdfMerger对象
    merger = PdfMerger()
    
    # 合并PDF文件
    for i, pdf_path in enumerate(pdf_files):
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
    parser = argparse.ArgumentParser(description='PDF文件合并工具 - 指定文件版')
    parser.add_argument('files', nargs='+', help='要合并的PDF文件路径列表')
    parser.add_argument('-o', '--output', help='输出文件路径，默认为"合并后的文件.pdf"', default='合并后的文件.pdf')
    
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
        result_path = merge_pdf_files(args.files, output_path)
        print(f"PDF文件合并成功! 输出文件: {result_path}")
        
    except Exception as e:
        logger.error(f"合并PDF文件时出错: {str(e)}")
        print(f"错误: {str(e)}")
        sys.exit(1)
    
if __name__ == "__main__":
    main() 