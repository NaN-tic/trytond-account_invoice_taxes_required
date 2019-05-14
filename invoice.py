# This file is part account_invoice_taxes_required module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['Invoice', 'InvoiceLine']


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

    @classmethod
    def validate(cls, lines):
        super(InvoiceLine, cls).validate(lines)
        for line in lines:
            line.check_tax_required()

    def check_tax_required(self):
        if not self.invoice or self.invoice.state in ('draft', 'cancel') or \
                self.type != 'line':
            return
        if not self.taxes:
            raise UserError(gettext(
                'account_invoice_taxes_required.tax_required',
                    line=self.rec_name,
                    invoice=(self.invoice.rec_name if self.invoice else '')))
