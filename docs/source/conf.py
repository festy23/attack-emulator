# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))  # Укажите правильный путь к папке с app.py

project = 'Эмулятор атак на веб-приложение'
copyright = '2024, Артур Иванов'
author = 'Артур Иванов'
release = '1.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # Автодокументация
    'sphinx.ext.napoleon', # Поддержка Google и NumPy стилей
    'sphinx.ext.viewcode', # Ссылка на исходный код
]

templates_path = ['_templates']
exclude_patterns = []
html_use_modindex = False
language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']