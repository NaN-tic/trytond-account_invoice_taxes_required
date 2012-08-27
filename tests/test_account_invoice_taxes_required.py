#!/usr/bin/env python
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

import sys
import os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import unittest
import datetime
from decimal import Decimal
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
        test_depends
from trytond.transaction import Transaction


class AccountInvoiceTaxesRequiredTestCase(unittest.TestCase):
    '''
    Test AccountInvoice module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('account_invoice_taxes_required')
        self.payment_term = POOL.get('account.invoice.payment_term')
        self.company = POOL.get('company.company')
        self.currency = POOL.get('currency.currency')
        self.invoice = POOL.get('account.invoice')
        self.invoice_line = POOL.get('account.invoice.line')
        self.party = POOL.get('party.party')
        self.account_tax = POOL.get('account.tax')
        self.account = POOL.get('account.account')
        self.journal = POOL.get('account.journal')
        self.journal_type = POOL.get('account.journal.type')
        self.user = POOL.get('res.user')

    def test0006depends(self):
        '''
        Test depends.
        '''
        test_depends()

    def test0010taxes_required(self):
        '''
        Test taxes required
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            currency_id = self.currency.create({
                    'name': 'A',
                    'symbol': 'A',
                    'code': 'A'
                    })
            company_id = self.company.create({
                    'name': 'Company',
                    'currency': currency_id,
                    })
            self.user.write(USER, {
                    'main_company': company_id,
                    'company': company_id,
                    })
            type_id = self.journal_type.create({
                    'name': 'A',
                    'code': 'A',
                    })
            journal_id = self.journal.create({
                    'name': 'A',
                    'type': 'A',
                    })

            tax_id = self.account_tax.create({
                    'name': 'Tax',
                    'description': 'Tax',
                    'sequence': 1,
                    'type': 'none',
                    'company': company_id,
                    })

            term_id = self.payment_term.create({
                    'name': '30 days',
                    'lines': [
                        ('create', {
                                'sequence': 1,
                                'type': 'remainder',
                                'months': 1,
                                })]
                    })
            party_id = self.party.create({
                    'name': 'Name',
                    })
            party = self.party.browse(party_id)
            receivable_account_id = self.account.create({
                    'name': 'Receivable',
                    'code': '',
                    'kind': 'receivable',
                    'company': company_id,
                    })
            revenue_account_id = self.account.create({
                    'name': 'Revenue',
                    'code': '',
                    'kind': 'revenue',
                    'company': company_id,
                    })

            invoice_id = self.invoice.create({
                    'party': party_id,
                    'currency': currency_id,
                    'account': receivable_account_id,
                    'invoice_address': party.addresses[0].id, 
                    'type': 'out_invoice',
                    'company': company_id,
                    'payment_term': term_id,
                    'journal': journal_id,
                    })
            self.invoice_line.create({
                    'invoice': invoice_id,
                    'company': company_id,
                    'description': 'A',
                    'quantity': 1,
                    'unit_price': 1,
                    'account': revenue_account_id,
                    'taxes': [
                        ('add', [tax_id])
                        ],
                    })
            self.assertRaises(Exception, self.invoice_line.create, {
                    'invoice': invoice_id,
                    'company': company_id,
                    'description': 'A',
                    'quantity': 1,
                    'unit_price': 1,
                    'account': revenue_account_id,
                    })

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceTaxesRequiredTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
