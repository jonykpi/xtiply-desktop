from setuptools import setup

def get_plat_name():
    """Parses value of the --plat-name from the program arguments."""



APP = ['xtiply.py']
DATA_FILES = []
OPTIONS = {
'argv_emulation': True,
'iconfile': 'app_icon.png',
}

setup(
    app=APP,
    version="0.1",
    options={
        'py2app': OPTIONS
    },
    data_files=DATA_FILES,
    setup_requires=['py2app'],

)
