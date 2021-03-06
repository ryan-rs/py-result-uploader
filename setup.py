#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

dependency_links = ['http://github.com/ryan-rs/qtest-swagger-client/tarball/master#egg=swagger-client-1.0.0']
requirements = ['Click>=6.0', 'swagger-client']
setup_requirements = ['pytest-runner']
test_requirements = ['pytest']

setup(
    author="rcbops",
    author_email='rcb-deploy@lists.rackspace.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Parse JUnitXML and convert into a qTest compliant JSON blob.",
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': [
            'py_result_uploader=py_result_uploader.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='py_result_uploader',
    name='py_result_uploader',
    packages=find_packages(include=['py_result_uploader']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rcbops/py-result-uploader',
    version='0.3.0',
    zip_safe=False,
)
