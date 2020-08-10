from setuptools import setup

setup(
    name='podcaster',
    version='0.1',
    description="Podcast player for the command line",
    author="Niklas Mertsch",
    author_email="niklasmertsch@web.de",
    packages=['podcaster'],
    license='MIT',
    install_requires=[
        'feedparser',
        'youtube-dl',
        'python-mpv',
    ],
    entry_points={
        'console_scripts': [
            'podcaster=podcaster.main:main',
        ]
    },
)
