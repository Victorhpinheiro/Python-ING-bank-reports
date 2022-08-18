import matplotlib.pyplot as plt
import matplotlib
import numpy as np

FIG_WIDTH = 21
FIG_HEIGHT = 13

MONTH_MAP = {
            '01': 'January', '02': 'February', '03': 'March',
            '04': 'April', '05': 'May', '06': 'June',
            '07': 'July', '08': 'August', '09': 'September',
            '10': 'October', '11': 'November', '12': 'December'
            }
def func(pct, allvals):
    '''Format the auto % of the pie chart'''
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n(${:,.2f} )".format(pct, absolute)

class All_years_total:
    """receive total value of all years of credit and debit without considering Internal transfers in asc order"""

    def __init__(self, list_all_years) -> None:
        self.list_all_years = list_all_years  # [2020, ,2021, 2022]
        self.list_values_credit = []  # have to be same len of all years
        self.list_values_debit = []  # have to be sabe len of all years
        self.title = ""

    def add_credit(self, credit):
        self.list_values_credit.append(credit)

    def add_debit(self, debit):
        if debit < 0:
            debit = debit * (-1)

        self.list_values_debit.append(debit)
    
    def set_title(self, title):
        self.title = title

    def plot_info(self):
        # Check if everything is same size
        length = len(self.list_all_years)
        if not all(length == len(lst) for lst in [self.list_values_credit, self.list_values_debit]):
            print("Values of indivual years are not the same length than credit/debit")
            return
    
        fig, ax = plt.subplots()  # Instance of Bar chart
        fig.set(figwidth=FIG_WIDTH, figheight=FIG_HEIGHT)
        plt.style.use('seaborn')  # Define style
        # Prepare X array and the width of the bars
        x_index = np.arange(length)
        width = 0.3
    
        # Add the bar that will be plotted in a variable
        rec_credit = ax.bar(x_index - (width/2), self.list_values_credit, width=width, color='#6bbf59', label='Credit')
        rec_debit = ax.bar(x_index + (width/2), self.list_values_debit, width=width, color='#fa7e61', label='Debit')

        ax.legend()  # Add color legend
        ax.set_title(self.title, fontsize=20)
        ax.set_xticks(ticks=x_index, labels=self.list_all_years)  # pass year as X layer
        ax.set_ylabel("Value $", fontsize='large')
        ax.set_xlabel("Years", fontsize='large')
        ax.yaxis.set_major_formatter('${x:,.2f}')

        # Add value on the bad and format nicely
        ax.bar_label(rec_credit, labels=[f'${x:,.2f}' for x in self.list_values_credit], fontsize='large')
        ax.bar_label(rec_debit, labels=[f'${x:,.2f}' for x in self.list_values_debit], fontsize='large')
        ax.grid(True, alpha=0.1)

        #Add text with difference info
        diff = self.diff_by_year()
        tittle = "Difference by year:     \n\n\n"
        line = []
        for key, value in diff.items():
            line.append(f"{key}: ${value:,.2f} \n\n")
        final_text = tittle + "".join(line)

        fig.tight_layout()
        fig.text(0.65, 0.8, final_text, ha='left', va='center', size=20, color='black')
        fig.subplots_adjust(right=0.62)

        # fig.savefig("foo.pdf", bbox_inches='tight')
        # plt.show()
        return fig

    def diff_by_year(self):
        length = len(self.list_all_years)
        if not all( length == len(lst) for lst in [self.list_values_credit, self.list_values_debit]):
            print("Values of indivual years are not the same length than credit/debit")
            return
        diff = dict()
        for i in range(length):
            diff[self.list_all_years[i]] = self.list_values_credit[i] - self.list_values_debit[i]
        
        return diff
        

class Month_by_month:
    def __init__(self, year, month) -> None:
        self.categories = []
        self.month = month
        self.year = year
        self.list_values = []  
        self.title = f"Expenses by Category - {MONTH_MAP[self.month]} / {self.year}" 
        self.expenses = []
     
    def add_category(self, category):
        self.categories.append(category)

    def add_value(self, value):
        if value < 0:
            value = value * (-1)

        self.list_values.append(value)

    def add_expense(self, date, expense, description):
        if len(self.expenses) < 1:
            self.expenses.append(f"TOP 5 OTHER EXPENSES MONTH - {MONTH_MAP[self.month]}/{self.year}\n\n\n")

        self.expenses.append(f"{date}: ${expense:,.2f} - {description[:20]}\n\n")

    def set_title(self, title):
        self.title = title

    def plot_info(self):
        # Check if everything is same size
        length = len(self.categories)
        if not length == len(self.list_values):
            print("Values and Categories are not the same length")
            return
    
        fig, ax = plt.subplots()  # Instance of Bar chart
        fig.set(figwidth=FIG_WIDTH, figheight=FIG_HEIGHT)
        plt.style.use('seaborn')  # Define style

        # Prepare X array and the width of the bars
        width = 0.35
    
        # Add the bar that will be plotted in a variable color='#fa7e61'
        rec = ax.bar(self.categories, self.list_values, width=width, color='#fa7e61')

        # ax.legend()  # Add color legend
        ax.set_title(self.title, fontsize=20)
        ax.set_ylabel("Value $", fontsize='large')
        ax.set_xlabel("Categories", fontsize='large')
        ax.yaxis.set_major_formatter('${x:,.2f}')

        # Add value on the bad and format nicely
        ax.bar_label(rec, labels=[f'${x:,.2f}' for x in self.list_values], fontsize='large')
        ax.grid(True, alpha=0.4)

        if len(self.expenses) >= 1:
            final_text = "".join(self.expenses)
        else:
            final_text = None

        fig.tight_layout()
        fig.text(0.65, 0.7, final_text, ha='left', va='center', size=20, color='#010001')
        fig.subplots_adjust(right=0.62)

        # fig.savefig("foo.pdf", bbox_inches='tight')
        # plt.show()
        return fig


