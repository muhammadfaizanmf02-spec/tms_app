# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.utils import flt

from tms_app.tms.utils import create_purchase_invoice


class FuelLog(Document):
	def validate(self):
		self.total_cost = flt(self.fuel_quantity_litres) * flt(self.rate_per_litre)

	def on_submit(self):
		if self.purchase_invoice or not self.supplier:
			return
		invoice = create_purchase_invoice(
			supplier=self.supplier,
			item_code="Vehicle Fuel",
			rate=self.total_cost or 0,
			reference_doctype=self.doctype,
			reference_name=self.name,
			posting_date=self.date,
		)
		if invoice:
			self.db_set("purchase_invoice", invoice)
