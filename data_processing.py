#Handles all the data reading and manipulation tasks. Uses Pandas to categorize transactions and calculate financial metrics.
import os
import pandas as pd
from datetime import datetime
from transactionDictionary import transaction_dict

def process_data():
    category_amount_dict = {}
    unknown_transactions = []

    USAA_FILE = "bk_download(25).csv"

    current_month = datetime.now().strftime('%B')
    os.chdir(f"C:\\Users\\Nick\\Documents\\Finances\\Main\\Data\\{current_month}")

    bank_dataframe = pd.read_csv(USAA_FILE)

    for index, row in bank_dataframe.iterrows():
        description = row['Description']
        amount = row['Amount']

        category = transaction_dict.get(description, "Unknown")

        if category is None:
            unknown_transactions.append(description)
            continue

        if category in category_amount_dict:
            category_amount_dict[category] += amount
        else:
            category_amount_dict[category] = amount

    return category_amount_dict, unknown_transactions

