LONG_DESCRIPTION = """
This package provides interactive data visualization tools in the Jupyter
Notebook.

The interactive visualization tool that is provided allows data selection
through HTML widgets and outputs a Vega-lite plot through Altair. In the HTML
widget it is possible to select columns to plot in various encodings. This
widget also supports some basic configuration (i.e., log vs linear scales).
"""

DESCRIPTION         = "Altair Widgets: An interactive visualization for statistical data for Python."
NAME                = "altair_widgets"
PACKAGES            = ['altair_widgets']
AUTHOR              = "Scott Sievert"
AUTHOR_EMAIL        = "me@scottsievert.com"
URL                 = 'http://altair-viz.github.io'
DOWNLOAD_URL        = 'http://github.com/altair-viz/altair_widgets/'
LICENSE             = 'BSD 3-clause'
INSTALL_REQUIRES    = ['ipython', 'ipywidgets', 'pandas', 'altair',
                       'vega>=0.4.4']

import io
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def version(path):
    """Obtain the packge version from a python file e.g. pkg/__init__.py

    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = version('altair_widgets/__init__.py')


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      packages=PACKAGES,
      # package_data=PACKAGE_DATA,
      install_requires=INSTALL_REQUIRES,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'],
     )
