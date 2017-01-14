"""
Setup file for Replay Enhancer.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='replayenhancer',
    version='0.5.1rc2',
    description='Replay Enhancer 0.5.1 Release Candidate 2',
    long_description=long_description,
    url='https://github.com/SenorPez/project-cars-replay-enhancer',
    author='Senor Pez',
    author_email='contact_at_github@example.org',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='gaming racing video data streaming',
    packages=find_packages(exclude=['assets', 'tests', 'utils']),
    install_requires=['moviepy', 'natsort', 'Pillow', 'tqdm'],
    extras_require={
        'dev': [],
        'test': []
    },
    package_data={
        'replayenhancer': [
            'lib/Roboto-Medium.ttf',
            'lib/Roboto-Regular.ttf',
            'lib/track_data.json']
    },
    entry_points={
        'console_scripts': [
            'replayenhancer=replayenhancer.replayenhancer:main',
            'packetcapture=replayenhancer.packetcapture:main'
        ],
    },
)

