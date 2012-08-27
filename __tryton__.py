#This file is part account_invoice_taxes_required module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
{
    'name': 'Account Invoice Taxes Required',
    'version': '2.4.0',
    'author': 'NaN·tic',
    'email': 'info@NaN-tic.com',
    'website': 'http://www.tryton.org/',
    'description': 'This module ensures all invoice lines have at least one'
        'tax assigned.',
    'depends': [
        'ir',
        'account',
        'company',
        'party',
        'product',
        'res',
        'currency',
        'account_product',
        'account_invoice',
        ],
    'xml': [
        ],
    'translation': [
        'locale/ca_ES.po',
        ]
}
