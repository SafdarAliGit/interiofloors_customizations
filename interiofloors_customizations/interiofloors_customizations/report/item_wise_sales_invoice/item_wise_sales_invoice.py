# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = [
        {
            "label": _("Inv No"),
            "fieldname": "inv_no",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 120
        },
        {
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Ref No"),
            "fieldname": "ref_no",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Item"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 140
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Other Charges"),
            "fieldname": "tax",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Grand Total"),
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 120
        }
    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []

    if filters.get("from_date"):
        conditions.append(f"`{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`{doctype}`.posting_date <= %(to_date)s")
    if filters.get("customer"):
        conditions.append(f"`{doctype}`.customer = %(customer)s")

    return " AND ".join(conditions)


def get_data(filters):
    data = []

    sales = """
    SELECT
        si.name AS inv_no,
        si.posting_date,
        si.customer_reference_number_purchase_order AS ref_no,
        sii.item_code,
        sii.qty,
        sii.rate,
        sii.amount, 
        si.total_taxes_and_charges AS tax,
        si.grand_total
        
    FROM
        `tabSales Invoice` si
    INNER JOIN
        `tabSales Invoice Item` sii ON si.name = sii.parent
    WHERE
        {conditions} AND 
        si.docstatus = 1  
    """.format(conditions=get_conditions(filters, "si"))

    sales_result = frappe.db.sql(sales, filters, as_dict=1)

    # TO REMOVE DUPLICATES
    # keys_to_check = ['inv_no', 'posting_date', 'tax']
    # seen_values = []
    #
    # for entry in sales_result:
    #     key_values = tuple(entry[key] for key in keys_to_check)
    # 
    #     if key_values in seen_values:
    #         for key in keys_to_check:
    #             entry[key] = None
    #     else:
    #         seen_values.append(key_values)

    # END
    # for item in sales_result:
    #     item.grand_total = (item.amount if item.amount else 0) + (item.tax if item.tax else 0)

    data.extend(sales_result)

    return data
