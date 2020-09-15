=======
autofmu
=======

.. image:: https://github.com/ajcerejeira/autofmu/workflows/CI/badge.svg
   :target: https://github.com/ajcerejeira/autofmu/actions
   :alt: Python package

.. image:: https://readthedocs.org/projects/autofmu/badge/?version=latest
   :target: https://autofmu.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://codecov.io/gh/ajcerejeira/autofmu/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ajcerejeira/autofmu
   :alt: Coverage status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black code style

Automatic FMU approximation tool.


.. begin-getting-started

Installation
============

Compilers
---------

To correctly build an FMU this program needs to compile the generated C source
into a shared library, therefore it requires the installation of C compilers.

If you are using the provided ``docker`` image to run the program then you are
already able to cross compile the generated FMU to ``linux32``, ``linus64``,
``win32`` and ``win64`` platforms.

Otherwise if you are using a Linux distribution, you probably already have
``gcc`` installed, so you should be able to compile FMUs for your system. If
you want to share the generated FMU it is advisable to also install a cross
compiler to produce the binaries for Windows platforms (like
`MinGW <http://www.mingw.org/>`_). Below are the instructions to install with
``apt`` and ``dnf``:

**Debian/Ubuntu**:

::

   sudo apt install gcc-x86-64-linux-gnu gcc-i686-linux-gnu gcc-mingw-w64 gcc-mingw-w64-i686

**Fedora**:

::

   sudo dnf install gcc-x86_64-linux-gnu mingw64-gcc mingw32-gcc



Usage
=====

``autofmu`` process a dataset

::

   autofmu "dataset.csv" --inputs "x" "y" --outputs "z" -o "My Awesome Model.fmu"

This will read the ``dataset.csv`` file, select the ``x``, ``y`` and ``z``
columns and find an approximation of the relation between the inputs and the
outputs. Based on this relation, the sources files for the  FMU will be
generated and compiled, resulting in the ``My Awesome Model.fmu`` file ready
to be used for simulations.

.. end-getting-started


Contributing
============

License
=======

This project is licensed under MIT license.
