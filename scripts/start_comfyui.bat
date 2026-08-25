@echo off
setlocal
set "AI_VIDEO_ROOT=%~dp0.."
call "%AI_VIDEO_ROOT%\.venv\Scripts\activate.bat"
cd /d "%AI_VIDEO_ROOT%\ComfyUI"
echo ComfyUI: http://127.0.0.1:8188
echo Runtime log: %AI_VIDEO_ROOT%\logs\comfyui_start.log
python main.py --lowvram --preview-method none --listen 127.0.0.1 --port 8188 --disable-auto-launch >> "%AI_VIDEO_ROOT%\logs\comfyui_start.log" 2>&1
endlocal
