{
    "name": "POS Refund User Restriction",
    "version": "16.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Batasi retur POS hanya untuk user yang dipilih",
    "license": "LGPL-3",
    "images": [
        "static/description/cover.png",
        "static/description/banner.png",
    ],
    "depends": ["point_of_sale"],
    "data": [
        "views/res_users_views.xml",
        "views/pos_order_views.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_refund_user_restriction/static/src/js/refund_restriction.js",
            "pos_refund_user_restriction/static/src/xml/refund_restriction.xml",
        ],
    },
    "installable": True,
    "application": False,
}
