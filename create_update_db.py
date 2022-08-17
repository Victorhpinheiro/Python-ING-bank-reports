import read_files
import categories
import sqlite3


if __name__ == "__main__":

    # Connect to the db
    conn = sqlite3.connect("banking.sqlite")
    cur = conn.cursor()

    # # I will try to create tables efficiently : one for banki account information. One for category. Finally, one for the transactions.
    # # Will keep credit and debit separated, as per the ING csv, to make more readable the queries
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS categories
        (id INTEGER PRIMARY KEY,
        category TEXT);
        """
    )
    cur.execute(
        """ CREATE TABLE IF NOT EXISTS acc_info
        (id INTEGER PRIMARY KEY,
        acc TEXT);"""
    )
    cur.execute(
        """ CREATE TABLE IF NOT EXISTS transactions
        (account_id INTEGER,
        date DATE NOT NULL,
        description TEXT NOT NULL,
        credit REAL,
        debit REAL,
        balance REAL,
        category_id TEXT);
        """
    )
    # Populate files

    categories_dic = dict(
        zip(categories.categories, [i + 1 for i in range(len(categories.categories))])
    )
    # Populate category
    for key, value in categories_dic.items():
        cur.execute(
            "INSERT OR IGNORE INTO categories (id, category) VALUES ( ? , ?)",
            (value, key),
        )
    conn.commit()

    # I have two everyday account that I will call "Notomorrow" and "General" give the name of your account :)

    # Populate acc_info
    acc_info_dic = {"General": 1, "Notomorrow": 2}
    for key, value in acc_info_dic.items():
        cur.execute(
            "INSERT OR IGNORE INTO acc_info (id, acc) VALUES ( ? , ?)", (value, key)
        )
    conn.commit()

    # Prepare to read and populate transactions table
    file_noto = ".\\Input\\Transactions no tomorrow.csv"
    file_gen = ".\\Input\\Transactions-general-stuff.csv"
    notomorrow = read_files.read_csv("Notomorrow", file_noto)
    general = read_files.read_csv("General", file_gen)

    for row in general:
        acc_name = row.get_name()
        date = read_files.format_date(row.get_date())
        desciption = row.get_description()
        credit = row.get_credit()
        debit = row.get_debit()
        balance = row.get_balance()
        category = categories.set_category(desciption)

        cur.execute(
            """INSERT OR IGNORE INTO transactions 
                (account_id,
                date,
                description,
                credit,
                debit,
                balance,
                category_id)
            VALUES ( ? , ? , ?, ?, ?, ?, ?)""",
            (
                acc_info_dic["General"],
                date,
                desciption,
                credit,
                debit,
                balance,
                categories_dic[category],
            ),
        )
    conn.commit()

    for row in notomorrow:
        acc_name = row.get_name()
        date = read_files.format_date(row.get_date())
        desciption = row.get_description()
        credit = row.get_credit()
        debit = row.get_debit()
        balance = row.get_balance()
        category = categories.set_category(desciption)

        cur.execute(
            """INSERT OR IGNORE INTO transactions 
                (account_id,
                date,
                description,
                credit,
                debit,
                balance,
                category_id)
            VALUES ( ? ,  ? , ?, ?, ?, ?, ?)""",
            (
                acc_info_dic["Notomorrow"],
                date,
                desciption,
                credit,
                debit,
                balance,
                categories_dic[category],
            ),
        )
    conn.commit()
    conn.close()
