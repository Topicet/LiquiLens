#Handles all the data reading and manipulation tasks. Uses Pandas to categorize transactions and calculate financial metrics.
import os
import pandas as pd
from datetime import datetime
from transactionDictionary import transaction_dict

def process_data():
    # Initialize a dictionary to store category-wise total amounts
    category_amount_dict = {}
    
    # Initialize a list to store descriptions of unknown transactions
    unknown_transactions = []

    # Specify the CSV file containing transaction data
    USAA_FILE = "bk_download(26).csv"

    current_month = datetime.now().strftime('%B')
    os.chdir(f"C:\\Users\\Nick\\Documents\\Finances\\Main\\Data\\{current_month}")


    bank_dataframe = pd.read_csv(USAA_FILE)

    for index, row in bank_dataframe.iterrows():
        description = row['Description']
        amount = row['Amount']

        # Lookup category in the transaction dictionary, default to "Unknown" if not found
        category = transaction_dict.get(description, "Unknown")

        # Check if the category is None (not found)
        if category is None:
            unknown_transactions.append(description)
            continue

        if category in category_amount_dict:
            category_amount_dict[category] += amount
        else:
            category_amount_dict[category] = amount

    return category_amount_dict, unknown_transactions
