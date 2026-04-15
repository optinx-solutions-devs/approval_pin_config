import json

from odoo import _, fields, models
from odoo.exceptions import UserError


class ApprovalPinVerifyWizard(models.TransientModel):
    _name = "approval.pin.verify.wizard"
    _description = "Verify Approval PIN"

    pin = fields.Char(string="Approval PIN")
    operation_label = fields.Char(required=True, readonly=True)
    target_model = fields.Char(required=True, readonly=True)
    target_method = fields.Char(required=True, readonly=True)
    target_record_ids = fields.Char(required=True, readonly=True)
    target_context_json = fields.Text(readonly=True)
    execute_on_server = fields.Boolean(default=True, readonly=True)
    user_id = fields.Many2one(
        "res.users",
        string="Current User",
        default=lambda self: self.env.user,
        readonly=True,
    )

    @classmethod
    def _serialize_ids(cls, records):
        return ",".join(str(record_id) for record_id in records.ids)

    @classmethod
    def _deserialize_ids(cls, raw_ids):
        return [int(record_id) for record_id in (raw_ids or "").split(",") if record_id]

    @classmethod
    def _serialize_context(cls, context):
        return json.dumps(context or {})

    def action_open_for_operation(self, operation_label, target_model, target_method, records, context=None, execute_on_server=True):
        wizard = self.create({
            "operation_label": operation_label,
            "target_model": target_model,
            "target_method": target_method,
            "target_record_ids": self._serialize_ids(records),
            "target_context_json": self._serialize_context(context),
            "execute_on_server": execute_on_server,
        })
        return {
            "name": operation_label,
            "type": "ir.actions.client",
            "tag": "approval_action_pin.open_pin_dialog",
            "target": "new",
            "params": {
                "wizard_id": wizard.id,
                "operation_label": operation_label,
                "user_name": self.env.user.display_name,
                "target_model": target_model,
                "target_method": target_method,
                "target_record_ids": records.ids,
                "target_context": context or {},
                "execute_on_server": execute_on_server,
            },
        }

    def action_confirm_pin(self, pin=None):
        self.ensure_one()
        entered_pin = pin if pin is not None else self.pin
        if not entered_pin:
            raise UserError(_("Please enter your approval PIN."))
        if not self.env.user.approval_pin_hash:
            raise UserError(_("Your user does not have an approval PIN yet. Set one from the Users form first."))
        if not self.env.user._verify_approval_pin(entered_pin):
            raise UserError(_("Invalid approval PIN."))

        if not self.execute_on_server:
            return True

        target_context = json.loads(self.target_context_json or "{}")
        target_context["approval_pin_verified"] = True
        records = self.env[self.target_model].browse(self._deserialize_ids(self.target_record_ids)).exists()
        if not records:
            raise UserError(_("The target record could not be found anymore."))
        method = getattr(records.with_context(target_context), self.target_method)
        return method()
