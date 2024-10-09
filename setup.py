# -*- coding: utf-8 -*-
from setuptools import setup

APP = ['main.py']  # Certifique-se de que o nome do script principal está correto
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['os'],
}

setup(
    app=APP,  # Use 'app' e não 'APP' aqui
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

