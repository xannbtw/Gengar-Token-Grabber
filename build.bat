@echo off
color 0e
echo.
set /p exe_name="Enter .exe name: "
if [%exe_name%]==[] ( 
    echo.
    echo Enter a name pls.
    pause
) 
if [%exe_name%] NEQ [] (
    echo.
    echo Name is: %exe_name%
    pyinstaller --clean --onefile --noconsole -i NONE -n %exe_name% main.py
    rmdir /s /q __pycache__
    rmdir /s /q build
    del /f / s /q %exe_name%.spec
    echo.
    echo generated exe as %exe_name%.exe in the dist folder
    echo.
    pause
    EXIT /B 1
)