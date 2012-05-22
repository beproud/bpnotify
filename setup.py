#!/usr/bin/env python
#:coding=utf-8:

from setuptools import setup, find_packages
 
setup (
    name='bpnotify',
    version='0.36',
    description='Notification routing for Django',
    author='Ian Lewis',
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
    include_package_data=True,
    packages=find_packages(),
    namespace_packages=['beproud', 'beproud.django'],
    test_suite='tests.main',
    install_requires=[
        'Django>=1.2.7',
        'django-jsonfield>=0.8.7',
    ],
    tests_require=[
        'mock>=0.7.2',
        'django-celery>=2.2.4',
    ],
    zip_safe=False,
)
