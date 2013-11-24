#This file is part account_invoice_taxes_required module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['InvoiceLine']
__metaclass__ = PoolMeta


class InvoiceLine:
    __name__ = 'account.invoice.line'

    @classmethod
    def __setup__(cls):
        super(InvoiceLine, cls).__setup__()
        cls._error_messages.update({
                'tax_required': ('Missing tax in line "%(line)s" in invoice '
                    '"%(invoice)s".'),
                })

    @classmethod
    def validate(cls, lines):
        super(InvoiceLine, cls).validate(lines)
        for line in lines:
            line.check_tax_required()

    def check_tax_required(self):
        if not self.invoice or self.invoice.state in ('draft', 'cancel'):
            return
        if not self.taxes:
            self.raise_user_error('tax_required', {
                    'line': self.line.rec_name,
                    'invoice': (self.line.invoice.rec_name if self.line.invoice
                        else '')
                    })
