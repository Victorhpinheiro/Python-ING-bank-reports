import sqlite3

import define_final_info as info
import SQL_queries as qr
# from matplotlib import rcParams

""" Will prepare and run all analyses in SQL and deliver the data in a ready format to plot
    Data analyses : - Individual accounts and total
                    year
                    month
                    Weekly
                    by category

"""
# MAIN ACTIONS

YEAR_CUR = '2022'

conn = sqlite3.connect("banking.sqlite")
conn.row_factory = sqlite3.Row # Make possible to access information by name
cur = conn.cursor()

# Check the Date format and years on the database
years = cur.execute(qr.CHECK_YEAR)
years_in_db = []
for item in years:
    years_in_db.append(item[0])

if len(years_in_db) < 1:
    raise ValueError("DATABASE HAVE THE DATE IN WRONG FORMAT OR EMPTY")
    exit()


# ALL Year TOTAL
all_years_sum = cur.execute(qr.ALL_ACCOUNTS_ALL_YEARS_SUM)

# Instances of the the all years info
all_year_sum = info.All_years_total(years_in_db)
all_year_sum.set_title("Total Credit and Debit by year - without Internal transfers")

for row in all_years_sum:
    all_year_sum.add_credit(row['total_deposits'])
    all_year_sum.add_debit(row['total_debit'])

all_year_sum.plot_info()

#ALL YEAR CATEGORY PIE
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
pie.plot_info()


# ALL Year Average NOT SURE IF WILL USE
# all_years_avg = cur.execute(qr.ALL_ACCOUNTS_ALL_YEARS_AVG)
# all_year_avg = info.All_years_total(years_in_db)

# for item in all_years_avg:
#     all_year_avg.add_credit(item["total_deposits"])
#     all_year_avg.add_debit(item["total_debit"])

# all_year_avg.plot_info()

# # MONTHLY EXPENSES CATEGORY BY MONTH
# months = cur.execute(qr.CHECK_MONTH, (YEAR_CUR,))
# months_in_order = []
# for row in months:
#     months_in_order.append(row["month"])

# for month in months_in_order:
#     mont = info.Month_by_month(YEAR_CUR, month)
#     test = cur.execute(qr.ALL_ACCOUNTS_CAT_EXPENSES_MONTHLY_VAR, (YEAR_CUR, month))
#     for row in test:
#         if row["category"] == 'Salary':
#             continue
#         mont.add_category(row["category"])
#         mont.add_value(row["debit"])

#     top_5_exp_month = cur.execute(qr.ALL_ACCOUNTS_HIGH_OTHER_EXPESES_MONTHLY, (YEAR_CUR, month))
#     for row in top_5_exp_month:

#         print(type(row['debit']))
#         mont.add_expense(row['date'], row['debit'], row['description'])
#     mont.plot_info()




# picture of whole year with categories
# whole_year = cur.execute(
#     """SELECT
#                         strftime('%Y', date),
#                         category_id,
#                         ROUND(AVG(credit),2) AS avarage_deposits,
#                         ROUND(SUM(credit),2) AS total_deposits,
#                         ROUND(AVG(debit),2) AS avarage_debit,
#                         ROUND(SUM(debit),2) AS total_debit
#                         FROM transactions
#                         GROUP BY 1, 2
#                         """
# )

# for item in whole_year:
#     print(item)
