from setuptools import setup
from setuptools.command.install import install

class CustomInstall(install):
    def run(self):
        install.run(self)
        # Create details.sv from details.sv.template
        with open('/opt/GnomeWallpaperSetter/details.sv', 'w') as details_file:
            # Here, you can specify default or placeholder values for the configuration.
            details_file.write('{"APIKEY": "", "Collection": "", "Hdir": "", "last_fetch_timestamp": ""}')


setup(
    name='GnomeWallpaperSetter',
    version='0.1',
    packages=['GnomeWallpaperSetter'],
    install_requires=[
        'requests','json', 'random', 'datetime', 'multiprocessing'
    ], cmdclass={'install': CustomInstall}
)
