frappe.views.calendar["Equipment Maintanance Order"] = {
    field_map: {
        "start": "maintanance_date",
        "end": "maintanance_date",
        "id": "name",
		"title": "equipment_id",
        "allDay": "allDay"
    },
    gantt: true,
    filters: [
        {
            "fieldtype": "Select",
            "fieldname": "status",
            "options": "Placed\nOpen\nCompleted",
            "label": __("Order Status")
        },
    ],
    get_events_method: "quantbit_calibration_process.quantbit_calibration_process.doctype.equipment_maintanance_order.equipment_maintanance_order.get_data", // Endpoint name
    get_css_class: function(data) {
        if(data.status=="Completed") {
            return "success";
        } if(data.status=="Open") {
            return "danger";
        } else if(data.status=="Placed") {
            return "warning";
        }
    }
}




