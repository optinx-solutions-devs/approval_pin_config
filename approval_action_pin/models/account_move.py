from odoo import _, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_request_approval_pin_post(self):
        if self.env.context.get("approval_pin_verified"):
            return self.action_post()
        requires_pin = self.env["ir.config_parameter"].sudo().get_param("approval_action_pin.require_invoice_post")
        if not requires_pin or not self.filtered(lambda move: move.is_invoice(include_receipts=True)):
            return self.action_post()
        return self.env["approval.pin.verify.wizard"].action_open_for_operation(
            operation_label=_("Confirm Invoice"),
            target_model=self._name,
            target_method="action_post",
            records=self,
            context={"validate_analytic": True},
        )
