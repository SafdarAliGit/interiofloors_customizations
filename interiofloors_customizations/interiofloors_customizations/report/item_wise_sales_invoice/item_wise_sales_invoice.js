frappe.query_reports["Item Wise Sales Invoice"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 1,
			 on_change: () => {
                var customer = frappe.query_report.get_filter_value('customer');
                if (customer) {
                    frappe.db.get_value('Customer', customer, ["customer_name"], function (value) {
                        frappe.query_report.set_filter_value('customer_name', value["customer_name"]);
                    });
                } else {
                    frappe.query_report.set_filter_value('customer_name', "");
                }
            }

		},
		 {
            "fieldname": "customer_name",
            "label": __("Party Name"),
            "fieldtype": "Data",
            "hidden": 0,

        },


	]
};