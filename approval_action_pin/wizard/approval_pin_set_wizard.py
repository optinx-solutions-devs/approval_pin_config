from odoo import _, fields, models
from odoo.exceptions import UserError, ValidationError


class ApprovalPinSetWizard(models.TransientModel):
    _name = "approval.pin.set.wizard"
    _description = "Set Approval PIN"

    user_id = fields.Many2one("res.users", required=True, readonly=True)
    new_pin = fields.Char(string="New PIN", required=True)
    confirm_pin = fields.Char(string="Confirm PIN", required=True)

    def action_set_pin(self):
        self.ensure_one()
        if self.new_pin != self.confirm_pin:
            raise ValidationError(_("PIN and confirmation PIN do not match."))
        if not self.user_id:
            raise UserError(_("Please choose a user."))
        self.user_id._set_approval_pin(self.new_pin)
        return {"type": "ir.actions.client", "tag": "reload"}
