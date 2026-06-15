from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestPosRefundRestriction(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        pos_group = cls.env.ref("point_of_sale.group_pos_user")
        cls.restricted_user = cls.env["res.users"].create(
            {
                "name": "Kasir Tanpa Retur",
                "login": "pos_no_refund",
                "groups_id": [(6, 0, pos_group.ids)],
                "allow_pos_refund": False,
            }
        )
        cls.allowed_user = cls.env["res.users"].create(
            {
                "name": "Kasir Dengan Retur",
                "login": "pos_with_refund",
                "groups_id": [(6, 0, pos_group.ids)],
                "allow_pos_refund": True,
            }
        )
        cls.refund_payload = [
            {
                "data": {
                    "lines": [
                        [
                            0,
                            0,
                            {
                                "product_id": 1,
                                "qty": -1,
                                "refunded_orderline_id": 10,
                            },
                        ]
                    ]
                }
            }
        ]

    def test_restricted_user_cannot_refund(self):
        with self.assertRaises(AccessError):
            self.env["pos.order"].with_user(
                self.restricted_user
            )._check_pos_refund_permission(self.refund_payload)

    def test_selected_user_can_refund(self):
        self.env["pos.order"].with_user(
            self.allowed_user
        )._check_pos_refund_permission(self.refund_payload)

    def test_backend_refund_requires_permission(self):
        with self.assertRaises(AccessError):
            self.env["pos.order"].with_user(
                self.restricted_user
            )._ensure_pos_refund_allowed()

        self.env["pos.order"].with_user(
            self.allowed_user
        )._ensure_pos_refund_allowed()

    def test_normal_sale_remains_allowed(self):
        sale_payload = [
            {
                "data": {
                    "lines": [
                        [0, 0, {"product_id": 1, "qty": 1}],
                    ]
                }
            }
        ]
        self.env["pos.order"].with_user(
            self.restricted_user
        )._check_pos_refund_permission(sale_payload)

    def test_permission_is_loaded_to_pos(self):
        params = self.env["pos.session"]._loader_params_res_users()
        self.assertIn("allow_pos_refund", params["search_params"]["fields"])
