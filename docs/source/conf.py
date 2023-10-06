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

master_doc = "index"
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
html_title = ""
html_static_path = ["_static"]
html_show_sourcelink = False
html_show_sphinx = False
html_favicon = "./_static/favicon.ico"
html_logo = "./_static/fav.svg"
html_static_path = ["_static"]
html_js_files = ["custom-icon.js"]
html_css_files = [
    "simcomm.css",
]

# json_url = "https://raw.githubusercontent.com/muhd-umer/simcomm/main/docs/source/_static/switcher.json"

# if "dev" in release or "rc" in release:
#     version_match = "dev"
#     json_url = "_static/switcher.json"
# else:
#     version_match = "v" + release

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/muhd-umer/simcomm",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/simcomm/",
            "icon": "https://pypi.org/static/images/logo-small.2a411bc6.svg",
            "type": "url",
        },
    ],
    # "logo": {
    #     "text": "SimComm",
    #     "image_dark": "_static/fav.svg",
    #     "alt_text": "SimComm",
    # },
    "footer_start": ["copyright"],
    "navbar_start": ["navbar-logo"],
    "navbar_align": "left",
    "navbar_center": ["navbar-nav"],
    # "navbar_center": ["navbar-nav"],
    # "switcher": {
    #     "json_url": json_url,
    #     "version_match": version_match,
    # },
    "show_toc_level": 3,
    "show_nav_level": 3,
}

html_context = {
    "github_user": "muhd-umer",
    "github_repo": "simcomm",
    "github_version": "main",
    "doc_path": "docs",
    "default_mode": "light",
}

html_extra_path = ["_extra/googlee67cda8bc2355b91.html"]
html_baseurl = "https://simcomm.readthedocs.io/en/latest/"

# -- Options for autosummary/autodoc output ------------------------------------
autosummary_generate = True

# -- Options for autoapi -------------------------------------------------------

# Optionally disable autoapi generation for all files in a directory
autoapi_generate_api_docs = True
autoapi_type = "python"
autoapi_dirs = ["../../simcomm"]
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
# autodoc_type_aliases = {"NDArray": "NDArray"}
python_use_unqualified_type_names = True


def skip_submodules(app, what, name, obj, skip, options):
    if what == "module":
        skip = True
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_submodules)
