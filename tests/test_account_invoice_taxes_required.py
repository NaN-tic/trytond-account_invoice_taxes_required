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
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, \
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
        self.account_type = POOL.get('account.account.type')
        self.ir_sequence = POOL.get('ir.sequence')
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
            currency, = self.currency.create([{
                        'name': 'A',
                        'symbol': 'A',
                        'code': 'A'
                        }])
            party, = self.party.create([{
                        'name': 'Company',
                        }])
            company, = self.company.create([{
                        'party': party.id,
                        'currency': currency.id,
                        }])
            user = self.user.search([('id', '=', USER)])
            self.user.write(user, {
                    'main_company': company,
                    'company': company,
                    })
            self.journal_type.create([{
                        'name': 'A',
                        'code': 'A',
                        }])
            sequence, = self.ir_sequence.create([{
                        'name': 'A',
                        'code': 'account.journal',
                        'padding': 3,
                        'number_increment': 1,
                        }])
            journal, = self.journal.create([{
                        'name': 'A',
                        'type': 'A',
                        'sequence': sequence.id,
                        }])
            tax, = self.account_tax.create([{
                        'name': 'Tax',
                        'description': 'Tax',
                        'sequence': 1,
                        'type': 'none',
                        'company': company,
                        }])
            term, = self.payment_term.create([{
                        'name': '30 days',
                        'lines': [
                            ('create', [{
                                    'sequence': 1,
                                    'type': 'remainder',
                                    'months': 1,
                                    }])]
                        }])
            account_type, = self.account_type.create([{
                        'name': 'Payable type',
                        'company': company,
                        'display_balance': 'debit-credit',
                        }])
            payable_account, = self.account.create([{
                        'name': 'Payable',
                        'code': '',
                        'kind': 'payable',
                        'company': company,
                        'type': account_type,
                        }])
            receivable_account, = self.account.create([{
                        'name': 'Receivable',
                        'code': '',
                        'kind': 'receivable',
                        'company': company,
                        'type': account_type,
                        }])
            party, = self.party.create([{
                        'name': 'Name',
                        'account_payable': payable_account.id,
                        'account_receivable': receivable_account.id,
                        }])
            revenue_account, = self.account.create([{
                        'name': 'Revenue',
                        'code': '',
                        'kind': 'revenue',
                        'company': company,
                        'type': account_type,
                        }])
            invoice, = self.invoice.create([{
                        'party': party.id,
                        'currency': currency,
                        'account': receivable_account.id,
                        'invoice_address': party.addresses[0].id,
                        'type': 'out_invoice',
                        'company': company,
                        'payment_term': term,
                        'journal': journal,
                        }])
            self.invoice_line.create([{
                        'invoice': invoice.id,
                        'company': company.id,
                        'description': 'A',
                        'quantity': 1,
                        'unit_price': 1,
                        'account': revenue_account.id,
                        'taxes': [
                            ('add', [tax])
                            ],
                        }])
            self.assertRaises(Exception, self.invoice_line.create, [{
                        'invoice': invoice.id,
                        'company': company.id,
                        'description': 'A',
                        'quantity': 1,
                        'unit_price': 1,
                        'account': revenue_account.id,
                        }])

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceTaxesRequiredTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
