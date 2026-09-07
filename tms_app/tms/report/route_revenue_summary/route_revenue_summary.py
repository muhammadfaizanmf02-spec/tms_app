# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt
"""Daily/period Route-wise Revenue Summary - combines Bus Ticket Booking
and Cargo Booking revenue per route, so it lines up with what actually
posts to Accounts via the linked Sales Invoices."""

import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Route", "fieldname": "route", "fieldtype": "Link", "options": "Bus Route", "width": 180},
		{"label": "Tickets Booked", "fieldname": "ticket_count", "fieldtype": "Int", "width": 110},
		{"label": "Ticket Revenue", "fieldname": "ticket_revenue", "fieldtype": "Currency", "width": 130},
		{"label": "Cargo Bookings", "fieldname": "cargo_count", "fieldtype": "Int", "width": 110},
		{"label": "Cargo Revenue", "fieldname": "cargo_revenue", "fieldtype": "Currency", "width": 130},
		{"label": "Total Revenue", "fieldname": "total_revenue", "fieldtype": "Currency", "width": 130},
	]


def get_data(filters):
	date_conditions = ""
	values = {}
	if filters.get("from_date"):
		date_conditions += " AND t.departure_date >= %(from_date)s"
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		date_conditions += " AND t.departure_date <= %(to_date)s"
		values["to_date"] = filters["to_date"]

	rows = frappe.db.sql(
		f"""
		SELECT
			r.name AS route,
			COALESCE(tk.ticket_count, 0) AS ticket_count,
			COALESCE(tk.ticket_revenue, 0) AS ticket_revenue,
			COALESCE(cg.cargo_count, 0) AS cargo_count,
			COALESCE(cg.cargo_revenue, 0) AS cargo_revenue,
			COALESCE(tk.ticket_revenue, 0) + COALESCE(cg.cargo_revenue, 0) AS total_revenue
		FROM `tabBus Route` r
		LEFT JOIN (
			SELECT t.route AS route,
				COUNT(tb.name) AS ticket_count,
				SUM(tb.fare_amount - IFNULL(tb.discount_amount, 0)) AS ticket_revenue
			FROM `tabBus Ticket Booking` tb
			INNER JOIN `tabBus Trip` t ON t.name = tb.trip
			WHERE tb.status != 'Cancelled' {date_conditions}
			GROUP BY t.route
		) tk ON tk.route = r.name
		LEFT JOIN (
			SELECT t.route AS route,
				COUNT(cb.name) AS cargo_count,
				SUM(cb.cargo_charges) AS cargo_revenue
			FROM `tabCargo Booking` cb
			INNER JOIN `tabBus Trip` t ON t.name = cb.trip
			WHERE cb.status != 'Cancelled' {date_conditions}
			GROUP BY t.route
		) cg ON cg.route = r.name
		ORDER BY total_revenue DESC
		""",
		values,
		as_dict=True,
	)
	return rows
