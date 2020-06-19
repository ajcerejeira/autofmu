=======
autofmu
=======

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

.. end-getting-started


Contributing
============

License
=======

This project is licensed under MIT license.
