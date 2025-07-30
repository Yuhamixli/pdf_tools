# PDF 合并工具

这是一个简单易用的 PDF 文件合并工具，可以将多个 PDF 文件合并为一个文件。该工具提供了多种使用方式，适合不同的使用场景。

## 功能特点

- 图形界面操作，简单易用
- 支持文件拖放功能（需安装额外依赖）
- 支持自定义合并顺序
- 支持按文件名或修改时间排序
- 提供命令行接口，适合批处理操作
- 详细的日志记录，方便问题排查
- 统一启动器，一站式访问所有功能

## 🚀 快速开始

### 一键启动（推荐）

**直接双击运行 `start.bat` 即可启动PDF工具！**

这个脚本会自动检测Python环境、安装依赖并启动工具。

### 手动启动

```bash
python pdf_tools.py
```

启动器界面中提供以下功能入口：
- PDF合并工具 - 文件夹模式
- PDF合并工具 - 拖放模式
- PDF合并工具 - 命令行模式
- PDF合并工具 - 文件列表模式

### 独立工具

也可以直接使用各个独立的工具：

#### 图形界面版本

1. **PDF 合并工具**（`pdf_merger.py`）：
   ```bash
   python pdf_merger.py
   ```
   - 提供完整的图形界面，可选择文件夹进行合并
   - 可自定义排序方式和输出文件名
   - 支持预览和调整文件顺序

2. **拖放合并工具**（`pdf_drag_drop.py`）：
   ```bash
   python pdf_drag_drop.py
   ```
   - 支持直接拖放 PDF 文件到界面进行合并
   - 可自定义文件顺序
   - 简单直观的操作方式

#### 命令行版本

1. **文件夹合并模式**（`pdf_merger_cli.py`）：
   ```bash
   python pdf_merger_cli.py /path/to/pdf/folder -o 输出文件.pdf -s name
   ```
   参数说明：
   - 第一个参数：PDF 文件所在文件夹路径
   - `-o, --output`：输出文件名（默认为"合并后的文件.pdf"）
   - `-s, --sort`：排序方式，可选 name（按文件名）或 time（按修改时间）
   - `-r, --reverse`：反向排序

2. **指定文件合并模式**（`pdf_merger_files.py`）：
   ```bash
   python pdf_merger_files.py file1.pdf file2.pdf file3.pdf -o 输出文件.pdf
   ```
   参数说明：
   - 列出要合并的所有 PDF 文件路径
   - `-o, --output`：输出文件名（默认为"合并后的文件.pdf"）

## 安装依赖

### Anaconda环境（推荐）

如果你使用Anaconda，请运行以下脚本自动配置环境：

```bash
# 双击运行或在命令行执行
setup_anaconda.bat
```

### 标准Python环境

```bash
pip install -r requirements.txt
```

### 快速启动

配置完成后，可以直接双击运行：
- `run_pdf_tools.bat` - 快速启动PDF工具

## 打包为可执行文件

### 推荐的打包方式

为了避免环境问题（特别是在Anaconda环境中），提供了专用的打包脚本：

- 双击运行 `build_package.bat`

这个脚本会自动创建独立的虚拟环境，安装所需依赖，并执行打包操作，有效避免Anaconda等环境中的兼容性问题。

### 使用打包脚本（高级用户）

如果你熟悉命令行，也可以直接使用打包脚本：

```bash
# 打包所有工具
python package.py all --version 1.0.0 --clean

# 打包单个工具
python package.py pdf_merger --version 1.0.0 --clean
python package.py pdf_drag_drop --version 1.0.0 --clean
python package.py pdf_merger_cli --no-window --version 1.0.0 --clean
python package.py pdf_merger_files --no-window --version 1.0.0 --clean

# 打包统一启动器
python package.py pdf_tools --version 1.0.0 --clean
```

注意：如果你在Anaconda环境中，上述命令可能会失败。在这种情况下，请使用前面提到的打包脚本，或手动创建一个虚拟环境。

### 手动打包

也可以使用 PyInstaller 手动打包：

```bash
# 打包图形界面版本
pyinstaller --onefile --windowed pdf_merger.py
pyinstaller --onefile --windowed pdf_drag_drop.py 
pyinstaller --onefile --windowed pdf_tools.py

# 打包命令行版本
pyinstaller --onefile pdf_merger_cli.py
pyinstaller --onefile pdf_merger_files.py
```

## 关于Anaconda环境的注意事项

如果你使用Anaconda Python环境，PyInstaller可能会遇到与某些Anaconda特定包（如pathlib的backport版本）的兼容性问题。解决方法：

1. 使用提供的自动化打包脚本（`build_package.bat`）
2. 创建一个独立的虚拟环境进行打包：
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python package.py all --version 1.0.0 --clean
   ```

## 使用提示

1. 在使用图形界面版本时，可以使用"上移"和"下移"按钮调整文件顺序
2. 拖放版本需要安装额外的 `tkinterdnd2` 库才能使用拖放功能
3. 命令行版本适合集成到自动化脚本或批处理流程中
4. 统一启动器提供了最便捷的使用体验，推荐新用户使用

## 故障排除

- 如果遇到 PDF 文件合并失败，请检查日志文件（`pdf_merger.log`、`pdf_drag_drop.log` 等）
- 如果拖放功能不可用，请确认是否已安装 `tkinterdnd2` 库
- 部分损坏的 PDF 文件可能会导致合并失败，请检查源文件是否完好
- 如果遇到其他问题，请查看应用程序日志文件获取详细错误信息
- 打包时出现pathlib相关错误，请参考上面"关于Anaconda环境的注意事项"部分

## 许可证

MIT 许可证 