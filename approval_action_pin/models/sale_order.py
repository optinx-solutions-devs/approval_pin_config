from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_request_approval_pin_confirm(self):
        if self.env.context.get("approval_pin_verified"):
            return self.action_confirm()
        if not self.env["ir.config_parameter"].sudo().get_param("approval_action_pin.require_sale_confirm"):
            return self.action_confirm()
        return self.env["approval.pin.verify.wizard"].action_open_for_operation(
            operation_label=_("Confirm Sales Order"),
            target_model=self._name,
            target_method="action_confirm",
            records=self,
            context={"validate_analytic": True},
        )
