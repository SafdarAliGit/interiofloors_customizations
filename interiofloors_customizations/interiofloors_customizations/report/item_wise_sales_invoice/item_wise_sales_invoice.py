# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
import frappe
from frappe import _
from decimal import Decimal


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = [

        {
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Invoice #"),
            "fieldname": "inv_no",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 120
        },
        {
            "label": _("Reference #"),
            "fieldname": "ref_no",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Items"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 140
        },
        {
            "label": _("Quantity"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 120
        }
        ,
        {
            "label": _("Other Charges"),
            "fieldname": "tax",
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
            "label": _("Grand Total"),
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 120
        }
    ]
    return columns


def format_currency(value):
    # Format the value as a string with 4 decimal places or as an empty string if it's zero
    return f"{value:.4f}" if value != 0 else ""


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
        0 AS grand_total
        
    FROM
        `tabSales Invoice` si
    INNER JOIN
        `tabSales Invoice Item` sii ON si.name = sii.parent
    WHERE
        {conditions} AND 
        si.docstatus = 1  
    """.format(conditions=get_conditions(filters, "si"))

    sales_result = frappe.db.sql(sales, filters, as_dict=1)

    current_brand = None
    brand_data = []  # Collects data for each brand
    brand_sum = {"amount": 0, "tax": 0, "grand_total": 0}  # Track sums for each brand
    total_sum = {"amount": 0, "tax": 0, "grand_total": 0}  # Track total sums

    for record in sales_result:
        # Convert to Decimal and handle None values
        amount = Decimal(record.get('amount', 0) or 0)
        tax = Decimal(record.get('tax', 0) or 0)
        grand_total = Decimal(record.get('grand_total', 0) or 0)
        # Check if we're still processing the same brand
        if current_brand is None:
            # First record, set the current brand
            current_brand = record['inv_no']
        elif record['inv_no'] != current_brand:
            # We've hit a new brand, time to insert the summary for the previous brand
            brand_data.append({
                "item_code": "**TOTAL**",
                "amount": format_currency(brand_sum['amount']),
                "tax": format_currency(brand_sum['tax']),
                "grand_total": format_currency(brand_sum['amount'] + brand_sum['tax']),
            })
            # Update total sum
            for key, value in brand_sum.items():
                total_sum[key] += value
            # Reset the sums for the new brand
            current_brand = record['inv_no']
            brand_sum = {"amount": 0, "tax": 0, "grand_total": 0}

        # Update the sums with the current record
        brand_sum["amount"] += amount
        brand_sum["tax"] += tax
        brand_sum["grand_total"] += grand_total

        # Append the current record to brand_data
        brand_data.append(record)

    # After looping through all records, insert a summary for the last brand
    if current_brand is not None:
        brand_data.append({
            "item_code": "**TOTAL**",
            "amount": format_currency(brand_sum['amount']),
            "tax": format_currency(brand_sum['tax']),
            "grand_total": format_currency(brand_sum['amount'] + brand_sum['tax']),
        })
        # Update total sum
        for key, value in brand_sum.items():
            total_sum[key] += value

    # Append brand_data to data
    data.extend(brand_data)

    # Append total sum to data
    data.append({
        "item_code": "**GRAND TOTAL**",
        "amount":format_currency(total_sum['amount']),
        "tax": format_currency(total_sum['tax']),
        "grand_total": format_currency(brand_sum['amount'] + brand_sum['tax']),
    })

    # sum_tax = 0
    # sum_amount = 0
    # for item in sales_result:
    #     sum_tax += item.tax if item.tax else 0
    #     sum_amount += item.amount if item.amount else 0
    #
    # sales_result.append({
    #     "inv_no": "Total",
    #     "posting_date": "",
    #     "ref_no": "",
    #     "item_code": "",
    #     "qty": "",
    #     "rate": "",
    #     "amount": sum_amount,
    #     "tax": sum_tax
    # })
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

    # data.extend(sales_result)

    return data
