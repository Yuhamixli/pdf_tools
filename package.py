import os
import sys
import subprocess
import argparse
import shutil
from datetime import datetime
import platform
import site

def check_anaconda():
    """检查是否在Anaconda环境中运行"""
    # 检查路径中是否包含"anaconda"或"conda"
    python_path = sys.executable
    site_packages = site.getsitepackages()
    
    in_conda = False
    for path in [python_path] + site_packages:
        if "anaconda" in path.lower() or "conda" in path.lower():
            in_conda = True
            conda_path = path
            break
    
    return in_conda, python_path if in_conda else None

def check_pyinstaller():
    """检查 PyInstaller 是否已安装"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def create_version_file(version):
    """创建版本信息文件"""
    with open("version.txt", "w", encoding="utf-8") as f:
        f.write(f"版本号: {version}\n")
        f.write(f"构建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("构建工具: PyInstaller\n")

def package_app(app_name, windowed=True, version="1.0.0", icon=None, clean=False):
    """打包应用为可执行文件"""
    # 检查文件是否存在
    if not os.path.exists(f"{app_name}.py"):
        print(f"错误: {app_name}.py 文件不存在")
        return False
    
    # 检查PyInstaller
    if not check_pyinstaller():
        print("错误: 未安装 PyInstaller，请先运行: pip install pyinstaller")
        return False
    
    # 创建版本文件
    create_version_file(version)
    
    # 如果需要清理，删除之前的构建文件
    if clean and os.path.exists("dist"):
        shutil.rmtree("dist", ignore_errors=True)
    if clean and os.path.exists("build"):
        shutil.rmtree("build", ignore_errors=True)
    
    # 构建命令
    cmd = ["pyinstaller", "--onefile"]
    
    if windowed:
        cmd.append("--windowed")
    
    if icon and os.path.exists(icon):
        cmd.extend(["--icon", icon])
    
    cmd.extend([
        "--name", f"{app_name}_{version.replace('.', '_')}",
        f"{app_name}.py"
    ])
    
    # 执行打包命令
    print(f"开始打包 {app_name}...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        # 尝试使用subprocess.run
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"打包完成! 可执行文件位于 dist 目录。")
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {str(e)}")
        
        # 检查输出以查找特定错误
        if "pathlib" in e.stdout or "pathlib" in e.stderr:
            print("\n错误: 检测到与Anaconda环境中的pathlib包冲突!")
            print("解决方案:")
            print("1. 使用提供的build_package.bat脚本进行打包，它将在独立的虚拟环境中执行")
            print("2. 或者，手动设置一个虚拟环境后再执行此脚本:")
            print("   python -m venv venv")
            print("   venv\\Scripts\\activate (Windows) 或 source venv/bin/activate (Linux/Mac)")
            print("   pip install -r requirements.txt")
            print("   python package.py all --version 1.0.0 --clean\n")
        
        return False

def main():
    parser = argparse.ArgumentParser(description="PDF 合并工具打包脚本")
    parser.add_argument("app", choices=["pdf_merger", "pdf_drag_drop", "pdf_merger_cli", "pdf_merger_files", "pdf_tools", "all"], 
                      help="要打包的应用")
    parser.add_argument("--no-window", action="store_true", help="不使用窗口模式（针对命令行应用）")
    parser.add_argument("--version", default="1.0.0", help="版本号")
    parser.add_argument("--icon", help="应用图标路径")
    parser.add_argument("--clean", action="store_true", help="清理之前的构建文件")
    parser.add_argument("--force", action="store_true", help="强制打包，忽略环境警告")
    
    args = parser.parse_args()
    
    # 检查是否在Anaconda环境中
    in_conda, conda_path = check_anaconda()
    if in_conda and not args.force:
        print(f"警告: 您正在Anaconda环境中运行此脚本 ({conda_path})。")
        print("PyInstaller与Anaconda环境中的一些包（如pathlib）不兼容，可能导致打包失败。")
        print("建议:")
        print("1. 使用提供的build_package.bat脚本进行打包")
        print("2. 或者使用独立的Python环境（非Anaconda）")
        print("3. 如果您确定要在当前环境中继续，请添加--force参数\n")
        
        user_input = input("您确定要在当前环境中继续吗? [y/N]: ")
        if user_input.lower() != 'y':
            print("已取消打包操作。")
            return
    
    apps_to_package = []
    if args.app == "all":
        apps_to_package = ["pdf_merger", "pdf_drag_drop", "pdf_merger_cli", "pdf_merger_files", "pdf_tools"]
    else:
        apps_to_package = [args.app]
    
    success_count = 0
    for app in apps_to_package:
        # 对于命令行工具，如果未指定，默认不使用窗口模式
        windowed = not args.no_window
        if app in ["pdf_merger_cli", "pdf_merger_files"] and not args.no_window:
            windowed = False
        
        if package_app(app, windowed, args.version, args.icon, args.clean):
            success_count += 1
    
    # 输出最终结果
    total = len(apps_to_package)
    if success_count == total:
        print(f"\n打包成功! 所有 {total} 个应用已成功打包。")
    else:
        print(f"\n警告: 只有 {success_count}/{total} 个应用打包成功。")
        print("如果遇到问题，请考虑使用build_package.bat脚本进行打包。")

if __name__ == "__main__":
    main() 