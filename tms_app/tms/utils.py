# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt
"""
Shared helpers for the TMS app.

These wrap the cross-module integration points called out in the TMS
functional spec (FLOW_DOCUMENT.md / README.md):
  - Bus Ticket Booking / Cargo Booking -> Sales Invoice (Accounts)
  - Fuel Log / Vehicle Maintenance Log -> Purchase Invoice (Buying/Accounts)
  - Bus Vehicle -> Item + Asset (Assets)

Every "create X" helper here is defensive: if the site is missing a
prerequisite (no default Company, no Asset Category, etc.) it logs the
error and shows a friendly, non-blocking message instead of crashing the
booking/log the user is trying to save.
"""

import frappe
from frappe.utils import nowdate, flt


def get_default_company():
	"""Best-effort lookup of the site's default Company."""
	company = frappe.defaults.get_user_default("company") or frappe.defaults.get_global_default("company")
	if not company:
		company = frappe.db.get_single_value("Global Defaults", "default_company")
	if not company:
		company = frappe.db.get_value("Company", {}, "name")
	return company


def get_or_create_customer(customer_name, mobile_no=None):
	"""Find-or-create a Customer so TMS bookings can bill through Accounts."""
	customer_name = (customer_name or "").strip() or "Walk-in Customer"
	if frappe.db.exists("Customer", customer_name):
		return customer_name

	customer_group = frappe.db.get_single_value("Selling Settings", "customer_group") or frappe.db.get_value(
		"Customer Group", {}, "name"
	)
	territory = frappe.db.get_single_value("Selling Settings", "territory") or frappe.db.get_value(
		"Territory", {}, "name"
	)

	customer = frappe.get_doc(
		{
			"doctype": "Customer",
			"customer_name": customer_name,
			"customer_type": "Individual",
			"customer_group": customer_group,
			"territory": territory,
			"mobile_no": mobile_no,
		}
	)
	customer.flags.ignore_mandatory = True
	customer.insert(ignore_permissions=True)
	return customer.name


def get_or_create_item(item_code, item_group=None, is_stock_item=0, is_fixed_asset=0, description=None, extra=None):
	"""Find-or-create an Item. Used for both service items (ticket/cargo
	revenue lines) and fixed-asset items (vehicles)."""
	if frappe.db.exists("Item", item_code):
		return item_code

	if not item_group or not frappe.db.exists("Item Group", item_group):
		item_group = frappe.db.get_single_value("Selling Settings", "item_group") or frappe.db.get_value(
			"Item Group", {}, "name"
		)

	item_doc = {
		"doctype": "Item",
		"item_code": item_code,
		"item_name": item_code,
		"item_group": item_group,
		"stock_uom": "Nos",
		"is_stock_item": is_stock_item,
		"is_fixed_asset": is_fixed_asset,
		"include_item_in_manufacturing": 0,
		"description": description or item_code,
	}
	if is_fixed_asset:
		asset_category = frappe.db.get_value("Asset Category", {}, "name")
		if asset_category:
			item_doc["asset_category"] = asset_category

	if extra:
		item_doc.update(extra)

	item = frappe.get_doc(item_doc)
	item.flags.ignore_mandatory = True
	item.insert(ignore_permissions=True)
	return item.name


def create_sales_invoice(
	customer_name,
	item_code,
	rate,
	qty=1,
	reference_doctype=None,
	reference_name=None,
	mobile_no=None,
	discount_amount=0,
	posting_date=None,
):
	"""Create + submit a Sales Invoice for a TMS booking (Bus Ticket Booking /
	Cargo Booking). Returns the Sales Invoice name, or None if it could not
	be created (a msgprint explains why; the calling booking is never
	blocked by this)."""
	try:
		company = get_default_company()
		if not company:
			frappe.msgprint(
				"No default Company is configured, so a Sales Invoice was not auto-created. "
				"Set a default Company in Global Defaults, then create the invoice manually.",
				alert=True,
				indicator="orange",
			)
			return None

		customer = get_or_create_customer(customer_name, mobile_no)
		get_or_create_item(item_code, item_group="Services", is_stock_item=0)

		si = frappe.new_doc("Sales Invoice")
		si.customer = customer
		si.company = company
		si.posting_date = posting_date or nowdate()
		si.set_posting_time = 1
		si.append("items", {"item_code": item_code, "qty": qty, "rate": flt(rate)})
		if discount_amount:
			si.discount_amount = flt(discount_amount)
		if reference_doctype and reference_name:
			si.remarks = f"Auto-created from {reference_doctype} {reference_name}"

		si.flags.ignore_mandatory = True
		si.insert(ignore_permissions=True)
		si.submit()
		return si.name
	except Exception:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "TMS Sales Invoice Auto-Creation Failed")
		frappe.msgprint(
			"Could not auto-create the Sales Invoice for this booking. "
			"Please create it manually - see the Error Log for details.",
			alert=True,
			indicator="orange",
		)
		return None


def create_purchase_invoice(
	supplier,
	item_code,
	rate,
	qty=1,
	reference_doctype=None,
	reference_name=None,
	posting_date=None,
):
	"""Create + submit a Purchase Invoice for fleet spend (Fuel Log / Vehicle
	Maintenance Log). Only runs when a Supplier is set - otherwise the log
	is just kept as an operational record with no accounting entry."""
	if not supplier:
		return None
	try:
		company = get_default_company()
		if not company:
			frappe.msgprint(
				"No default Company is configured, so a Purchase Invoice was not auto-created.",
				alert=True,
				indicator="orange",
			)
			return None

		get_or_create_item(item_code, item_group="Services", is_stock_item=0)

		pi = frappe.new_doc("Purchase Invoice")
		pi.supplier = supplier
		pi.company = company
		pi.posting_date = posting_date or nowdate()
		pi.set_posting_time = 1
		pi.append("items", {"item_code": item_code, "qty": qty, "rate": flt(rate)})
		if reference_doctype and reference_name:
			pi.remarks = f"Auto-created from {reference_doctype} {reference_name}"

		pi.flags.ignore_mandatory = True
		pi.insert(ignore_permissions=True)
		pi.submit()
		return pi.name
	except Exception:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "TMS Purchase Invoice Auto-Creation Failed")
		frappe.msgprint(
			"Could not auto-create the Purchase Invoice. Please create it manually - "
			"see the Error Log for details.",
			alert=True,
			indicator="orange",
		)
		return None
