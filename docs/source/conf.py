# Configuration file for the Sphinx documentation builder.

from usps_client.version import VERSION as version

release = version
project = "usps-client"
copyright = "2019, macro1"
author = "macro1"

extensions = ["sphinx.ext.autodoc", "sphinxcontrib.apidoc"]
templates_path = ["_templates"]
exclude_patterns = []

html_theme = "alabaster"
html_static_path = ["_static"]

apidoc_module_dir = "../../src"
apidoc_toc_file = False
