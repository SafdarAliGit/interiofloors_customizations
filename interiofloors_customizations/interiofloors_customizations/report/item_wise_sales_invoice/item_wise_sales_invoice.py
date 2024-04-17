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
        }
    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []

    if filters.get("from_date"):
        conditions.append(f"`{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`{doctype}`.posting_date <= %(to_date)s")

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
        sii.amount
    FROM
        `tabSales Invoice` si
    INNER JOIN
        `tabSales Invoice Item` sii ON si.name = sii.parent
    WHERE
        si.docstatus = 1 AND 
        {conditions}
    """.format(conditions=get_conditions(filters, "si"))

    sales_result = frappe.db.sql(sales, filters, as_dict=1)
    data.extend(sales_result)

    return data
