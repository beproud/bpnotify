#!/usr/bin/env python
#:coding=utf-8:

from setuptools import setup, find_packages

setup(
    name='bpnotify',
    version='0.42',
    description='Notification routing for Django',
    author='Ian Lewis',
    author_email='ian@beproud.jp',
    url='https://github.com/beproud/bpnotify/',
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
        'Django>=1.2,<1.8',
        'django-jsonfield>=0.8.7,<1.0',
    ],
    tests_require=[
        'celery>=2.2.7,<4.0',
        'mock>=0.7.2',
    ],
    zip_safe=False,
)
