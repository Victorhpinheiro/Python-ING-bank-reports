import re

# define here your list of categories, regex to check and modify the function

categories = [
    "Income",
    "Groceries",
    "Transport",
    "Shopping",
    "House",
    "Rent",
    "Investment",
    "Subscription",
    "Internal",
    "fitness",
    "Other",
]
# Mapping regex with the description with interest categories.
# CONFIGURATION - REGEX
income = "(Salary)|(Dividend)"  # Salary
grocery = "(WOOLWORTHS)|(COLES)|(ALDI)|(Cosmos)|(7-ELEVEN)|(FISHME)"
transport = "(OPAL)|(UBER)|(CARSHAREAUS)|(TRANSPORT)"
shopping = "(Daiso)|(store)|(AMAZON)|(BIG W)|(MARKETPLACE)|(KMART)|(JB HI-FI)|(EB GAMES)|(TARGET)|(OFFICEWORKS)|(TYPO)"
house = "(VODAFONE)|(AGL)|(CIRCLES)"  # house is internet/ eletricity and phones
rent = "(DEFT RENT)"
investment = "(Spaceship)|(binance)|(Stake)"
subs = "(LINODE)|(Patreon)|(AMZNPRIMEAU)"
internal = "(Internal)|(round up)"
fitness = "(Clublinks)|(Fitness)"


def set_category(description):
    """
    Return a string of a category given a description
    """
    # Salary
    if re.search(income, description):
        return "Income"
    elif re.search(grocery, description):
        return "Groceries"
    elif re.search(transport, description):
        return "Transport"
    elif re.search(shopping, description):
        return "Shopping"
    elif re.search(house, description):
        return "House"
    elif re.search(rent, description):
        return "Rent"
    elif re.search(investment, description):
        return "Investment"
    elif re.search(subs, description):
        return "Subscription"
    elif re.search(internal, description):
        return "Internal"
    elif re.search(fitness, description):
        return "fitness"
    else:
        return "Other"
