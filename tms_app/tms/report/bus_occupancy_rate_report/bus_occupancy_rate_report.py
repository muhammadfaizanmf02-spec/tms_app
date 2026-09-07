# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Trip", "fieldname": "trip", "fieldtype": "Link", "options": "Bus Trip", "width": 110},
		{"label": "Route", "fieldname": "route", "fieldtype": "Link", "options": "Bus Route", "width": 160},
		{"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Bus Vehicle", "width": 120},
		{"label": "Departure Date", "fieldname": "departure_date", "fieldtype": "Date", "width": 110},
		{"label": "Total Seats", "fieldname": "total_seats", "fieldtype": "Int", "width": 100},
		{"label": "Booked Seats", "fieldname": "booked_seats", "fieldtype": "Int", "width": 110},
		{"label": "Occupancy %", "fieldname": "occupancy", "fieldtype": "Percent", "width": 110},
		{"label": "Trip Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
	]


def get_data(filters):
	conditions = []
	values = {}

	if filters.get("from_date"):
		conditions.append("t.departure_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("t.departure_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	if filters.get("route"):
		conditions.append("t.route = %(route)s")
		values["route"] = filters["route"]
	if filters.get("vehicle"):
		conditions.append("t.vehicle = %(vehicle)s")
		values["vehicle"] = filters["vehicle"]

	condition_sql = (" AND " + " AND ".join(conditions)) if conditions else ""

	rows = frappe.db.sql(
		f"""
		SELECT
			t.name AS trip,
			t.route AS route,
			t.vehicle AS vehicle,
			t.departure_date AS departure_date,
			t.status AS status,
			v.total_seats AS total_seats,
			(
				SELECT COUNT(*) FROM `tabBus Ticket Booking` b
				WHERE b.trip = t.name AND b.status != 'Cancelled'
			) AS booked_seats
		FROM `tabBus Trip` t
		LEFT JOIN `tabBus Vehicle` v ON v.name = t.vehicle
		WHERE 1=1 {condition_sql}
		ORDER BY t.departure_date DESC
		""",
		values,
		as_dict=True,
	)

	for row in rows:
		total_seats = row.total_seats or 0
		booked_seats = row.booked_seats or 0
		row["occupancy"] = round((booked_seats / total_seats) * 100, 1) if total_seats else 0

	return rows
