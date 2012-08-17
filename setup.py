#!/usr/bin/python
import os, sys, glob

from distutils.core import setup
from distutils.extension import Extension
from setuptools import find_packages

name = 'appdotnet'
version = '0.1'


cmdclass = {}
ext_modules = []

metadata = {'name':name,
            'version': version,
            'cmdclass': cmdclass,
            'ext_modules': ext_modules,
            'description':'appdotnet',
            'author':'',
            'py_modules':['appdotnet',],
            'requires':[
                'request',
                ],
            'install_requires':[
                ],
}


if __name__ == '__main__':
    dist = setup(**metadata)
