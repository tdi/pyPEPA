import os
import sys

try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup


setup (
        name = "pypepa",
        version = "0.4.10dev1",
        description = "pypepa is a PEPA library and a toolset for PEPA.",
        long_description = open("README.rst").read(),
        author = "Dariusz Dwornikowski", 
        author_email = "dariusz.dwornikowski@cs.put.poznan.pl",
        url = "https://github.com/tdi/pyPEPA",
        packages = ["pypepa",
                    "pypepa.cli",
                    "pypepa.parsing",
                    "pypepa.derivation",
                    "pypepa.experiments",
                    "pypepa.solvers",
            ],
        package_data={'': ['LICENCE.txt']},
        requires = [
           'numpy (>=1.6.7)',
            'scipy (>=0.10)', 
            'pyparsing (==1.5.7)',
            'matplotlib (>=1.2.0)',
            ],
        install_requires = ['numpy>=1.6.7', 'scipy>=0.11', 'pyparsing==1.5.6',
                             'matplotlib>=1.2.1'],
        license = "Apache Common 2.0",
        zip_safe = False,

        entry_points = {
            'console_scripts': ['pypepa=pypepa.cli.cli:main',]
            },
        classifiers = [
            'Environment :: Console',
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 2.7',
            'License :: OSI Approved :: Apache Software License',
            'Intended Audience :: Science/Research',
            'Operating System :: POSIX',
            ],
)



