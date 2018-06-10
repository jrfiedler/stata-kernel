# stata-kernel
A Stata kernel for IPython/Jupyter

**This code is not actively maintained. If anyone is interested in taking over this project, with more active maintenance, please feel free to do so.**

## Setup
This kernel currently only works in Windows.

You need a recent version of Stata, 
and if you have not already used Stata automation, register its type library 
by following [these instructions](http://www.stata.com/automation/#createmsapp).

You also need IPython 3.

## Installing
You can install with

    pip install git+https://github.com/jrfiedler/stata-kernel
    python -m stata_kernel.install
	
## Using
After installing, simply open an IPython notebook server

    ipython notebook
	
and choose a new "Stata" notebook.
