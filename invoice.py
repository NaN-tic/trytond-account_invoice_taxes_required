#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import copy
from trytond.model import ModelView, ModelSQL
from trytond.pyson import Eval


class InvoiceLine(ModelSQL, ModelView):
    _name = 'account.invoice.line'

    def __init__(self):
        super(InvoiceLine, self).__init__()
        self._constraints += [
            ('check_tax_required', 'tax_required')
            ]
        self.taxes = copy.copy(self.taxes)
        self.taxes.states = self.taxes.states.copy()
        self.taxes.states['required'] = Eval('type') == 'line'
        self._reset_columns()
        self._error_messages.update({
                'tax_required': 'All invoice lines must have at least one tax.',
                })

    def check_tax_required(self, ids):
        for line in self.browse(ids):
            if not line.taxes:
                return False
        return True

InvoiceLine()

