import dearpygui.dearpygui as dpg
import os
import subprocess

def create_and_run_bat(file_to_delete, is_gta):
    if is_gta:
        bat_content = f"""@echo off
setlocal
set "filepath=%USERPROFILE%\\Documents\\GTA San Andreas User Files\\gta_sa.set"
if exist "%filepath%" (
    del "%filepath%"
)
endlocal"""
    else:
        bat_content = '''@echo off
setlocal
set "PSCommand=[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; $folder = New-Object System.Windows.Forms.FolderBrowserDialog; if ($folder.ShowDialog() -eq 'OK') { $folder.SelectedPath }"
for /f "usebackq delims=" %%i in (`powershell -command "%PSCommand%"`) do set "gamePath=%%i"
set "sampFuncsPath=%gamePath%\\SAMPFUNCS"
if exist "%sampFuncsPath%" (
    set "fileFound=false"
    for %%f in ("%sampFuncsPath%\\sampfuncs-settings*.ini") do (
        del "%%f"
        set "fileFound=true"
    )
    if "%fileFound%"=="false" (
        rem No files to delete
    )
) else (
    rem SAMPFUNCS folder not found
)
endlocal
exit'''

    with open("delete_files.bat", "w") as bat_file:
        bat_file.write(bat_content)

    subprocess.run("delete_files.bat", shell=True)
    os.remove("delete_files.bat")

def delete_gta_callback(sender, app_data):
    create_and_run_bat("gta_sa.set", True)

def delete_samp_callback(sender, app_data):
    create_and_run_bat("sampfuncs-settings.ini", False)

dpg.create_context()
dpg.create_viewport(title='samp-helper (artem hikaru)', width=600, height=400)

dpg.set_viewport_resizable(True)

with dpg.window(tag="Primary", width=600, height=400):
    dpg.add_text("Select a file to delete:", wrap=200)
    dpg.add_spacer(height=10)
    dpg.add_button(label="Delete gta_sa.set", callback=delete_gta_callback, width=-1)
    dpg.add_spacer(height=10)
    dpg.add_button(label="Delete sampfuncs-settings.ini", callback=delete_samp_callback, width=-1)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()