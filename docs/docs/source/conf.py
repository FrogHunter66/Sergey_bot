# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath('C:\\Users\\NikeX\\PycharmProjects\\Sergey_test'))  # путь к проекту

extensions = [
    'sphinx.ext.autodoc',     # документация из docstring
    'sphinx.ext.napoleon',    # Google-style docstrings
    'myst_parser',            # Markdown поддержка
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sergey_test'
copyright = '2025, Nikita'
author = 'Nikita'
release = '2.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
