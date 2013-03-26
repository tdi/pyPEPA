pyPEPA
======

pyPEPA is a PEPA library and a toolset for Performance Evaluation Process Algebra (PEPA) by Jane
Hillston. 


About
=====

pyPEPA consist of three parts:

 1. libpepa --- a library written in python (mostly 3.3+ conformant)
 2. pyPEPA --- a command line tool for solving and graphing
 3. distr/ --- a map reduce tool for solving large PEPA experiments


Installation
============

For the current version I recommend installing in a virtualenv. 

1. Clone the project

    git clone git@github.com:tdi/pyPEPA.git pypepa
    cd pypepa

2. Make a virtualenv

    mkvirtualenv -p /usr/bin/python3 pypepa
    workon pypepa

3. Install all requirements

    pip install pyparsing colorama numpy scipy matplotlib


pyPEPA
======

### Simple usage

Show help command:

     ./pyPEPA -h

