""" 
Created by Victor Pinheiro 
all rights reserved
Version 2.1
"""

import os
import sqlite3
import sys
import subprocess
# Try or install matplotlib
try:
    import matplotlib.pyplot as plt

except Exception:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                        'matplotlib==3.5.3'])
    import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import define_final_info as info
import SQL_queries as qr
import create_update_db as db
import CONFIG as cfg
import create_csv_test as tst_csv


if __name__ == '__main__':

    # Create tests csv if config   
    if cfg.IS_TEST:
        try:
            for i in range(cfg.AMOUNT_TEST):
                file_of_test = 'Acc_name_test' + str(i) + '.csv'
                tst_csv.create_test_csv(cfg.PATH, file_of_test, tst_csv.generate_quality, 10000)
        except Exception:
            raise ValueError("AMOUNT OF TESTS HAVE TO BE AND INTEGER")

    # List of graphs by report
    report_figs = []

    # Create Db and get list of files in Input
    csv_found = db.create_db(cfg.PATH)
    print("Database created")

    conn = sqlite3.connect("banking.sqlite")
    conn.row_factory = sqlite3.Row # Make possible to access information by name, making more readable
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

    report_figs.append(all_year_sum.plot_info())
    print("ALL Accounts - difference all years done")

    #############################################################################################
    # Monthly Income on specific year - ALL ACCOUNTS
    #############################################################################################
    income = info.Year_total_income(cfg.YEAR_CUR)
    q = cur.execute(qr.ALL_ACCOUNTS_INCOME_MONTHLY_VAR, (cfg.YEAR_CUR,))

    for row in q:
        income.add_month(row["month"])
        income.add_credit(row["credit"])
    income.set_title(f"Income by month (All Accounts) - {cfg.YEAR_CUR}")
    report_figs.append(income.plot_info())
    print(f"ALL Accounts - Monthly income on {cfg.YEAR_CUR} done")

    #############################################################################################
    # Expenses by Category on specifc year - ALL ACCOUNTS
    #############################################################################################
    pie = info.Category_year_pie(cfg.YEAR_CUR)
    pie_info = cur.execute(qr.ALL_ACCOUNTS_CAT_YEAR_VAR, (cfg.YEAR_CUR,))
    for row in pie_info:
        pie.add_category(row["category"])
        pie.add_value(row["debit"])

    top_10_exp_year = cur.execute(qr.MOST_EXPENSIVE_OTHERS_YEAR, (cfg.YEAR_CUR,))
    for row in top_10_exp_year:
        pie.add_expense(row['date'], row['debit'], row['description'])

    report_figs.append(pie.plot_info())
    print(f"ALL ACCOUNTS - PIE cat by the year {cfg.YEAR_CUR} done")

    #############################################################################################
    # Monthly Expenses by category on a specific year - ALL ACCOUNTS
    #############################################################################################
    months = cur.execute(qr.CHECK_MONTH, (cfg.YEAR_CUR,))
    months_in_order = []
    for row in months:
        months_in_order.append(row["month"])

    for month in months_in_order:
        mont = info.Month_by_month(cfg.YEAR_CUR, month)
        cat_months = cur.execute(qr.ALL_ACCOUNTS_CAT_EXPENSES_MONTHLY_VAR, (cfg.YEAR_CUR, month))
        for row in cat_months:
            if row["category"] == 'Salary':
                continue
            mont.add_category(row["category"])
            mont.add_value(row["debit"])

        top_5_exp_month = cur.execute(qr.ALL_ACCOUNTS_HIGH_OTHER_EXPESES_MONTHLY, (cfg.YEAR_CUR, month))
        for row in top_5_exp_month:
            mont.add_expense(row['date'], row['debit'], row['description'])
        report_figs.append(mont.plot_info())
        print(f"ALL ACCOUNTS - Expenses for the month {month}-{cfg.YEAR_CUR} done")

    #############################################################################################
    # Print Report ALL ACCS TOGETHER
    #############################################################################################
    try:
        os.mkdir("Reports")
    except Exception:
        pass

    with PdfPages(f".\\Reports\\Report All consolidated {cfg.YEAR_CUR}.pdf") as report1:
        for item in report_figs:
            report1.savefig(item)
            plt.close(item)

    #############################################################################################
    # INDIVIDUAL ACCS
    #############################################################################################
    if len(csv_found) < 2:
        print("Finished all Reports, Go Check on the folder 'Reports':)")
        exit()

    for file in csv_found:
        acc = file # File name without the .csv
        report_figs = []

        #############################################################################################
        # Difference All years - Individual ACC
        #############################################################################################
        all_years_sum = cur.execute(qr.INDIVIDUAL_ACCOUNT_ALL_YEARS_SUM, (acc,))

        # Instances of the the all years info
        all_year_sum = info.All_years_total(years_in_db)
        all_year_sum.set_title("Total Credit and Debit by year - without Internal transfers")

        for row in all_years_sum:
            all_year_sum.add_credit(row['total_deposits'])
            all_year_sum.add_debit(row['total_debit'])

        report_figs.append(all_year_sum.plot_info())
        print(f"Individual Accounts - difference all years done for {acc}")
        
        #############################################################################################
        # Monthly Income on specific year - INDIVIDUAL ACC
        #############################################################################################
        income = info.Year_total_income(cfg.YEAR_CUR)
        q = cur.execute(qr.INDIVIDUAL_ACCOUNT_INCOME_MONTHLY_VAR, (cfg.YEAR_CUR, acc))

        for row in q:
            income.add_month(row["month"])
            income.add_credit(row["credit"])
        income.set_title(f"Income by month (All Accounts) - {cfg.YEAR_CUR}")
        report_figs.append(income.plot_info())
        print(f"Individual acc {acc} - Monthly income on {cfg.YEAR_CUR} done")

        #############################################################################################
        # Expenses by Category on specifc year - INDIVIDUAL ACC
        #############################################################################################
        pie = info.Category_year_pie(cfg.YEAR_CUR)
        pie_info = cur.execute(qr.INDIVIDUAL_ACCOUNT_CAT_YEAR_VAR, (acc, cfg.YEAR_CUR))
        for row in pie_info:
            if row["category"] == 'Income':
                continue
            pie.add_category(row["category"])
            pie.add_value(row["debit"])

        top_10_exp_year = cur.execute(qr.INDIVIDUAL_MOST_EXPENSIVE_OTHERS_YEAR, (acc, cfg.YEAR_CUR))
        for row in top_10_exp_year:
            pie.add_expense(row['date'], row['debit'], row['description'])

        report_figs.append(pie.plot_info())
        print(f"Individual acc {acc} - PIE cat by the year {cfg.YEAR_CUR} done")
        #############################################################################################
        # Monthly Expenses by category on a specific year - ALL ACCOUNTS
        #############################################################################################
        months = cur.execute(qr.CHECK_MONTH, (cfg.YEAR_CUR,))
        months_in_order = []
        for row in months:
            months_in_order.append(row["month"])

        for month in months_in_order:
            mont = info.Month_by_month(cfg.YEAR_CUR, month)
            cat_months = cur.execute(qr.INDIVIDUAL_ACCOUNT_CAT_EXPENSES_MONTHLY_VAR, (acc, cfg.YEAR_CUR, month))
            for row in cat_months:
                if row["category"] == 'Salary':
                    continue
                mont.add_category(row["category"])
                mont.add_value(row["debit"])

            top_5_exp_month = cur.execute(qr.INDIVIDUAL_ACCOUNT_HIGH_OTHER_EXPESES_MONTHLY, (acc, cfg.YEAR_CUR, month))
            for row in top_5_exp_month:
                mont.add_expense(row['date'], row['debit'], row['description'])
            report_figs.append(mont.plot_info())
            print(f"{acc} - Expenses for the month {month}-{cfg.YEAR_CUR} done")

            with PdfPages(f".\\Reports\\Report {acc}-{cfg.YEAR_CUR}.pdf") as report1:
                for item in report_figs:
                    report1.savefig(item)
                    plt.close(item)
    print("Finished all Reports, Go Check on the folder 'Reports':)")
