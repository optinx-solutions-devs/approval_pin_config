from odoo import _, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        if self.env.context.get("approval_pin_verified"):
            return super().button_validate()
        if not self.env["ir.config_parameter"].sudo().get_param("approval_action_pin.require_transfer_validate"):
            return super().button_validate()
        return self.env["approval.pin.verify.wizard"].action_open_for_operation(
            operation_label=_("Validate Transfer"),
            target_model=self._name,
            target_method="button_validate",
            records=self,
            context=dict(self.env.context),
        )

    def action_request_approval_pin_validate(self):
        return self.button_validate()
