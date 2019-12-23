from setuptools import setup

install_requires = [
    'aiohttp==3.6.2',
]

setup(
    name='aiotsearch',
    version="0.1.0",
    author='Anton Ovsyannikov',
    author_email='anton.ovsyannikov@gmail.com',
    description='Search topic with aiohttp.',
    platforms=['POSIX'],
    install_requires=install_requires,
    packages=['aiotsearch'],
)
