import json

import frappe

NUMBER_CARDS = [
	{
		"name": "Active Engagements",
		"document_type": "Engagement",
		"filters": [["Engagement", "status", "not in", ["Completed", "Archived", "Declined"]]],
	},
	{
		"name": "Open Audit Findings",
		"document_type": "Audit Finding",
		"filters": [["Audit Finding", "status", "=", "Open"]],
	},
	{
		"name": "Open Review Notes",
		"document_type": "Review Note",
		"filters": [["Review Note", "status", "=", "Open"]],
	},
	{
		"name": "Pending Deliverables",
		"document_type": "Deliverable",
		"filters": [["Deliverable", "status", "!=", "Delivered"]],
	},
]

GROUP_BY_CHARTS = [
	{
		"name": "Engagements by Status",
		"document_type": "Engagement",
		"group_by_based_on": "status",
		"type": "Bar",
	},
	{
		"name": "Audit Findings by Severity",
		"document_type": "Audit Finding",
		"group_by_based_on": "severity",
		"type": "Donut",
	},
	{
		"name": "Open Review Notes by Priority",
		"document_type": "Review Note",
		"group_by_based_on": "priority",
		"type": "Bar",
	},
]

DASHBOARD_NAME = "CA Firm Audit Dashboard"


def create_number_cards():
	for card in NUMBER_CARDS:
		if frappe.db.exists("Number Card", card["name"]):
			continue
		try:
			doc = frappe.new_doc("Number Card")
			doc.label = card["name"]
			doc.document_type = card["document_type"]
			doc.type = "Document Type"
			doc.function = "Count"
			doc.is_public = 1
			doc.filters_json = json.dumps(card["filters"])
			doc.insert(ignore_permissions=True)
		except Exception:
			frappe.log_error(title=f"CA Firm: failed to create number card {card['name']}")


def create_charts():
	for chart in GROUP_BY_CHARTS:
		if frappe.db.exists("Dashboard Chart", chart["name"]):
			continue
		try:
			doc = frappe.new_doc("Dashboard Chart")
			doc.chart_name = chart["name"]
			doc.chart_type = "Group By"
			doc.document_type = chart["document_type"]
			doc.group_by_type = "Count"
			doc.group_by_based_on = chart["group_by_based_on"]
			doc.type = chart["type"]
			doc.timeseries = 0
			doc.timespan = "Last Year"
			doc.time_interval = "Monthly"
			doc.is_public = 1
			doc.insert(ignore_permissions=True)
		except Exception:
			frappe.log_error(title=f"CA Firm: failed to create dashboard chart {chart['name']}")


def create_dashboard():
	if frappe.db.exists("Dashboard", DASHBOARD_NAME):
		return
	try:
		doc = frappe.new_doc("Dashboard")
		doc.dashboard_name = DASHBOARD_NAME
		doc.module = "CA Firm Setup"
		doc.is_default = 0
		for chart in GROUP_BY_CHARTS:
			if frappe.db.exists("Dashboard Chart", chart["name"]):
				doc.append("charts", {"chart": chart["name"], "width": "Half"})
		for card in NUMBER_CARDS:
			if frappe.db.exists("Number Card", card["name"]):
				doc.append("cards", {"card": card["name"]})
		doc.insert(ignore_permissions=True)
	except Exception:
		frappe.log_error(title="CA Firm: failed to create dashboard")


def create_all():
	create_number_cards()
	create_charts()
	create_dashboard()
