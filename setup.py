#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="appdotnet",
    version="0.0.1",
    packages=find_packages(),

    install_requires=['requests'],

    author="Simon de la Rouviere",
    author_email="simon@delarouviere.com",
    description="A simple wrapper for App.net's API.",
    license="TODO",
    keywords="microblog social api",
    url="https://github.com/simondlr/Python-App.net-API-Wrapper",

    classifiers=[
        "Development Status :: 3 - Alpha",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python'],
)
