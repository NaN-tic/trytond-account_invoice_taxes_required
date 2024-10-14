# This file is part account_invoice_taxes_required module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError
from trytond.model import fields


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def quote(cls, sales):
        SaleLine = Pool().get('sale.line')

        super().quote(sales)
        for sale in sales:
            SaleLine.validate(sale.lines)


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'
    taxes_required = fields.Function(fields.Boolean('Taxes Required'),
        'on_change_with_taxes_required')

    @fields.depends('type')
    def on_change_with_taxes_required(self, name=None):
        InvoiceLine = Pool().get('account.invoice.line')

        return (InvoiceLine.default_taxes_required()
            if self.type == 'line' else False)

    @fields.depends('type')
    def on_change_type(self):
        if self.type != 'line':
            self.taxes_required = False
        super().on_change_type()

    @classmethod
    def validate(cls, lines):
        super().validate(lines)
        for line in lines:
            line.check_tax_required()

    def check_tax_required(self):
        if (not self.sale
                or not self.taxes_required
                or self.sale.state in ('draft', 'cancelled')
                or self.type != 'line'):
            return
        if not self.taxes:
            raise UserError(gettext(
                'account_invoice_taxes_required.msg_missing_taxes',
                    line=self.rec_name.split(' @ ')[0],
                    record=self.sale.rec_name))
