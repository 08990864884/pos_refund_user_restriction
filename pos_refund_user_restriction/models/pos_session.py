from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_res_users(self):
        result = super()._loader_params_res_users()
        fields = result["search_params"]["fields"]
        if "allow_pos_refund" not in fields:
            fields.append("allow_pos_refund")
        return result
