import unittest
from decimal import Decimal

from proteus import Model
from trytond.model.exceptions import ValidationError
from trytond.modules.account.tests.tools import (create_chart,
                                                 create_fiscalyear, create_tax,
                                                 get_accounts)
from trytond.modules.account_invoice.tests.tools import (
    create_payment_term, set_fiscalyear_invoice_sequences)
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Install account_invoice_taxes_required and sale Module
        activate_modules(['account_invoice_taxes_required', 'sale'])

        # Create company
        _ = create_company()
        company = get_company()

        # Create fiscal year
        fiscalyear = set_fiscalyear_invoice_sequences(
            create_fiscalyear(company))
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)
        accounts = get_accounts(company)
        revenue = accounts['revenue']
        expense = accounts['expense']

        # Create tax
        tax = create_tax(Decimal('.10'))
        tax.save()

        # Create party
        Party = Model.get('party.party')
        party = Party(name='Party')
        party.save()

        # Create account categories
        ProductCategory = Model.get('product.category')
        account_category = ProductCategory(name="Account Category")
        account_category.accounting = True
        account_category.account_expense = expense
        account_category.account_revenue = revenue
        account_category.save()
        account_category_tax, = account_category.duplicate()
        account_category_tax.customer_taxes.append(tax)
        account_category_tax.save()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'service'
        template.salable = True
        template.list_price = Decimal('40')
        template.account_category = account_category_tax
        product, = template.products
        product.cost_price = Decimal('25')
        template.save()
        product, = template.products

        # Create payment term
        payment_term = create_payment_term()
        payment_term.save()

        # Create invoice Without Taxes
        Sale = Model.get('sale.sale')
        sale = Sale()
        sale.party = party
        sale.payment_term = payment_term
        line = sale.lines.new()
        line.product = product
        line.quantity = 5
        line.unit_price = Decimal(40)
        line = sale.lines.new()
        line.description = 'Test'
        line.quantity = 1
        line.unit_price = Decimal(20)
        self.assertEqual(line.taxes_required, True)
        self.assertEqual(sale.untaxed_amount, Decimal('220.00'))
        self.assertEqual(sale.tax_amount, Decimal('20.00'))
        self.assertEqual(sale.total_amount, Decimal('240.00'))
        sale.save()

        with self.assertRaises(ValidationError):
            sale.click('quote')

        sale.reload()
        self.assertEqual(sale.state, 'draft')

        # Create sale With Taxes
        sale = Sale()
        sale.party = party
        sale.payment_term = payment_term
        line = sale.lines.new()
        line.product = product
        line.quantity = 5
        line.unit_price = Decimal(20)
        line = sale.lines.new()
        self.assertEqual(line.taxes_required, True)
        line.type = 'comment'
        self.assertEqual(line.taxes_required, False)
        line.description = 'Test'
        sale.click('quote')
        self.assertEqual(sale.state, 'quotation')
