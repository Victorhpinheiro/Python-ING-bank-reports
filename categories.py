import re

# define here your list of categories, regex to check and modify the function

categories = [
    "Salary",
    "Groceries",
    "Transport",
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
salary = "Salary"  # Salary
grocery = "(WOOLWORTHS)|(COLES)|(ALDI)|(Cosmos)|(7-ELEVEN)|(FISHME)"
transport = "(OPAL)|(UBER)|(CARSHAREAUS)"
shopping = "(Daiso)|(store)|(AMAZON)|(BIG W)|(MARKETPLACE)|(KMART)|(JB HI-FI)|(EB GAMES)|(TARGET)|(OFFICEWORKS)|(TYPO)"
house = "(VODAFONE)|(AGL)|(CIRCLES)"  # house is internet/ eletricity and phones
rent = "(DEFT RENT)"
investment = "(Spaceship)|(binance)|(Stake)"
subs = "(LINODE)|(Patreon)|(AMZNPRIMEAU)"
internal = "(Internal)"
fitness = "(Clublinks)|(Fitness)"


def set_category(description):
    """
    Return a string of a category given a description
    """
    # Salary
    if re.search(salary, description):
        return "Salary"
    elif re.search(grocery, description):
        return "Groceries"
    elif re.search(transport, description):
        return "Transport"
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


test1 = "SUSHI HUB WORLD TOWE - Visa Purchase - Receipt 169122In SYDNEY Date 10 Aug 2022 Card 462263xxxxxx4173"
test2 = "LANDMARK CAFE - Visa Purchase - Receipt 169121In SILVERWATER Date 10 Aug 2022 Card 462263xxxxxx4173"
test3 = "LANDMARK CAFE - Visa Purchase - Receipt 156339In SILVERWATER Date 09 Aug 2022 Card 462263xxxxxx4173"
test4 = (
    "Internal Transfer - Internal Transfer - Receipt 386526 Orange Everyday 0309078434"
)
test5 = "Everyday round up - Everyday round up - Receipt 297224 OE Card xx4173 Transaction $21.80 Transfer to Savings Maximiser ACC 0811230987"
test6 = "Everyday round up - Everyday round up - Receipt 769605 OE Card xx4173 Transaction $12.00 Transfer to Savings Maximiser ACC 0811230987"
test7 = "eBay O*22-08957-34392 - Visa Purchase - Receipt 186976In Sydney Date 09 Aug 2022 Card 462263xxxxxx8943"
test8 = "LANDMARK CAFE - Visa Purchase - Receipt 186975In SILVERWATER Date 08 Aug 2022 Card 462263xxxxxx4173"

print(set_category(test1))
print(set_category(test2))
print(set_category(test3))
print(set_category(test4))
print(set_category(test5))
print(set_category(test6))
print(set_category(test7))
print(set_category(test8))
