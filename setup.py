import os
import sys
import pypepa

try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup

requires = ["matplotlib >= 1.2.0", 
            "numpy >= 1.6.0", 
            "scipy >= 0.10", 
            "pyparsing >= 1.5.4",
            "colorama >= 0.2.4"]

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
        install_requires = requires,
        license = open("LICENCE.txt").read(),
        zip_safe = False,

        entry_points = {
            'console_scripts': ['pypepa=pypepa.cli.cli:main',]
            },
        classifiers = (
            'Environment :: Console',
            'Development Status :: 4 - Beta',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 2.7',
            'License :: OSI Approved :: Apache Software License',
            'Intended Audience :: Science/Research'
            ),
        )


