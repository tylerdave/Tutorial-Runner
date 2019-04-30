#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=6.0", "pytoml", "pytest>=3.5.0" ,"pytest-clarity"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Dave Forgac",
    author_email="tylerdave@tylerdave.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="A command line interface for running tutorial lessons.",
    entry_points={
        "console_scripts": [
            "tutorial=tutorial_runner.cli:tutorial",
            "tutorial-runner=tutorial_runner.cli:tutorial",
        ]
    },
    install_requires=requirements,
    license="MPL 2.0",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="tutorial_runner",
    name="tutorial-runner",
    packages=find_packages(include=["tutorial_runner"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tylerdave/tutorial-runner",
    version="0.2.5",
    zip_safe=False,
)
