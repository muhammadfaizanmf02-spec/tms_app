# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from tms_app.tms.utils import create_purchase_invoice


class VehicleMaintenanceLog(Document):
	def on_submit(self):
		if self.purchase_invoice or not self.supplier or not self.cost:
			return
		invoice = create_purchase_invoice(
			supplier=self.supplier,
			item_code="Vehicle Maintenance",
			rate=self.cost or 0,
			reference_doctype=self.doctype,
			reference_name=self.name,
			posting_date=self.maintenance_date,
		)
		if invoice:
			self.db_set("purchase_invoice", invoice)
