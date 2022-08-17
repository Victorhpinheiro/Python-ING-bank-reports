import csv
import random
import datetime
import os

FILE_NAME = ".\\Input\\conta_test.csv"
HEADERS = ['Date', 'Description', 'Credit', 'Debit', 'Balance']
DATE_START = datetime.datetime(2020, 1, 2)
DATE_END = datetime.datetime(2022, 12, 30)
DESCRIPTIONS_DEBIT = ["WOOLWORTHS", "AGL", "TRANSPORT", "RENT", "Stake", "AMAZON", "Fitness", "Other"]
DESCRIPTIONS_CREDIT = ['Salary']
QUANTITY_OF_TRANSACTIONS = 10000

# Trully random data, good to test efficiency but display/reports might look silly 
def rand_date(start, end):
    '''Consider start and end a datetime object'''
    diff = end - start
    random_days = random.randrange(diff.days)
    date = start + datetime.timedelta(days=random_days)

    if date.day < 10 and date.month < 10:
        date_str = f"0{date.day}/0{date.month}/{date.year}"
    elif date.day < 10 and date.month >= 10:
        date_str = f"0{date.day}/{date.month}/{date.year}"
    elif date.day >= 10 and date.month < 10:
        date_str = f"{date.day}/0{date.month}/{date.year}"
    else:
        date_str = f"{date.day}/{date.month}/{date.year}"

    return date_str


def rand_ranges(type):
    if type == "WOOLWORTHS":
        return -1 * random.randrange(1,150)
    
    elif type == "Other":
        return -1 * random.randrange(1,2500)
    
    elif type == "TRANSPORT":
        return -1 * random.randrange(1,50)

    elif type == "AMAZON":
        return -1 * random.randrange(1,50)

    elif type == "RENT":
        return -1 * random.randrange(1,700)
    
    elif type == "Fitness":
        return -1 * random.randrange(1,50)

    elif type == "Investment":
        return -1 * random.randrange(1,150)
    
    elif type == "Salary":
        return random.randrange(5000,7000)
    
    elif type == "Stake":
        return -1* random.randrange(1,250)
    
    elif type == "AGL":
        return -1* random.randrange(1,250)


def generate_quantity(num):
    lst = []
   
    for i in range(num):
        credit = False
        prob = random.randrange(100)
        if prob <= 2:
            credit = True

        dt = rand_date(DATE_START, DATE_END)
        des_credit = random.choice(DESCRIPTIONS_CREDIT)
        des_debit = random.choice(DESCRIPTIONS_DEBIT)

        if credit:
            lst.append([dt, des_credit, rand_ranges(des_credit), 0, 5000])
        else:
            lst.append([dt, des_debit, 0, rand_ranges(des_debit), 5000])
    
    return lst

try:
    os.mkdir("Input")
except Exception:
    pass

with open(FILE_NAME, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(HEADERS)
    writer.writerows(generate_quantity(QUANTITY_OF_TRANSACTIONS))