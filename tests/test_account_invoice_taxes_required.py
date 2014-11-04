#!/usr/bin/env python
# This file is part account_invoice_taxes_required module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_depends
from trytond.tests.test_tryton import doctest_setup, doctest_teardown


class AccountInvoiceTaxesRequiredTestCase(unittest.TestCase):
    'Test Account Invoice Taxes Required module'

    def setUp(self):
        trytond.tests.test_tryton.install_module(
            'account_invoice_taxes_required')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceTaxesRequiredTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_invoice_taxes_required.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
