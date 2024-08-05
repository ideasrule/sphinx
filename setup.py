import setuptools
from sphinx_interp import __version__, name

setuptools.setup(
    name = name,
    version = __version__,
    author = "Michael Zhang, Jegug Ih",
    author_email = "zmzhang@uchicago.edu",
    description = "A package to interpolate SPHINX stellar spectra",
    long_description = "",
    long_description_content_type = "text/markdown",
    url = "https://github.com/ideasrule/sphinx",
    packages = setuptools.find_packages(),
    classifiers = (
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        "numpy", "scipy", "setuptools_scm"]
)
