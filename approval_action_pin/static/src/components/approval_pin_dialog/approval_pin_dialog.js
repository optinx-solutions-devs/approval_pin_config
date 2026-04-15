/** @odoo-module **/

import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class ApprovalPinDialog extends Component {
    static template = "approval_action_pin.ApprovalPinDialog";
    static components = { Dialog };
    static props = {
        close: Function,
        wizardId: Number,
        operationLabel: String,
        userName: String,
        onSuccess: Function,
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.pinInputRef = useRef("pinInput");
        this.state = useState({
            pin: "",
            showPin: false,
            isProcessing: false,
            error: "",
            isShaking: false,
        });

        onMounted(() => {
            this.pinInputRef.el?.focus();
        });
    }

    get maskedPreview() {
        return this.state.pin ? "•".repeat(this.state.pin.length) : "• • • •";
    }

    get secureApprovalLabel() {
        return _t("Secure Approval");
    }

    get approvalPinLabel() {
        return _t("Approval PIN");
    }

    get pinPlaceholder() {
        return _t("Enter Pin");
    }

    get digitsHintLabel() {
        return _t("Digits only (Numbers)");
    }

    get visibilityLabel() {
        return this.state.showPin ? _t("Hide") : _t("Show");
    }

    get subtitleLabel() {
        return _t("Enter the approval PIN for %s.", this.props.userName);
    }

    get confirmLabel() {
        return this.state.isProcessing ? _t("Checking...") : _t("Confirm");
    }

    onInput(ev) {
        this.state.pin = (ev.target.value || "").replace(/\D/g, "").slice(0, 8);
        if (this.state.error) {
            this.state.error = "";
        }
    }

    onKeydown(ev) {
        if (ev.key === "Enter") {
            ev.preventDefault();
            this.confirm();
        }
    }

    toggleVisibility() {
        this.state.showPin = !this.state.showPin;
        this.pinInputRef.el?.focus();
    }

    showInlineError(message) {
        this.state.error = message;
        this.state.isShaking = true;
        window.setTimeout(() => {
            this.state.isShaking = false;
        }, 420);
    }

    async confirm() {
        if (this.state.isProcessing) {
            return;
        }
        if (!this.state.pin) {
            this.showInlineError(_t("Please enter your approval PIN."));
            this.pinInputRef.el?.focus();
            return;
        }
        this.state.isProcessing = true;
        try {
            const result = await this.orm.call(
                "approval.pin.verify.wizard",
                "action_confirm_pin",
                [[this.props.wizardId], this.state.pin]
            );
            await this.props.onSuccess(result);
            this.props.close();
        } catch (error) {
            this.state.pin = "";
            const message = error?.data?.message || error?.message || "";
            if (
                message.includes("Invalid approval PIN") ||
                message.includes("Please enter your approval PIN")
            ) {
                this.showInlineError(_t("Wrong PIN. Please try again."));
                this.pinInputRef.el?.focus();
                return;
            }
            this.pinInputRef.el?.focus();
            throw error;
        } finally {
            this.state.isProcessing = false;
        }
    }

    cancel() {
        this.props.close();
    }
}
