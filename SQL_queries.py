'''This file will hold all the queries for organization'''

# Full table -> (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory

CHECK_YEAR = "SELECT DISTINCT strftime('%Y', date) as year FROM transactions"
CHECK_MONTH = "SELECT DISTINCT strftime('%m', date) as month FROM transactions WHERE strftime('%Y', date) = ? ORDER BY 1 ASC"


####################################################################################################################
# Calulate ALL YEAR CREDIT vs DEBIT - ALL ACC
####################################################################################################################
ALL_ACCOUNTS_ALL_YEARS_SUM = """SELECT
                            strftime('%Y', date),
                            ROUND(SUM(credit),2) AS total_deposits,
                            ROUND(SUM(debit),2) AS total_debit
                            FROM transactions
                            WHERE category_id != (SELECT id FROM categories WHERE category = 'Internal')
                            GROUP BY 1
                            """

####################################################################################################################
# Calulate Income by month - ALL ACC
####################################################################################################################
ALL_ACCOUNTS_INCOME_MONTHLY_VAR = """SELECT
                                    strftime('%m', date) as month,
                                    ROUND(SUM(credit),2) AS credit
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category != 'Internal' AND strftime('%Y', date) = ?
                                    GROUP BY 1
                                    HAVING CREDIT > 0
                                    """


####################################################################################################################
# Calulate Expenses by category by month + top 5 expenses of the month - ALL ACC
####################################################################################################################
ALL_ACCOUNTS_CAT_EXPENSES_MONTHLY_VAR = """SELECT
                                    strftime('%Y/%m', date),
                                    category,
                                    ROUND(SUM(debit),2) AS debit
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category != 'Internal' AND debit < 0
                                    GROUP BY 1, 2
                                    HAVING strftime('%Y', date) = ? AND
                                    strftime('%m', date) = ?
                                    """

ALL_ACCOUNTS_HIGH_OTHER_EXPESES_MONTHLY = """SELECT
                                    date,
                                    strftime('%Y/%m', date),
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

####################################################################################################################
# Calulate Expenses by category by yes + top 10 expenses of the year - ALL ACC
####################################################################################################################
ALL_ACCOUNTS_CAT_YEAR_VAR = """SELECT
                                    strftime('%Y', date),
                                    category,
                                    ROUND(SUM(debit),2) AS debit
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category != 'Internal' AND debit < 0
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

####################################################################################################################
# Calulate ALL YEAR CREDIT vs DEBIT - INDIVIDUAL ACC
####################################################################################################################
INDIVIDUAL_ACCOUNT_ALL_YEARS_SUM = """SELECT
                            strftime('%Y', date),
                            ROUND(SUM(credit),2) AS total_deposits,
                            ROUND(SUM(debit),2) AS total_debit
                            FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                            WHERE category_id != (SELECT id FROM categories WHERE category = 'Internal') AND
                            acc = ?
                            GROUP BY 1
                            """

####################################################################################################################
# Calulate Income by month - INDIVIDUAL ACC
####################################################################################################################
INDIVIDUAL_ACCOUNT_INCOME_MONTHLY_VAR = """SELECT
                                    strftime('%m', date) as month,
                                    acc,
                                    ROUND(SUM(credit),2) AS credit
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category != 'Internal' AND strftime('%Y', date) = ? AND
                                    acc = ?
                                    GROUP BY 1, 2
                                    HAVING CREDIT > 0
                                    """


####################################################################################################################
# Calulate Expenses by category by month + top 5 expenses of the month - INDIVIDUAL ACC
####################################################################################################################
INDIVIDUAL_ACCOUNT_CAT_EXPENSES_MONTHLY_VAR = """SELECT
                                    strftime('%Y%m', date),
                                    category,
                                    acc,
                                    ROUND(SUM(debit),2) AS debit
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category != 'Internal' AND acc =? AND debit < 0
                                    GROUP BY 1, 2, 3
                                    HAVING strftime('%Y', date) = ? AND
                                    strftime('%m', date) = ?
                                    """

INDIVIDUAL_ACCOUNT_HIGH_OTHER_EXPESES_MONTHLY = """SELECT
                                    date,
                                    strftime('%Y%m', date),
                                    description,
                                    acc,
                                    category,
                                    debit,
                                    description
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category = 'Other' AND debit < 0 and
                                    acc = ?
                                    GROUP BY 2, 3, 4
                                    HAVING strftime('%Y', date) = ? AND
                                    strftime('%m', date) = ?
                                    ORDER BY debit ASC
                                    LIMIT 5
                                    """

####################################################################################################################
# Calulate Expenses by category by year PIE + top 10 expenses of the year - INDIVIDUAL ACC
####################################################################################################################
INDIVIDUAL_ACCOUNT_CAT_YEAR_VAR = """SELECT
                                    strftime('%Y', date),
                                    category,
                                    acc,
                                    ROUND(SUM(debit),2) AS debit
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category != 'Internal' AND debit < 0 AND
                                    acc = ?
                                    GROUP BY 1, 2
                                    HAVING strftime('%Y', date) = ?
                                    """

INDIVIDUAL_MOST_EXPENSIVE_OTHERS_YEAR = """SELECT
                                    date,
                                    strftime('%Y', date),
                                    description,
                                    acc,
                                    category,
                                    debit,
                                    description
                                    FROM (SELECT * FROM transactions AS t JOIN categories AS c ON t.category_id = c.id JOIN acc_info AS a ON t.account_id = a.id)
                                    WHERE category = 'Other' AND debit < 0 AND
                                    acc = ?
                                    GROUP BY 2,3,4
                                    HAVING strftime('%Y', date) = ? 
                                    ORDER BY debit ASC
                                    LIMIT 10
                                    """
