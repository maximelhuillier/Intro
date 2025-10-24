"""
Setup script for AnalystHelper
Permet d'installer AnalystHelper comme package Python
"""

from setuptools import setup, find_packages
from pathlib import Path

# Lire le README
this_directory = Path(__file__).parent
long_description = (this_directory / "README_ANALYST_HELPER.md").read_text(encoding='utf-8')

setup(
    name='analyst-helper',
    version='1.0.0',
    author='AnalystHelper Contributors',
    description='Outil d\'aide à l\'analyse de dossiers, extraction de pièces jointes et génération de rapports',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/votre-username/analyst-helper',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'extract-msg>=0.45.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'black>=22.0',
            'flake8>=4.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'analyst-helper=demo:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
