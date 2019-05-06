# Configuration file for the Sphinx documentation builder.

from usps_client import version

project = "usps-client"
copyright = "2019, macro1"
author = "macro1"
release = version.VERSION

extensions = ["sphinx.ext.autodoc", "sphinxcontrib.apidoc"]
templates_path = ["_templates"]
exclude_patterns = []

html_theme = "alabaster"
html_static_path = ["_static"]

apidoc_module_dir = "../../src"
apidoc_toc_file = False
