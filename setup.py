#!/usr/bin/env python
#This file is part account_invoice_taxes_required module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from setuptools import setup
import re
import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)


requires = ['python-dateutil']
for dep in info.get('depends', []):
    if not re.match(r'(ir|res|workflow|webdav)(\W|$)', dep):
        requires.append('trytond_%s >= %s.%s, < %s.%s' %
                (dep, major_version, minor_version, major_version,
                    minor_version + 1))
requires.append('trytond >= %s.%s, < %s.%s' %
        (major_version, minor_version, major_version, minor_version + 1))

setup(name='trytonzz_account_invoice_taxes_required',
    version=info.get('version', '0.0.1'),
    description='Account Invoice Taxes Required',
    author='NaN·tic',
    author_email='info@NaN-tic.com',
    url='http://www.nan-tic.com',
    download_url="https://bitbucket.org/zikzakmedia/trytond-account_invoice_taxes_required",
    package_dir={'trytond.modules.account_invoice_taxes_required': '.'},
    packages=[
        'trytond.modules.account_invoice_taxes_required',
        'trytond.modules.account_invoice_taxes_required.tests',
        ],
    package_data={
        'trytond.modules.account_invoice_taxes_required': info.get('xml', []) \
            + ['tryton.cfg', 'locale/*.po'],
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
    license='GPL-3',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    account_invoice_taxes_required = trytond.modules.account_invoice_taxes_required
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
)
