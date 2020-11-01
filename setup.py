from cx_Freeze import setup, Executable

executables = [Executable("paysdufle.py", base = "Win32GUI")]

packages = ["sys", 'time', 'pygame', 'logging', 'pygame_menu', 'moviepy']
options = {
    'build_exe': {    
        'packages':packages,
    },
}

setup(
    name = "Pays du FLE",
    options = options,
    version = "1.0",
    description = "L'anniversaire magique",
    executables = executables
)