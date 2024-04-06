from setuptools import setup

def get_plat_name():
    """Parses value of the --plat-name from the program arguments."""



APP = ['test.py']
DATA_FILES = []
OPTIONS = {}

setup(
    app=APP,
    version="0.1",
    options={
        'py2app': OPTIONS
    },
    data_files=DATA_FILES,
    setup_requires=['py2app'],

)
