@echo off
cl /LD /O2 /EHsc input_hook.cpp /Fe:input_hook.dll user32.lib
if %errorlevel% neq 0 exit /b %errorlevel%
echo built input_hook.dll