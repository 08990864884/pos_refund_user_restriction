from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class PosOrder(models.Model):
    _inherit = "pos.order"

    user_can_refund = fields.Boolean(
        string="User Boleh Retur",
        compute="_compute_user_can_refund",
        compute_sudo=False,
    )

    @api.depends_context("uid")
    def _compute_user_can_refund(self):
        allowed = self.env.user.allow_pos_refund
        for order in self:
            order.user_can_refund = allowed

    def _ensure_pos_refund_allowed(self):
        if not self.env.user.allow_pos_refund:
            raise AccessError(
                _(
                    "Anda tidak memiliki izin untuk melakukan retur POS. "
                    "Hubungi administrator untuk mengaktifkan hak Boleh Retur POS."
                )
            )

    @api.model
    def _check_pos_refund_permission(self, orders):
        if self.env.user.allow_pos_refund:
            return

        for order in orders:
            for line_command in order.get("data", {}).get("lines", []):
                line_values = (
                    line_command[2]
                    if isinstance(line_command, (list, tuple))
                    and len(line_command) > 2
                    and isinstance(line_command[2], dict)
                    else {}
                )
                if line_values.get("refunded_orderline_id"):
                    self._ensure_pos_refund_allowed()

    @api.model
    def create_from_ui(self, orders, draft=False):
        self._check_pos_refund_permission(orders)
        return super().create_from_ui(orders, draft=draft)

    def refund(self):
        self._ensure_pos_refund_allowed()
        return super().refund()
