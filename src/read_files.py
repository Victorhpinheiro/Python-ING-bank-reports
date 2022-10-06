import csv


class Row:
    """
    Hold information of the rows of the CSV
    """

    def __init__(self, name, date, description, credit, debit, balance) -> None:
        self.name = name
        self.date = date
        self.description = description
        self.credit = credit
        self.debit = debit
        self.balance = balance

    def get_name(self):
        return self.name

    def get_date(self):
        return self.date

    def get_description(self):
        return self.description

    def get_credit(self):
        return self.credit

    def get_debit(self):
        return self.debit

    def get_balance(self):
        return self.balance

    def is_credit(self):
        if self.credit > 0 and self.debit == 0:
            return True
        return False

    def is_debit(self):
        """Debit is a Negative value"""
        if self.credit == 0 and self.debit < 0:
            return True
        return False

    def __str__(self) -> str:
        return f"ROW of date {self.date} and balance {self.balance}"


def read_csv(acc_name, file):
    """
    Consider the CSV file from the bank ING and return all the information as a list of rows objects
    """
    # TODO default ING
    if 'ING' in acc_name:
        try:
            with open(file, "r") as f:
                csv_reader = csv.DictReader(f)
                next(csv_reader)

                for line in csv_reader:
                    yield Row(
                        acc_name,
                        line["Date"],
                        line["Description"],
                        line["Credit"],
                        line["Debit"],
                        line["Balance"],
                    )
        except Exception:
            raise FileExistsError("Couldn't Open the CSV")
    elif 'CBA' in acc_name:
        # CBA csv does not have header, the structure is: Date, credit/debit, descripiton balance
        try:
            with open(file, "r") as f:
                csv_reader = csv.reader(f)

                for line in csv_reader:
                    if float(line[1]) < 0:
                        yield Row(
                            acc_name,
                            line[0],
                            line[2],
                            0,
                            float(line[1]),
                            line[3],
                        )
                    else:
                        yield Row(
                            acc_name,
                            line[0],
                            line[2],
                            float(line[1]),
                            0,
                            line[3],
                        )
        except Exception:
            raise FileExistsError("Couldn't Open the CSV or no ING or CBA in the name")
        


def format_date(date):
    # Format date into the ISO8601 in order to add to the db yyyy-mm-dd
    # Consider the input date in the format dd/mm/yyyy
    new_date = date.split("/")
    new_date.reverse()
    new_date = "-".join(new_date)

    return new_date



