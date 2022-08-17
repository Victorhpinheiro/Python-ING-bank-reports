'''This file will hold all the queries for organization'''

# Full table -> (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory

CHECK_YEAR = "SELECT DISTINCT strftime('%Y', date) FROM transactions"
CHECK_MONTH = "SELECT DISTINCT strftime('%m', date) as month FROM transactions WHERE strftime('%Y', date) = ? ORDER BY 1 ASC"

# All year All account credit + debit
ALL_ACCOUNTS_ALL_YEARS_SUM = """SELECT
                            strftime('%Y', date),
                            ROUND(SUM(credit),2) AS total_deposits,
                            ROUND(SUM(debit),2) AS total_debit
                            FROM transactions
                            WHERE category_id != (SELECT id FROM categories WHERE category = 'Internal')
                            GROUP BY 1
                            """

# ALL_ACCOUNTS_ALL_YEARS_AVG = """SELECT
#                             strftime('%Y', date),
#                             ROUND(AVG(NULLIF(credit, '')),2) AS total_deposits,
#                             ROUND(AVG(NULLIF(debit,'')),2) AS total_debit
#                             FROM transactions
#                             WHERE category_id != (SELECT id FROM categories WHERE category = 'Internal')
#                             GROUP BY 1
#                             """

# Used for all accounts analysis of expense by category by month and 5 most expensives other expenses
ALL_ACCOUNTS_CAT_EXPENSES_MONTHLY_VAR = """SELECT
                                    strftime('%m', date),
                                    category,
                                    ROUND(SUM(credit),2) AS credit,
                                    ROUND(SUM(debit),2) AS debit
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category != 'Internal'
                                    GROUP BY 1, 2
                                    HAVING strftime('%Y', date) = ? AND
                                    strftime('%m', date) = ?
                                    """

ALL_ACCOUNTS_HIGH_OTHER_EXPESES_MONTHLY = """SELECT
                                    date,
                                    strftime('%m', date),
                                    description,
                                    category,
                                    debit,
                                    description
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category = 'Other' AND debit < 0
                                    GROUP BY 2,3
                                    HAVING strftime('%Y', date) = ? AND
                                    strftime('%m', date) = ?
                                    ORDER BY debit ASC
                                    LIMIT 5
                                    """

# Used for Pie chart, analyse of all year category
ALL_ACCOUNTS_CAT_YEAR_VAR = """SELECT
                                    strftime('%Y', date),
                                    category,
                                    ROUND(SUM(debit),2) AS debit
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category != 'Internal'
                                    GROUP BY 1, 2
                                    HAVING strftime('%Y', date) = ?
                                    """

MOST_EXPENSIVE_OTHERS_YEAR = """SELECT
                                    date,
                                    strftime('%Y', date),
                                    description,
                                    category,
                                    debit,
                                    description
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category = 'Other' AND debit < 0
                                    GROUP BY 2,3
                                    HAVING strftime('%Y', date) = ? 
                                    ORDER BY debit ASC
                                    LIMIT 10
                                    """

# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
