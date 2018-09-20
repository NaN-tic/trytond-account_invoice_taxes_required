# This file is part of the account_invoice_taxes_required module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_teardown, doctest_checker


class AccountInvoiceTaxesRequiredTestCase(ModuleTestCase):
    'Test Account Invoice Taxes Required module'
    module = 'account_invoice_taxes_required'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceTaxesRequiredTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_invoice_taxes_required.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite
