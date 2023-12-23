#Handles all the data reading and manipulation tasks. Uses Pandas to categorize transactions and calculate financial metrics.
import os
import pandas as pd
import re
from datetime import datetime
from transactionDictionary import transaction_dict

def process_data():
    # Initialize a dictionary to store category-wise total amounts
    category_amount_dict = {}
    
    # Initialize a list to store descriptions of unknown transactions
    unknown_transactions = {}

    # Specify the CSV file containing transaction data
    USAA_FILE = "bk_download(27).csv"

    current_month = datetime.now().strftime('%B')
    os.chdir(f"C:\\Users\\Nick\\Documents\\Finances\\Main\\Data\\{current_month}")


    bank_dataframe = pd.read_csv(USAA_FILE)

    for index, row in bank_dataframe.iterrows():
        description = row['Description']
        amount = row['Amount']
        status = row['Status']

        # Skip Simmons Statements
        if regexSearch_Simmons(description):
            continue
        #Skip pending transactions
        if status == "Pending":
            continue

        # Lookup category in the transaction dictionary, default to "Unknown" if not found
        category = transaction_dict.get(description, "Unknown")

        # Check if the category is None (not found)
        if category == "Unknown":
            if description in unknown_transactions:
                unknown_transactions[description] += amount
            else:
                unknown_transactions[description] = amount       
            continue

        if category in category_amount_dict:
            category_amount_dict[category] += amount
        else:
            category_amount_dict[category] = amount

    # Sort the dictionary by value in descending order
    category_amount_dict = {k: v for k, v in sorted(category_amount_dict.items(), key=lambda item: item[1], reverse=True)}

    for category, amount in category_amount_dict.items():
        # Round to 2 decimal places
        category_amount_dict[category] = round(amount, 2)

    
    return category_amount_dict, unknown_transactions


def regexSearch_Simmons(description):
    pattern = re.compile(r'(?i)simmons?')
    if pattern.search(description):
        return True
    else:
        return False
