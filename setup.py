import os
import sys
import pypepa

try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup

setup (
        name = "pypepa",
        version = pypepa.__version__,
        description = "pypepa is a PEPA library and a toolset for PEPA.",
        long_description = open("README.rst").read() + '\n\n' +
                           open("HISTORY.rst").read(),
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
        install_requires = ["matplotlib", 
            "numpy", 
            "scipy", 
            "pyparsing",
            "colorama"],
        license = "Apache Common 2.0",
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


