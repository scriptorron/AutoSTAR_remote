del /S /Q dist\AutoSTAR_remote > NUL:
rd /S /Q dist\AutoSTAR_remote

del /S /Q build > NUL:
rd /S /Q build

call conda env export > environment.yml

pyinstaller AutoSTAR_remote.spec
if %errorlevel% neq 0 exit /b %errorlevel%

