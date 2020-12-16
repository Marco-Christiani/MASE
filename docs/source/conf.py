# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sphinx_rtd_theme


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))


# -- Project information -----------------------------------------------------

project = 'MASE'
copyright = '2020, Marco Christiani'
author = 'Marco Christiani'

# The full version, including alpha/beta/rc tags
release = '0.0.7'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'sphinx_rtd_theme', # Read The Docs theme
	'sphinx.ext.autodoc',
    'sphinx.ext.napoleon', # For google docstring support
    'sphinx.ext.mathjax', # latex
]
napoleon_google_docstring = True # setup for napolean
napoleon_numpy_docstring = False


autodoc_mock_imports = ['bs4', 'requests'] # for automatic documentation

autodoc_default_options = { # autodoc config options
    'members': True,
    'member-order': 'bysource',
    # 'special-members': '__init__', # document __init__ by default
    'undoc-members': True, # include functions/methods/etc missing docstrings
    'exclude-members': '__weakref__'
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']



