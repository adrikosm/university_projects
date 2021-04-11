# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Project information -----------------------------------------------------

project = 'Σχεδίαση Βάσεων Δεδομένων και Κατανεμημένες ΒΔ'
copyright = '2019, Ηαροκόπειο Πανεπιστήμιο'
author = 'Ιωάννης Σομός, Ευάγγελος Κοντός, Ανδρέας Μαυρόπουλος'
version = ''
release = ''

# -- General configuration ---------------------------------------------------

extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = 'el'
exclude_patterns = ['_build', '.directory']
pygments_style = 'manni'
highlight_language = 'sql'

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_title = '2η Εργασία'
html_static_path = ['_static']
html_theme_options = {'nosidebar': True}

# -- Options for LaTeX output ------------------------------------------------

latex_engine = 'xelatex'
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '12pt',
    'figure_align': 'htbp',
    'babel': r'\usepackage[greek,english]{babel}',
    "fontpkg": r"""
\setmainfont{Lato}
\setsansfont{Lato}
\setmonofont{Hack}
    """,
}
latex_documents = [('Assignment2', 'Assignment2.tex', '', author, 'manual')]

