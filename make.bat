@echo on
set PY_FILE=face_shape_key_fixer.py
set PROJECT_NAME=Face Shape Key Fixer
set VERSION=1.0.0
set FILE_VERSION=file_version_info.txt
set ICO_DIR=pes_indie.ico

pyinstaller --onefile "%PY_FILE%" --icon="%ICO_DIR%" --name "%PROJECT_NAME%_%VERSION%" --version-file "%FILE_VERSION%"

copy fix_ps2_for_releases.bat dist\fix_ps2.bat
copy fix_psp_for_releases.bat dist\fix_psp.bat
cd dist
tar -acvf "%PROJECT_NAME%_%VERSION%.zip" *
pause
