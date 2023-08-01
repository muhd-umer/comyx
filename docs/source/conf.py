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
import simcomm

version = simcomm.__version__

project = "SimComm"
copyright = "2023, Muhammad Umer"
author = "Muhammad Umer"
release = str(version)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinx_copybutton",
    "autoapi.extension",
    # For extension examples and demos
    "ablog",
    "matplotlib.sphinxext.plot_directive",
    "numpydoc",
    "sphinx_togglebutton",
    "sphinx_favicon",
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy-1.8.1/", None),
}

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_title = f"SimComm ({version})"
html_static_path = ["_static"]
html_show_sourcelink = False
html_show_sphinx = False
html_favicon = "./favicon.ico"
html_logo = "./_static/fav.png"
html_static_path = ["_static"]
html_js_files = ["custom-icon.js"]
html_css_files = [
    "simcomm.css",
]

version_match = "v" + release

# -- Options for autosummary/autodoc output ------------------------------------
autosummary_generate = True
autodoc_typehints = "description"
autodoc_member_order = "groupwise"

# -- Options for autoapi -------------------------------------------------------
autoapi_type = "python"
autoapi_dirs = ["../../simcomm"]
autoapi_keep_files = True
autoapi_root = "api"
autoapi_member_order = "groupwise"

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/muhd-umer/simcomm",
            "icon": "fa-brands fa-github",
        },
    ],
    "logo": {
        "text": "SimComm",
        "image_dark": "_static/fav.png",
        "alt_text": "SimComm",
    },
    "footer_start": ["copyright"],
    "navbar_start": ["navbar-logo"],
    "navbar_align": "left",
    # "navbar_center": ["navbar-nav", "version-switcher"],
    "navbar_center": ["navbar-nav"],
    # "switcher": {
    #     "json_url": json_url,
    #     "version_match": version_match,
    # },
    "show_toc_level": 1,
    "show_nav_level": 2,
}

html_context = {
    "github_user": "muhd-umer",
    "github_repo": "simcomm",
    "github_version": "main",
    "doc_path": "docs",
}
