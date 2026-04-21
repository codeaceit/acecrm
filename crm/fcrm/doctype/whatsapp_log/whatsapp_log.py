# Copyright (c) 2026, CodeAce IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WhatsappLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		date: DF.Date | None
		id: DF.Data | None
		message: DF.SmallText | None
		reference_docname: DF.DynamicLink | None
		reference_doctype: DF.Link | None
		user: DF.Link | None
	# end: auto-generated types

	@staticmethod
	def default_list_data():
		return {
			"columns": [
				{"label": "From Number", "type": "Data", "key": "from", "width": "12rem"},
				{"label": "Message", "type": "Small Text", "key": "message", "width": "20rem"},
				{"label": "Date", "type": "Date", "key": "date", "width": "10rem"},
				{"label": "User", "type": "Link", "key": "user", "width": "10rem"},
			],
			"rows": ["from", "message", "date", "user"],
		}


@frappe.whitelist()
def get_whatsapp_log(log_name=None):
	frappe.flags.in_test = True
	if not log_name:
		return {"error": "log_name is required"}
	CRM_ALLOWED_ROLES = ["System Manager", "Sales Manager", "Sales User"]
	roles = set(frappe.get_roles())

	if not roles.intersection(set(CRM_ALLOWED_ROLES)):
		frappe.throw("You are not permitted to access this resource.", frappe.PermissionError)

	try:
		whatsapp_log = frappe.get_cached_doc("Whatsapp Log", log_name)
		return {
			"id": whatsapp_log.name,
			"name": whatsapp_log.name,
			"from_number": whatsapp_log.get("from"),
			"message": whatsapp_log.message,
			"date": whatsapp_log.date,
			"user": whatsapp_log.user,
			"id": whatsapp_log.id,
			"reference_doctype": whatsapp_log.reference_doctype,
			"reference_docname": whatsapp_log.reference_docname,
		}
	except frappe.DoesNotExistError:
		return {"error": f"Whatsapp Log {log_name} not found"}
	return {
		"name": whatsapp_log.name,
		"from_number": whatsapp_log.get("from"),
		"message": whatsapp_log.message,
		"date": whatsapp_log.date,
		"user": whatsapp_log.user,
		"id": whatsapp_log.id,
		"reference_doctype": whatsapp_log.reference_doctype,
		"reference_docname": whatsapp_log.reference_docname,
	}
