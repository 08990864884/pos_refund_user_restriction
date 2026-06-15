from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    allow_pos_refund = fields.Boolean(
        string="Boleh Retur POS",
        help="User ini dapat melihat dan menjalankan fungsi retur pada Point of Sale.",
    )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ["allow_pos_refund"]
