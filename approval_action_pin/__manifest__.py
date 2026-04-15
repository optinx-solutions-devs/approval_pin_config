{
    "name": "PIN Approval for Secure Actions",
    "summary": "Secure sales, invoices, transfers, and payments with user PIN approval",
    "description": """
        PIN Approval adds an approval popup before key Odoo actions.

        Main features:
        - Require a PIN before confirming Sales Orders.
        - Require a PIN before confirming customer/vendor invoices.
        - Require a PIN before validating Inventory Transfers.
        - Require a PIN before creating payments from Register Payment.
        - Configure each protected action from Settings.
        - Manage approval PINs per backend user.
        """,
    "version": "17.0.1.0.0",
    "category": "Tools",
    "author": "Optin Solutions",
    # "website": "https://www.optinsolutions.com",
    "support": "optinassist@gmail.com",
    "price": 21.9,
    "currency": "USD",
    "license": "LGPL-3",
    "depends": [
        "base_setup",
        "sale",
        "account",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/res_users_views.xml",
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "views/stock_picking_views.xml",
        "views/account_payment_register_views.xml",
        "wizard/approval_pin_set_wizard_views.xml",
        "wizard/approval_pin_verify_wizard_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "approval_action_pin/static/src/actions/approval_pin_action.js",
            "approval_action_pin/static/src/components/approval_pin_dialog/approval_pin_dialog.js",
            "approval_action_pin/static/src/components/approval_pin_dialog/approval_pin_dialog.xml",
            "approval_action_pin/static/src/scss/approval_pin.scss",
        ],
    },
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
