.. pypepa documentation master file, created by
   sphinx-quickstart on Thu Jul 18 15:33:13 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypepa's documentation!
==================================

.. image:: pypepa.png
    :align: left
    :width: 140px

pypepa is a library and a toolset for `Performance Evaluation Process Algebra
<http://www.dcs.ed.ac.uk/pepa/>`_ (PEPA) by Jane Hillston. pypepa is not a fully PEPA compatible tool, it supports a limited (for now) PEPA syntax
(we only allow ``<>`` operator in system equation), i.e. it does not suport hiding operator (e.g.
``P\{a,b,}``), does not calculate passage time and provide model checking. pypepa also does not use Kronecker
state space representation and Hillston's aggregation algorithms, so it can have worse performance
than the PEPA Eclipse Plugin. All these features, plus more, are planned to be added in future versions.

----------------

pypepa consist of three parts:

1. ``libpepa`` - a library written in Python,
2. ``pypepa`` - a command line tool for solving and graphing,
3. ``distr`` - map reduce tools for solving large PEPA experiments (not done yet)

News
----

**(18.07.2013)** pypepa can now calculate utilisations of components' states, output argument works
again

**(07.06.2013)** Added support for defining rates as mathematical expressions, e.g. r=2*3+7*n;

Documentation
-------------

.. toctree::
   :maxdepth: 2

   installdoc
   clidoc
   libpepadoc
   credits



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

