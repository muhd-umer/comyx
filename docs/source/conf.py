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
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
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

# json_url = "./_static/versions.json"

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
}

html_context = {
    "github_user": "muhd-umer",
    "github_repo": "simcomm",
    "github_version": "main",
    "doc_path": "docs",
}
