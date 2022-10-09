import datetime

############################# MAIN #################################################
PATH = ".\\Input" # Path where are the inputs
YEAR_CUR = str(datetime.datetime.today().year) # Year of the reports as string

############################# TEST #################################################
# Will generate a mock csv file when running. Turn to 'False' to use in real data an put files in input
IS_TEST = True
AMOUNT_TEST = 2


############################# CHARTS #################################################
FIG_WIDTH = 21
FIG_HEIGHT = 13
COLOR_BAR_CREDIT = '#6bbf59'
COLOR_BAR_DEBIT = '#fa7e61'
# if you are having more than 15 categories, please add more colors
COLOR_PIE = ['#ff9999', '#edff86', '#66b3ff', '#fa7e61', '#ffcc99', "#bc5f04", '#f4442e',
            '#48acf0','#93a3bc', '#41ead4', '#e6ccbe', '#edff86', '#f3c969', '#ecd444', '#8cad7e']


############################# FIXED #################################################
# Do not change - fix values
MONTH_MAP = {
            '01': 'January', '02': 'February', '03': 'March',
            '04': 'April', '05': 'May', '06': 'June',
            '07': 'July', '08': 'August', '09': 'September',
            '10': 'October', '11': 'November', '12': 'December'
            }