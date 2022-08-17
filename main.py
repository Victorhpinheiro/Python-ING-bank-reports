import os
import sqlite3
from matplotlib.backends.backend_pdf import PdfPages

import define_final_info as info
import SQL_queries as qr
import create_update_db as db


""" Created by Victor Pinheiro 
all rights reserved
Version 1.0
"""
file_gen = ".\\Input\\conta_test.csv"
acc_info_dic = {"General": 1}
YEAR_CUR = '2022'
REPORTS_FIGS = []

if __name__ == '__main__':

    db.create_db()

    conn = sqlite3.connect("banking.sqlite")
    conn.row_factory = sqlite3.Row # Make possible to access information by name
    cur = conn.cursor()

    # Check the Date format and years on the database
    years = cur.execute(qr.CHECK_YEAR)
    years_in_db = []
    for item in years:
        years_in_db.append(item["year"])

    if len(years_in_db) < 1:
        raise ValueError("DATABASE HAVE THE DATE IN WRONG FORMAT OR EMPTY")
        exit()
    #############################################################################################
    # Difference All years - ALL ACCOUNTS
    #############################################################################################
    all_years_sum = cur.execute(qr.ALL_ACCOUNTS_ALL_YEARS_SUM)

    # Instances of the the all years info
    all_year_sum = info.All_years_total(years_in_db)
    all_year_sum.set_title("Total Credit and Debit by year - without Internal transfers")

    for row in all_years_sum:
        all_year_sum.add_credit(row['total_deposits'])
        all_year_sum.add_debit(row['total_debit'])

    REPORTS_FIGS.append(all_year_sum.plot_info())

    #############################################################################################
    # Monthly Income on specific year - ALL ACCOUNTS
    #############################################################################################
    income = info.Year_total_income(YEAR_CUR)
    q = cur.execute(qr.ALL_ACCOUNTS_INCOME_MONTHLY_VAR,(YEAR_CUR,))

    for row in q:
        income.add_month(row["month"])
        income.add_credit(row["credit"])
    income.set_title(f"Income by month (All Accounts) - {YEAR_CUR}")
    REPORTS_FIGS.append(income.plot_info())

    #############################################################################################
    # Expenses by Category on specifc year - ALL ACCOUNTS
    #############################################################################################
    pie = info.Category_year_pie(YEAR_CUR)
    pie_info = cur.execute(qr.ALL_ACCOUNTS_CAT_YEAR_VAR, (YEAR_CUR,))
    for row in pie_info:
        if row["category"] == 'Income':
            continue
        pie.add_category(row["category"])
        pie.add_value(row["debit"])

    top_10_exp_year = cur.execute(qr.MOST_EXPENSIVE_OTHERS_YEAR, (YEAR_CUR,))
    for row in top_10_exp_year:
        pie.add_expense(row['date'], row['debit'], row['description'])

    REPORTS_FIGS.append(pie.plot_info())

    #############################################################################################
    # Monthly Expenses by category on a specific year - ALL ACCOUNTS
    #############################################################################################
    months = cur.execute(qr.CHECK_MONTH, (YEAR_CUR,))
    months_in_order = []
    for row in months:
        months_in_order.append(row["month"])

    for month in months_in_order:
        mont = info.Month_by_month(YEAR_CUR, month)
        cat_months = cur.execute(qr.ALL_ACCOUNTS_CAT_EXPENSES_MONTHLY_VAR, (YEAR_CUR, month))
        for row in cat_months:
            if row["category"] == 'Salary':
                continue
            mont.add_category(row["category"])
            mont.add_value(row["debit"])

        top_5_exp_month = cur.execute(qr.ALL_ACCOUNTS_HIGH_OTHER_EXPESES_MONTHLY, (YEAR_CUR, month))
        for row in top_5_exp_month:
            mont.add_expense(row['date'], row['debit'], row['description'])
        REPORTS_FIGS.append(mont.plot_info())

    #############################################################################################
    # Print Report Main acc
    #############################################################################################
    try:
        os.mkdir("Reports")
    except Exception:
        pass

    with PdfPages(f".\\Reports\\Report All consolidated {YEAR_CUR}.pdf") as report1:
        for item in REPORTS_FIGS:
            report1.savefig(item)

