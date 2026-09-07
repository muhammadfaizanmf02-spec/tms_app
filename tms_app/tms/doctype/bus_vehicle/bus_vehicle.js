// Copyright (c) 2026, Your Company and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bus Vehicle", {
	refresh(frm) {
		if (!frm.doc.asset && !frm.is_new()) {
			frm.add_custom_button(__("Create Asset"), () => {
				frappe.confirm(
					__("Create an Item + Asset record for this vehicle and link it back here?"),
					() => {
						frm.call("create_asset").then(() => frm.reload_doc());
					}
				);
			});
		}
		if (frm.doc.asset) {
			frm.add_custom_button(__("View Asset"), () => {
				frappe.set_route("Form", "Asset", frm.doc.asset);
			});
		}
	},
});
