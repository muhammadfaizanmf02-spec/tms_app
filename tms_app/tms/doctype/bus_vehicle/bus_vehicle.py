# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

from tms_app.tms.utils import get_default_company, get_or_create_item


class BusVehicle(Document):
	@frappe.whitelist()
	def create_asset(self):
		"""Create an Item (marked as a fixed asset) + an Asset record for this
		vehicle, and link it back via the `asset` field. This is the bridge
		between the TMS fleet register and ERPNext's Assets module
		(depreciation, maintenance, insurance)."""
		if self.asset:
			frappe.throw(f"Asset {self.asset} is already linked to this vehicle.")

		company = get_default_company()
		if not company:
			frappe.throw("Please set a default Company (Global Defaults) before creating an Asset.")

		asset_category = frappe.db.get_value("Asset Category", {}, "name")
		if not asset_category:
			frappe.throw("Please create at least one Asset Category before creating an Asset.")

		item_code = get_or_create_item(
			self.vehicle_number,
			item_group="Vehicles",
			is_stock_item=0,
			is_fixed_asset=1,
			description=f"{self.vehicle_type or 'Bus'} - {self.vehicle_number}",
		)

		asset = frappe.get_doc(
			{
				"doctype": "Asset",
				"asset_name": self.vehicle_number,
				"item_code": item_code,
				"asset_category": asset_category,
				"company": company,
				"purchase_date": self.purchase_date or nowdate(),
				"available_for_use_date": self.purchase_date or nowdate(),
				"gross_purchase_amount": self.purchase_value or 0,
				"is_existing_asset": 1,
			}
		)
		asset.flags.ignore_mandatory = True
		asset.insert(ignore_permissions=True)

		self.db_set("asset", asset.name)
		frappe.msgprint(f"Asset <b>{asset.name}</b> created and linked to this vehicle.")
		return asset.name
