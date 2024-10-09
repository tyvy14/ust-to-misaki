from setuptools import setup

APP = ['seu_script.py']  # Substitua pelo nome do seu script
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter'],  # Inclua tkinter, pois ele é necessário para a interface
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
