@echo off
chcp 65001 >nul
echo ========================================
echo PDF工具离线包制作中心
echo ========================================
echo.
echo 请选择要制作的离线包类型：
echo.
echo 1. 离线包（需要目标机器有Python）
echo 2. 绿色版（包含Python解释器）
echo 3. 可执行版（exe文件，最推荐）
echo 4. 全部制作
echo 5. 退出
echo.
set /p choice=请输入选择 (1-5): 

if "%choice%"=="1" goto offline
if "%choice%"=="2" goto standalone
if "%choice%"=="3" goto exe
if "%choice%"=="4" goto all
if "%choice%"=="5" goto exit
goto invalid

:offline
echo.
echo [信息] 制作离线包...
call build_offline_package.bat
goto end

:standalone
echo.
echo [信息] 制作绿色版...
call build_standalone_package.bat
goto end

:exe
echo.
echo [信息] 制作可执行版...
call build_exe_package.bat
goto end

:all
echo.
echo [信息] 制作所有版本...
echo.
echo [信息] 1. 制作离线包...
call build_offline_package.bat
echo.
echo [信息] 2. 制作绿色版...
call build_standalone_package.bat
echo.
echo [信息] 3. 制作可执行版...
call build_exe_package.bat
echo.
echo [信息] 所有版本制作完成！
goto end

:invalid
echo 无效选择，请重新输入
goto end

:exit
echo 退出
goto end

:end
echo.
echo ========================================
echo 制作完成！
echo ========================================
echo.
echo 生成的文件：
echo - PDF工具离线包.zip （需要Python）
echo - PDF工具绿色版.zip （包含Python）
echo - PDF工具可执行版.zip （推荐，无需安装）
echo.
echo 推荐使用顺序：
echo 1. PDF工具可执行版.zip （最推荐，即插即用）
echo 2. PDF工具绿色版.zip （包含Python，适合无Python环境）
echo 3. PDF工具离线包.zip （需要目标机器有Python）
echo.
pause 