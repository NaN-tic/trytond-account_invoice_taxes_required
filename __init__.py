# This file is part account_invoice_taxes_required module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import invoice
from . import sale
from . import purchase

def register():
    Pool.register(
        invoice.Invoice,
        invoice.InvoiceLine,
        module='account_invoice_taxes_required', type_='model')
    Pool.register(
        sale.Sale,
        sale.SaleLine,
        depends=['sale'],
        module='account_invoice_taxes_required', type_='model')
    Pool.register(
        purchase.Purchase,
        purchase.PurchaseLine,
        depends=['purchase'],
        module='account_invoice_taxes_required', type_='model')
