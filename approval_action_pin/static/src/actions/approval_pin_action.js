/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ApprovalPinDialog } from "../components/approval_pin_dialog/approval_pin_dialog";

export function openApprovalPinDialog(env, action) {
    return new Promise((resolve) => {
        let settled = false;
        let handledSuccess = false;
        const cloneAction = (nextAction) => {
            if (!nextAction || typeof nextAction !== "object") {
                return nextAction;
            }
            try {
                return JSON.parse(JSON.stringify(nextAction));
            } catch {
                return { ...nextAction };
            }
        };
        const resolveOnce = (nextAction) => {
            if (settled) {
                return;
            }
            settled = true;
            resolve(cloneAction(nextAction) || { type: "ir.actions.act_window_close" });
        };
        env.services.dialog.add(
            ApprovalPinDialog,
            {
                wizardId: action.params.wizard_id,
                operationLabel: action.params.operation_label,
                userName: action.params.user_name,
                onSuccess: async (nextAction) => {
                    handledSuccess = true;
                    const clonedNextAction = cloneAction(nextAction);
                    if (clonedNextAction && typeof clonedNextAction === "object") {
                        await env.services.action.doAction(clonedNextAction);
                    } else {
                        await env.services.action.doAction({
                            type: "ir.actions.client",
                            tag: "soft_reload",
                        });
                    }
                    resolveOnce({ type: "ir.actions.act_window_close" });
                },
            },
            {
                onClose: () => {
                    if (!handledSuccess) {
                        resolveOnce({ type: "ir.actions.act_window_close" });
                    }
                },
            }
        );
    });
}

registry.category("actions").add("approval_action_pin.open_pin_dialog", openApprovalPinDialog);
