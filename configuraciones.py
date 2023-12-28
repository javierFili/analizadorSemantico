import sys
from cx_Freeze import setup, Executable

build_exe_options = {
  "excludes": ["kivy", "re", "copy", "kivy.app"],
  "zip_include_packages": ["encodings", "PySide6"],
}
base = "Win32GUI" if sys.platform == "win32" else None
setup(
  name="Expresiones",
  version="1.0",
  description="Descripción de Mi Aplicación",
  executables=[Executable("startApp.py")],
  options={"build_exe": build_exe_options},
)
