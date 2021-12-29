"""Packaging."""
from codecs import open
from os.path import abspath
from os.path import dirname
from os.path import join
from subprocess import call

from setuptools import Command
from setuptools import find_packages
from setuptools import setup

from convert import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""

    description = "run tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(["py.test", "--cov=converter-cli", "--cov-report=term-missing"])
        raise SystemExit(errno)


setup(
    name="mytools",
    version=__version__,
    description="A linux file log converter command line program in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williamchand/mytens-mytools",
    author="William chandra",
    author_email="williamchans57@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: Public Domain",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="cli, log, linux, mytools",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=["docopt"],
    extras_require={
        "test": ["coverage", "pytest", "pytest-cov", "mock"],
    },
    entry_points={
        "console_scripts": [
            "mytools=convert.cli:main",
        ],
    },
    cmdclass={"test": RunTests},
)
