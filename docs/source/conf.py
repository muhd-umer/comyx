# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# Package information
import comyx

version = comyx.__version__

project = "Comyx"
copyright = "2024, Muhammad Umer"
author = "Muhammad Umer"
release = str(version)

# -- General configuration ---------------------------------------------------

master_doc = "index"
templates_path = ["_templates"]
exclude_patterns = []

# -- Extension configuration -------------------------------------------------

extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_favicon",
    "sphinx_togglebutton",
    "myst_nb",
    "sphinxext.opengraph",
]

ogp_site_url = "https://comyx.readthedocs.io/latest/"
ogp_image = "http://comyx.readthedocs.io/latest/_static/ogp_image.png"
ogp_enable_meta_description = False
ogp_custom_meta_tags = [
    '<meta name="description" content="Comyx is a Python library for simulating wireless communication systems."/>',
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy-1.12.0/", None),
}
source_suffix = [".rst", ".ipynb", ".md"]

myst_enable_extensions = [
    "amsmath",
    "dollarmath",
    "html_image",
]
suppress_warnings = [
    "ref.citation",
    "ref.footnote",
    "myst.header",
    "misc.highlighting_failure",
]
nb_execution_mode = "auto"

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_book_theme"
html_title = ""
html_static_path = ["_static"]
html_show_sourcelink = False
html_show_sphinx = False
html_logo = "./_static/comyx_200px.png"
html_favicon = "./_static/favicon.png"
html_css_files = [
    "comyx.css",
]

# Add canonical URL
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")

html_theme_options = {
    "show_toc_level": 2,
    "repository_url": "https://github.com/muhd-umer/comyx",
    "use_repository_button": True,  # add a "link to repository" button
    "navigation_with_keys": False,
}

html_context = {
    "github_user": "muhd-umer",
    "github_repo": "comyx",
    "github_version": "main",
    "doc_path": "docs",
    "default_mode": "dark",
}

html_extra_path = ["_extra/googlee67cda8bc2355b91.html"]

# -- Options for autosummary/autodoc output ------------------------------------
autosummary_generate = True

# -- Options for autoapi -------------------------------------------------------

# Optionally disable autoapi generation for all files in a directory
autoapi_generate_api_docs = True
autoapi_type = "python"
autoapi_dirs = ["../../comyx"]
autoapi_keep_files = False
autoapi_root = "api"
autoapi_member_order = "groupwise"
autoapi_template_dir = "_templates/autoapi"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autodoc_typehints = "signature"
python_use_unqualified_type_names = True


def skip_submodules(app, what, name, obj, skip, options):
    if what == "module":
        skip = True
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_submodules)


remove_from_toctrees = ["_autosummary/*"]
