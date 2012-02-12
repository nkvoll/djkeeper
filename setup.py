from setuptools import setup, find_packages


# make python setup.py test not spew errors (see http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
import sys
if 'test' in sys.argv:
    import multiprocessing


setup(
    name = "djkeeper",
    version = "0.2.1",

    author = 'Njal Karevoll',
    author_email = 'njal@karevoll.no',

    description = 'Utilities for using ZooKeeper from a Django project.',
    long_description = open('Readme.md').read(),

    license = 'MIT',

    keywords = 'zookeeper, pykeeper',

    url = 'http://github.com/nkvoll/djkeeper',

    # enable python setup.py nosetests
    setup_requires = ['nose'],
    test_suite = 'nose.collector',
    tests_require = ['mock'],

    requires = ['pykeeper'],

    packages = find_packages(),

    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django'
    ]
)
