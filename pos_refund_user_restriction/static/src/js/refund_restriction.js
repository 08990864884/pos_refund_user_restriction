odoo.define("pos_refund_user_restriction.refund_restriction", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const TicketScreen = require("point_of_sale.TicketScreen");

    const RefundRestrictedTicketScreen = (TicketScreen) =>
        class extends TicketScreen {
            async _onDoRefund() {
                if (!this.env.pos.user.allow_pos_refund) {
                    await this.showPopup("ErrorPopup", {
                        title: this.env._t("Retur Tidak Diizinkan"),
                        body: this.env._t(
                            "User Anda tidak memiliki izin untuk melakukan retur POS."
                        ),
                    });
                    return;
                }
                return super._onDoRefund(...arguments);
            }
        };

    Registries.Component.extend(TicketScreen, RefundRestrictedTicketScreen);
});
