import re

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


PIN_REGEX = re.compile(r"^\d{4,8}$")


class ResUsers(models.Model):
    _inherit = "res.users"

    approval_pin_hash = fields.Char(copy=False)
    approval_pin_is_set = fields.Boolean(
        string="Approval PIN Set",
        compute="_compute_approval_pin_is_set",
    )

    @api.depends("approval_pin_hash")
    def _compute_approval_pin_is_set(self):
        for user in self:
            user.approval_pin_is_set = bool(user.approval_pin_hash)

    def _check_can_manage_approval_pin(self):
        self.ensure_one()
        if self == self.env.user:
            return
        if not self.env.user.has_group("base.group_system"):
            raise AccessError(_("Only administrators can manage another user's approval PIN."))

    def _validate_approval_pin_format(self, pin):
        if not PIN_REGEX.match(pin or ""):
            raise ValidationError(_("Approval PIN must contain only 4 to 8 digits."))

    def _set_approval_pin(self, pin):
        self.ensure_one()
        self._check_can_manage_approval_pin()
        self._validate_approval_pin_format(pin)
        self.sudo().write({
            "approval_pin_hash": self._crypt_context().hash(pin),
        })

    def _clear_approval_pin(self):
        self.ensure_one()
        self._check_can_manage_approval_pin()
        self.sudo().write({"approval_pin_hash": False})

    def _verify_approval_pin(self, pin):
        self.ensure_one()
        hashed = self.sudo().approval_pin_hash
        if not hashed:
            return False
        valid, replacement = self._crypt_context().verify_and_update(pin, hashed)
        if valid and replacement:
            self.sudo().write({"approval_pin_hash": replacement})
        return valid

    def action_open_set_approval_pin_wizard(self):
        self.ensure_one()
        self._check_can_manage_approval_pin()
        view = self.env.ref("approval_action_pin.approval_pin_set_wizard_view_form")
        return {
            "name": _("Set Approval PIN"),
            "type": "ir.actions.act_window",
            "res_model": "approval.pin.set.wizard",
            "view_mode": "form",
            "view_id": view.id,
            "target": "new",
            "context": {
                "default_user_id": self.id,
            },
        }

    def action_clear_approval_pin(self):
        self.ensure_one()
        if not self.env.user.has_group("base.group_system"):
            raise UserError(_("Only administrators can clear an approval PIN."))
        self._clear_approval_pin()
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
