# Copyright (c) 2024, tejal kumbhar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EquipmentMaintananceOrder(Document):
	pass


@frappe.whitelist()
def get_data(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions

	conditions = get_event_conditions("Equipment Maintanance Order", filters)

	data = frappe.db.sql(
		"""
		select
			distinct `tabEquipment Maintanance Order`.name, `tabEquipment Maintanance Order`.equipment_name, `tabEquipment Maintanance Order`.equipment_id,
			`tabEquipment Maintanance Order`.status, `tabEquipment Maintanance Order`.maintanance_date
		from
			`tabEquipment Maintanance Order`
		where (ifnull(`tabEquipment Maintanance Order`.maintanance_date, '0000-00-00')!= '0000-00-00') \
			and (`tabEquipment Maintanance Order`.maintanance_date between %(start)s and %(end)s)
			{conditions}
		""".format(
			conditions=conditions
		),
		{"start": start, "end": end},
		as_dict=True,
		update={"allDay": 0},
	)
	return data
