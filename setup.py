from setuptools import setup, find_packages


setup(
    name='LanzlOrbiter',
    author='DiNitride',
    url='',
    version='0.1.0',
    license='MIT',
    description='Bot bot bot',
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['lanzl=lanzl.bot:main']}
)