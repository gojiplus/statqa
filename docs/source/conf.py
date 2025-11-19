"""Sphinx configuration for tableqa documentation."""

import sys
from pathlib import Path

from tableqa import __version__


# Add source to path
sys.path.insert(0, str(Path(__file__).parents[2] / "src"))

# Project information
project = "tableqa"
copyright = "2025, TableQA Contributors"
author = "TableQA Contributors"

# Version
version = __version__
release = __version__

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

# MyST parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

# Templates
templates_path = ["_templates"]
exclude_patterns = []

# HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# Autodoc
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
