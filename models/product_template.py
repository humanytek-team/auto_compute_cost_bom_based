from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends('product_variant_ids', 'product_variant_ids.standard_price', 'product_variant_count')
    def _compute_standard_price(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.standard_price = template.product_variant_ids.standard_price
        for template in (self - unique_variants):
            template.standard_price = 0.0
        for template in self:
            if template.product_variant_count == 1:
                product = template.product_variant_id
                bom = self.env['mrp.bom']._bom_find(product=product)
                if bom:
                    price = product._calc_price(bom)
                    template.standard_price = price
