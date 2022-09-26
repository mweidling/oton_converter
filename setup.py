# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = open('requirements.txt').read().split('\n')

setup(
    name='oton_converter',
    version='0.1.0',
    description='A CLI tool for converting OCR-D workflows to NextFlow',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mewidling/oton_converter',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=install_requires,
    package_data={
        '': ['*.json', '*.yml', '*.yaml', '*.list', '*.xml'],
    },
    entry_points={
        'console_scripts': [
            'oton=oton.cli:cli',
        ]
    },
)