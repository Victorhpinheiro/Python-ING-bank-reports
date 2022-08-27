'''
Created by Victor Pinheiro
Solo file that will create a mock csv export from the bank ING Australia
There is a function to test efficiency and one for more realistic data
'''

import csv
import random
import datetime
import os
from collections import OrderedDict


FILE_NAME = ".\\Input\\conta-ING.csv"
HEADERS = ['Date', 'Description', 'Credit', 'Debit', 'Balance']
DATE_START = datetime.datetime(2021, 1, 13)
DATE_END = datetime.datetime(2022, 8, 30)
DESCRIPTIONS_DEBIT = ["WOOLWORTHS", "AGL", "TRANSPORT", "RENT", "Stake", "AMAZON", "Fitness", "Other"]
DESCRIPTIONS_CREDIT = ['Salary']



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
        return -1 * random.randrange(1,500)

    elif type == "TRANSPORT":
        return -1 * random.randrange(1,50)

    elif type == "AMAZON":
        return -1 * random.randrange(1,50)

    elif type == "RENT":
        return -1 * random.randrange(1,1500)

    elif type == "Fitness":
        return -1 * random.randrange(1,50)

    elif type == "Investment":
        return -1 * random.randrange(1,150)

    elif type == "Salary":
        return random.randrange(5000,10000)

    elif type == "Stake":
        return -1* random.randrange(1,250)

    elif type == "AGL":
        return -1* random.randrange(1,250)


# Trully random data, good to test efficiency but display/reports might look silly 
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


# Data that makes sense, can't add infinity transactions in a small range of date Good to test report 
def generate_quality(num):
    lst = []
    count_credit = 0
    count_expenses = -1
    other_count = 0
    # Fix to run lst_months faster https://stackoverflow.com/questions/34898525/generate-list-of-months-between-interval-in-python
    # lst_months = OrderedDict(((DATE_START + datetime.timedelta(x)).strftime(r"%m/%Y"), None) for x in range((DATE_END - DATE_START).days)).keys()
    total_months = lambda dt: dt.month + 12 * dt.year
    lst_months = []
    for tot_m in range(total_months(DATE_START)-1, total_months(DATE_END)):
        y, m = divmod(tot_m, 12)
        lst_months.append(datetime.datetime(y, m+1, 1).strftime("%m/%Y"))
    
    
    for item in lst_months:
        fmt_date = f"25/{item}"
        des_credit = random.choice(DESCRIPTIONS_CREDIT)
        value_credit = rand_ranges(des_credit)
        lst.append([fmt_date, des_credit, rand_ranges(des_credit), 0, 5000])
        count_credit += value_credit
    
    # Addd random expenses not pass 90% of income
    for i in range(num):
        prob = random.randrange(100)
        if prob <= 20:
            des_debit = 'Other'
        else:
            des_debit = random.choice(DESCRIPTIONS_DEBIT)
        
        dt = rand_date(DATE_START, DATE_END)
        debit = rand_ranges(des_debit)
        
        if ((count_expenses + debit)*-1) >= (0.90*count_credit):
            break
        
        lst.append([dt, des_debit + str(other_count), 0, rand_ranges(des_debit), 5000])
        count_expenses += debit
        other_count += 1

    return lst


def create_test_csv(path, file_name, func, quantity):
    try:
        os.mkdir("Input")
    except Exception:
        pass

    with open(path + '\\' + file_name, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)
        writer.writerows(func(quantity))
