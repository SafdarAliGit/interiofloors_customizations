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
		 "fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
		},
		{
		 "fieldname": "item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
			 on_change: () => {
                var item_code = frappe.query_report.get_filter_value('item_code');
                if (item_code) {
                    frappe.db.get_value('Item', item_code, ["item_name"], function (value) {
                        frappe.query_report.set_filter_value('item_name', value["item_name"]);
                    });
                } else {
                    frappe.query_report.set_filter_value('item_name', "");
                }
            }
		},
		 {
            "fieldname": "item_name",
            "label": __("Item Name"),
            "fieldtype": "Data",
            "hidden": 0,

        },

		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			// "reqd": 1,
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

        }


	]
};