class Category_year_pie:
    def __init__(self, year) -> None:
        self.categories = []
        self.year = year
        self.list_values = []  
        self.title = f"Expenses by Category - {self.year}" 
        self.expenses = []
     
    def add_category(self, category):
        self.categories.append(category)

    def add_value(self, value):
        if value < 0:
            value = value * (-1)

        self.list_values.append(value)

    def add_expense(self, date, expense, description):
        if len(self.expenses) < 1:
            self.expenses.append(f"TOP 10 OTHER EXPENSES YEAR - {self.year}\n\n\n")

        self.expenses.append(f"{date}: ${expense:,.2f} - {description[:20]}\n\n")

    def set_title(self, title):
        self.title = title

    def plot_info(self):
        # Check if everything is same size
        length = len(self.categories)
        if not length == len(self.list_values):
            print("Values and Categories are not the same length")
            return

        color = ['#ff9999', '#edff86', '#66b3ff', '#fa7e61', '#ffcc99', "#bc5f04", '#f4442e',
                '#48acf0','#93a3bc', '#41ead4', '#e6ccbe', '#edff86', '#f3c969', '#ecd444', '#8cad7e']
        colors = color[:length]

        fig, ax = plt.subplots()
        fig.set(figwidth=FIG_WIDTH, figheight=FIG_HEIGHT)
        # plt.style.use('seaborn')  # Define style

        wedges, texts, autotexts = ax.pie(self.list_values, colors=colors, autopct=lambda pct: func(pct, self.list_values), textprops=dict(color="black"))
        ax.legend(wedges, self.categories,
                        title="Categproes",
                        loc="center left",
                        bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.setp(autotexts, size=9, weight="bold")

        ax.set_title(f"Expenses by Category - Year {self.year}", fontsize=20)
        # ax.set_title(self.title, fontsize=20)
        if len(self.expenses) >= 1:
            final_text = "".join(self.expenses)
        else:
            final_text = None

        fig.tight_layout()
        fig.text(0.65, 0.5, final_text, ha='left', va='center', size=20, color='#010001')
        fig.subplots_adjust(right=0.58)

        # # fig.savefig("foo.pdf", bbox_inches='tight')
        # plt.show()
        return fig


class Year_total_income:
    """receive total value of all years of credit and debit without considering Internal transfers in asc order"""

    def __init__(self, year) -> None:
        self.year = year
        self.values_credit = []  # have to be same len of all years
        self.month = []
        self.title = ""

    def add_credit(self, credit):
        self.values_credit.append(credit)
    
    def add_month(self, month):
        self.month.append(month)
    
    def set_title(self, title):
        self.title = title

    def plot_info(self):
        # Check if everything is same size
        length = len(self.month)
        if not length == len(self.values_credit):
            print("Values of indivual months are not the same length than credit")
            return
    
        fig, ax = plt.subplots()  # Instance of Bar chart
        fig.set(figwidth=FIG_WIDTH, figheight=FIG_HEIGHT)
        plt.style.use('seaborn')  # Define style
        # Prepare X array and the width of the bars
        x_index = np.arange(length)
        width = 0.8
    
        # Add the bar that will be plotted in a variable
        rec_credit = ax.bar(x_index, self.values_credit, width=width, color='#6bbf59', label='Income')
        labels = [MONTH_MAP[i] for i in self.month]

        ax.legend()  # Add color legend
        ax.set_title(self.title, fontsize=20)
        ax.set_xticks(ticks=x_index, labels=labels)  # pass year as X layer
        ax.set_ylabel("Value $", fontsize='large')
        ax.set_xlabel("Months", fontsize='large')
        ax.yaxis.set_major_formatter('${x:,.2f}')

        # Add value on the bad and format nicely
        ax.bar_label(rec_credit, labels=[f'${x:,.2f}' for x in self.values_credit], fontsize='large')
        ax.grid(True, alpha=0.1)

        # plt.show()
        return fig
        