"""Sphinx configuration."""
project = "AWS SNS Subscription Manager"
author = "Andrew Herrington"
copyright = "2022, Andrew Herrington"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
