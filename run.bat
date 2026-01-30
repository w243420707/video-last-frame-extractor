@echo off
chcp 65001 >nul
setlocal

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"

REM 使用虚拟环境中的 Python
set "PYTHON=%SCRIPT_DIR%venv\Scripts\python.exe"

REM 检查是否有参数
if "%~1"=="" (
    echo 使用方法: 把视频文件拖拽到此脚本上，或者在命令行运行:
    echo     run.bat ^<视频文件路径^> [输出图片路径]
    echo.
    echo 示例:
    echo     run.bat video.mp4
    echo     run.bat video.mp4 output.png
    pause
    exit /b 1
)

REM 运行 Python 脚本
"%PYTHON%" "%SCRIPT_DIR%extract_last_frame.py" %*

pause
