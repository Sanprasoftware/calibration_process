# Copyright (c) 2024, tejal kumbhar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EquipmentMaintenanceOrder(Document):
	

	@frappe.whitelist()
	def available_qty(self):
		for row in self.get("items"):
			if row.source_warehouse and row.item_code:
				doc_name = frappe.get_value('Bin',{'item_code':row.item_code,'warehouse': row.source_warehouse}, "actual_qty")
				row.available_quantity = doc_name

	def on_submit(self):
		self.create_task_completion()
	
	@frappe.whitelist()
	def create_task_completion(self):
		for i in self.get("maintanance_task_list"):
			doc = frappe.new_doc("Task List Completion")
			doc.company =self.company
			doc.order_type = self.order_type
			doc.maintanance_order_type = self.maintanance_order_type	
			doc.date =self.date
			doc.equipment_category = self.equipment_category
			doc.equipment_id= self.equipment_id
			doc.equipment_brand=self.equipment_brand
			doc.equipment_name = self.equipment_name
			doc.plant = self.equipment_plant
			doc.location =self.equipment_location
			doc.order_by_department = self.order_from_department
			if self.maintanance_date:
				doc.maintanance_scheduled_date = self.maintanance_date
				doc.equipment_maintenance_schedule = self.equipment_maintanance_schedule
			doc.assign_to = i.assign_to
			doc.assign_to_name = i.assign_to_name
			doc.append('task_completion_details', {	
						"parameter": i.maintenance_task,
						"parameter_details": i.description,
						"value":i.value,
					})
		
			doc.maintenance_order= self.name
			doc.insert()
			doc.save()


@frappe.whitelist()
def get_data(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions

	conditions = get_event_conditions("Equipment Maintenance Order", filters)

	data = frappe.db.sql(
		"""
		select
			distinct `tabEquipment Maintenance Order`.name, `tabEquipment Maintenance Order`.equipment_name, `tabEquipment Maintenance Order`.equipment_id,
			`tabEquipment Maintenance Order`.status, `tabEquipment Maintenance Order`.maintanance_date,`tabEquipment Maintenance Order`.date
		from
			`tabEquipment Maintenance Order`
		where (ifnull(`tabEquipment Maintenance Order`.date, '0000-00-00')!= '0000-00-00') \
			and (`tabEquipment Maintenance Order`.date between %(start)s and %(end)s)
			{conditions}
		""".format(
			conditions=conditions
		),
		{"start": start, "end": end},
		as_dict=True,
		update={"allDay": 0},
	)
	return data
