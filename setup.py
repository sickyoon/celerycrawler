""" CeleryCrawler is benchmark project created to demonstrate GoCelery
"""

import codecs
from os import path
from setuptools import setup, find_packages

# Get the long description from the README file
with codecs.open(
    path.join(path.abspath(path.dirname(__file__)), 'README.md'),
    encoding='utf-8'
) as f:
    long_description = f.read()

setup(
    name='celerycrawler',
    version='0.0.1',
    description='A benchmark project created to demonstrate GoCelery',
    long_description=long_description,
    url='https://github.com/sickyoon/celerycrawler',
    author='Sick Yoon',
    author_email='sick.yoon@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='gocelery, celery, webcrawler, webspider, benchmark',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['peppercorn'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    }
)
