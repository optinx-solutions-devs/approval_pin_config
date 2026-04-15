from odoo import _, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def action_create_payments(self):
        if self.env.context.get("approval_pin_verified"):
            return super().action_create_payments()
        if not self.env["ir.config_parameter"].sudo().get_param("approval_action_pin.require_payment_register"):
            return super().action_create_payments()
        return self.env["approval.pin.verify.wizard"].action_open_for_operation(
            operation_label=_("Register Payment"),
            target_model=self._name,
            target_method="action_create_payments",
            records=self,
            context=dict(self.env.context),
        )

    def action_request_approval_pin_create_payments(self):
        return self.action_create_payments()
