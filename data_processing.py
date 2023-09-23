#Handles all the data reading and manipulation tasks. Uses Pandas to categorize transactions and calculate financial metrics.
import os
import pandas as pd
from datetime import datetime
from transactionDictionary import transaction_dict

# Initialize the dictionary to store summed amounts for each category
category_amount_dict = {}
unkown_transactions = []  # where transactions values eg "Buckees" or "Sephora", values that are not in my transactionDictionary can be added.


USAA_FILE = "bk_download(25).csv"
#SIMMONS_FILE = "Credit_Card_Statement.csv"

# Grab both excel files
current_month = datetime.now().strftime('%B')
os.chdir(f"C:\\Users\\Nick\\Documents\\Finances\\Main\Data\\{current_month}")


bank_dataframe = pd.read_csv(USAA_FILE)
#credit_card_df = pd.read_excel(SIMMONS_FILE, sheet_name="Your_Sheet_Name_Here")

for index, row in bank_dataframe.iterrows():
    description = row['Description']
    amount = row['Amount']
    
    # Map the description to a category using transaction_dict
    category = transaction_dict.get(description, "Unknown")

    #If this transaction doesn't exist in my transactionDictionary
    if category is None:
        unkown_transactions.append(description)
        continue
    
    # Update the amount for this category in category_amount_dict
    if category in category_amount_dict:
        category_amount_dict[category] += amount
    else:
        category_amount_dict[category] = amount

# Now, category_amount_dict contains summed amounts for each category

print(category_amount_dict)