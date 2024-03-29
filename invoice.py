# This file is part account_invoice_taxes_required module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError
from trytond.model import fields


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def validate(cls, invoices):
        InvoiceLine = Pool().get('account.invoice.line')

        super(Invoice, cls).validate(invoices)
        for invoice in invoices:
            InvoiceLine.validate(invoice.lines)


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'
    taxes_required = fields.Boolean('Taxes Required', readonly=True)

    @classmethod
    def default_taxes_required(cls):
        return True

    @classmethod
    def validate(cls, lines):
        super(InvoiceLine, cls).validate(lines)
        for line in lines:
            line.check_tax_required()

    def check_tax_required(self):
        if (not self.invoice
                or not self.taxes_required
                or self.invoice.state in ('draft', 'cancelled')
                or self.type != 'line'):
            return
        if not self.taxes:
            raise UserError(gettext(
                'account_invoice_taxes_required.tax_required',
                    line=self.rec_name.split(' @ ')[0],
                    invoice=(self.invoice.id if self.invoice else '')))
