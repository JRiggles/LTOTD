from setuptools import setup

APP = ['src/ltotd.py']
VERSION = '1.1.0'
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'src/appicon.png',
    'plist': {
        'CFBundleIdentifier': 'com.jriggles.LTOTD',
        'CFBundleShortVersionString': VERSION,
        'LSUIElement': True,  # menu bar app
        'NSHumanReadableCopyright': (
            'Copyright © 2024-25 John Riggles [sudo_whoami] - MIT License'
        ),
    },
    'packages': ['httpx', 'rumps',],
}

setup(
    app=APP,
    name='LTOTD',
    version=VERSION,
    description='Get the Lospec Tag of the Day and show it in the menu bar',
    author='J. Riggles [sudo_whoami]',
    url='https://github.com/JRiggles/LTOTD',
    license='MIT',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
