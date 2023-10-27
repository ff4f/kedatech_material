from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Material(models.Model):
    _name = 'material'
    _description = 'Material'
    _order = 'name'

    code = fields.Char(string='Material Code')
    name = fields.Char(string='Material Name')
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')], string='Material Type')
    price = fields.Float(string='Buy Price')
    partner_id = fields.Many2one('res.partner', string='Related Supplier')

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 100:
                raise ValidationError("Price should not be less than 100")
