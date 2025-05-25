frappe.views.calendar["Equipment Maintenance Order"] = {
    field_map: {
        "start": "date",
        "end": "date",
        "id": "name",
		"title": "status",
        "allDay": "allDay"
    },
    gantt: true,
    filters: [
        {
            "fieldtype": "Select",
            "fieldname": "status",
            "options": "Placed\nOpen\nCompleted\nDraft",
            "label": __("Order Status")
        },
    ],
    get_events_method: "quantbit_calibration_process.quantbit_calibration_process.doctype.equipment_maintenance_order.equipment_maintenance_order.get_data", 
    get_css_class: function(data) {
        if(data.status=="Completed") {
            return "success";
        } if(data.status=="Open") {
            return "danger";
        } else if(data.status=="Draft") {
            return "warning";
        }
    }
}
