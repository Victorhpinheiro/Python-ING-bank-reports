import read_files
import CONFIG_CATEGORIES as categories
import sqlite3
import os


def create_db(path):
    # Check if files exists
    files_to_feed_db = []
    for path, folder, files in os.walk(path):
        for file in files:
            if ("ING" in file and ".csv") or ("CBA" in file and ".csv"):
                files_to_feed_db.append(file[:len(file)-4])
    
    if len(files_to_feed_db) < 1:
        raise FileExistsError(f"No csv with ING in the name in the folder {path}")

    # Connect to the db
    conn = sqlite3.connect("banking.sqlite")
    cur = conn.cursor()

    # Do not accumulate information if run more than once.
    cur.execute("DROP TABLE IF EXISTS categories")
    cur.execute("DROP TABLE IF EXISTS acc_info")
    cur.execute("DROP TABLE IF EXISTS transactions")

    # Create table efficiently - avoiding string repetition: one for bank account information. One for category. Finally, one for the transactions.
    # Will keep credit and debit separated, as per the ING csv, to make more readable in the queries
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
    # Create categories
    categories_dic = dict(
        zip(categories.categories, [i + 1 for i in range(len(categories.categories))])
    )

    # POPULATE categories
    for key, value in categories_dic.items():
        cur.execute(
            "INSERT OR IGNORE INTO categories (id, category) VALUES ( ? , ?)",
            (value, key),
        )
    conn.commit()

    # acc info set-up with the name of the files csv found
    acc_dic = dict(
        zip(files_to_feed_db, [i + 1 for i in range(len(files_to_feed_db))])
    )
    
    files_to_feed_db
    # POPULATE acc_info
    for key, value in acc_dic.items():
        cur.execute(
            "INSERT OR IGNORE INTO acc_info (id, acc) VALUES ( ? , ?)", (value, key)
        )
    conn.commit()

    # Read and populate transactions table
    for acc in files_to_feed_db:
        file_to_read = path + '\\' + acc + ".csv"
        transactions_csv = read_files.read_csv(file, file_to_read)
        for row in transactions_csv:
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
                    acc_dic[acc],
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

    return files_to_feed_db