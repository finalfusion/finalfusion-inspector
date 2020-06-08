#!/usr/bin/env python3

from setuptools import setup

setup(
    name='finalfusion-inspector',
    version='0.1.0',
    author='Daniël de Kok',
    author_email='me@danieldk.eu',
    packages=['finalfusion_inspector'],
    package_data={
        'finalfusion_inspector': [
            '*.ui',
        ]
    },
    entry_points={
        'gui_scripts': [
            'finalfusion-inspector=finalfusion_inspector.__main__:main',
        ]
    },
    install_requires=[
        'finalfusion >= 0.7, < 0.8',
        'matplotlib == 3',
        'PyQt5 >= 5.13',
        'scikit-learn == 0.21.*'
    ],
)
