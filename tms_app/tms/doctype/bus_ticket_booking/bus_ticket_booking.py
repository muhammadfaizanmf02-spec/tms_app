# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from tms_app.tms.utils import create_sales_invoice


class BusTicketBooking(Document):
	def on_submit(self):
		if self.status == "Cancelled":
			return
		if self.sales_invoice:
			return
		invoice = create_sales_invoice(
			customer_name=self.customer_name,
			item_code="Bus Ticket Fare",
			rate=self.fare_amount or 0,
			reference_doctype=self.doctype,
			reference_name=self.name,
			mobile_no=self.customer_contact,
			discount_amount=self.discount_amount or 0,
			posting_date=self.booking_date,
		)
		if invoice:
			self.db_set("sales_invoice", invoice)

	def on_cancel(self):
		if not self.sales_invoice:
			return
		if frappe.db.get_value("Sales Invoice", self.sales_invoice, "docstatus") != 1:
			return
		try:
			si = frappe.get_doc("Sales Invoice", self.sales_invoice)
			si.cancel()
		except Exception:
			frappe.log_error(frappe.get_traceback(), "TMS Sales Invoice Cancel Failed")
			frappe.msgprint(
				f"Could not auto-cancel linked Sales Invoice {self.sales_invoice}. Please cancel it manually.",
				alert=True,
				indicator="orange",
			)
