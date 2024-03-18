from odoo import models, fields


class BlendxIntent(models.Model):
    _name = "blendx.intent"
    _description = "Blendx Intent"
    _rec_name = "blendx_intent_name"

    blendx_intent_name = fields.Char(string='Name')
    blendx_intent_deprecated = fields.Boolean(string='Deprecated')
