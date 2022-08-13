import read_files
import categories
import sqlite3


if __name__ == "__main__":

    # Connect to the db
    conn = sqlite3.connect("banking.sqlite")
    cur = conn.cursor()

    # I will try to create tables efficiently : one for banki account information. One for category. Finally, one for the transactions.
    # Will keep credit and debit separated, as per the ING csv, to make more readable the queries
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS categories
        (id INTEGER PRIMARY KEY  ASC,
        category TEXT);
        """
    )
    cur.execute(
        """ CREATE TABLE IF NOT EXISTS acc_info
        (id INTEGER PRIMARY KEY ASC,
        category TEXT);"""
    )
    cur.execute(
        """ CREATE TABLE IF NOT EXISTS transactions
        (id INTEGER PRIMARY KEY ASC,
        account_id INTEGER,
        date TEXT NOT NULL,
        description TEXT NOT NULL,
        credit REAL,
        debit REAL,
        balance REAL,
        category TEXT);
        """
    )
    # Populate files

    categories_dic = dict(
        zip(categories.categories, [i + 1 for i in range(len(categories.categories))])
    )
    # Populate category
    for key, value in categories_dic:
        cur.execute(
            """
            INSERT INTO categoy (id, category)
            VALUES (?, ?)
            """,
            value,
            key,
        )

    # I have two everyday account that I will call "Notomorrow" and "General" give the name of your account :)

    file_noto = ".\\Input\\Transactions no tomorrow.csv"
    file_gen = ".\\Input\\Transactions-general-stuff.csv"
    notomorrow = read_files.read_csv("Notomorrow", file_noto)
    general = read_files.read_csv("General", file_gen)

    # populate acc_info

    for row in general:
        acc_name = row.get_name()
        date = row.get_date()
        desciption = row.get_description()
        credit = row.get_credit()
        debit = row.get_debit()
        category = categories.set_category(desciption)

        cur.execute(
            """
            INSERT INTO categoy
        """
        )
