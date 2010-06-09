#!/usr/bin/env python
#:coding=utf-8:

from setuptools import setup, find_packages
 
setup (
    name='bpnotify',
    version='0.1',
    description='Nofication routing for Django',
    author='K.K. BeProud',
    author_email='ian@beproud.jp',
    url='https://project.beproud.jp/hg/bpnotify/',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Plugins',
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=["notify"],
    test_suite='tests.main',
)
