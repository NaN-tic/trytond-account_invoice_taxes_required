# This file is part of the account_invoice_taxes_required module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoiceTaxesRequiredTestCase(ModuleTestCase):
    'Test Account Invoice Taxes Required module'
    module = 'account_invoice_taxes_required'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceTaxesRequiredTestCase))
    return suite