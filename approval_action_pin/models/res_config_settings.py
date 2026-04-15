from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    approval_pin_required_sale_confirm = fields.Boolean(
        string="Sales Order Confirmation",
        config_parameter="approval_action_pin.require_sale_confirm",
    )
    approval_pin_required_invoice_post = fields.Boolean(
        string="Invoice Confirmation",
        config_parameter="approval_action_pin.require_invoice_post",
    )
    approval_pin_required_transfer_validate = fields.Boolean(
        string="Transfer Validation",
        config_parameter="approval_action_pin.require_transfer_validate",
    )
    approval_pin_required_payment_register = fields.Boolean(
        string="Register Payment",
        config_parameter="approval_action_pin.require_payment_register",
    )
