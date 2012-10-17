#This file is part account_invoice_taxes_required module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
import copy
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['InvoiceLine']
__metaclass__ = PoolMeta

class InvoiceLine:
    'Invoice Line'
    __name__ = 'account.invoice.line'

    @classmethod
    def __setup__(cls):
        super(InvoiceLine, cls).__setup__()
        cls._constraints += [
            ('check_tax_required', 'tax_required')
            ]
        cls.taxes = copy.copy(cls.taxes)
        cls.taxes.states = cls.taxes.states.copy()
        cls.taxes.states['required'] = Eval('type') == 'line'
        cls._error_messages.update({
                'tax_required': 'All invoice lines must have at least one tax.',
                })

    def check_tax_required(self):
        if not self.taxes:
            return False
        return True
