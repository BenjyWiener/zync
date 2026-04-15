"""Configuration file for the Sphinx documentation builder."""

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from pathlib import Path
import sys


project = 'ZyncIO'
copyright = '2026, Benjy Wiener'
author = 'Benjy Wiener'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.insert(0, str(Path(__file__).parent))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'enum_tools.autoenum',
    'sphinx_autodoc_typehints',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx_toolbox.more_autodoc.autoprotocol',
    'sphinx_toolbox.more_autodoc.typevars',
    'sphinxcontrib_trio',
    '_ext.autodoc_hooks',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

default_role = 'py:obj'

add_module_names = False

autoclass_content = 'both'

typehints_document_rtype_none = False

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
suppress_warnings = ['config.cache']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'shibuya'
html_static_path = ['_static']
html_logo = '_static/ZyncIO.png'
html_favicon = '_static/favicon.ico'
html_theme_options = {
    'accent_color': 'cyan',
    'globaltoc_expand_depth': 1,
    'github_url': 'https://github.com/BenjyWiener/zyncio',
}
html_context = {
    'source_type': 'github',
    'source_user': 'BenjyWiener',
    'source_repo': 'zyncio',
}
