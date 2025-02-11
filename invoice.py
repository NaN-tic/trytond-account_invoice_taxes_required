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

        super().validate(invoices)
        for invoice in invoices:
            InvoiceLine.validate(invoice.lines)


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'
    taxes_required = fields.Boolean('Taxes Required', readonly=True)

    @classmethod
    def default_taxes_required(cls):
        return True

    @fields.depends('type')
    def on_change_type(self):
        if self.type != 'line':
            self.taxes_required = False
        try:
            super().on_change_type()
        except AttributeError:
            pass

    @classmethod
    def validate(cls, lines):
        super().validate(lines)
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
                'account_invoice_taxes_required.msg_missing_taxes',
                    line=self.rec_name.split(' @ ')[0],
                    record=self.invoice.rec_name))
