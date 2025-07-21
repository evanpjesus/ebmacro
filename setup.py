from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'EB Macro',
        'CFBundleDisplayName': 'EB Macro',
        'CFBundleIdentifier': 'com.yourname.ebmacro',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    },
    'packages': ['pynput'],
}

setup(
    app=APP,
    name='EB Macro',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)