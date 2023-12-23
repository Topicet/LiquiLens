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

def createDataTable():
    # Initialize a dictionary to store category-wise total amounts
    category_amount_dict = {}

    positiveCashFlow = 0
    negativeCashFlow = 0

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
            continue

        if category in category_amount_dict:
            category_amount_dict[category] += amount
        else:
            category_amount_dict[category] = amount

        if amount > 0:
            positiveCashFlow += amount
        else:
            negativeCashFlow += amount



    #Dictionary for the panda dataframe
    # Sort the dictionary by value in descending order
    category_amount_dict = {k: v for k, v in sorted(category_amount_dict.items(), key=lambda item: item[1], reverse=True)}

    # Iterate over the dictionary and update each value
    for key in category_amount_dict:
        category_amount_dict[key] /= positiveCashFlow

    income_to_expense_ratio = abs(negativeCashFlow / positiveCashFlow)
    netCashFlow = positiveCashFlow + negativeCashFlow

    
    headerDictionary = {'positiveCashFlow': positiveCashFlow, 'negativeCashFlow': negativeCashFlow, 'netCashFlow': netCashFlow, 'income_to_expense_ratio': income_to_expense_ratio}

    
    # Convert the header dictionary into a DataFrame
    header_df = pd.DataFrame([headerDictionary])
    
    # Convert the category amounts dictionary into a DataFrame
    categories_df = pd.DataFrame(list(category_amount_dict.items()), columns=['Category', 'Amount'])
    categories_df['Percentage'] = categories_df['Amount'] / positiveCashFlow * 100  # Calculate percentage
    
    # Merge both DataFrames into a single one for the DataTable
    # The header_df will have one row, so we can concatenate with categories_df
    final_df = pd.concat([header_df, categories_df], ignore_index=True)

    # DataTable expects a list of dictionaries
    data_for_table = final_df.to_dict('records')
    
    # Define the columns for the DataTable
    columns_for_table = [{"name": col, "id": col} for col in final_df.columns]

    return categories_df, header_df


def regexSearch_Simmons(description):
    pattern = re.compile(r'(?i)simmons?')
    if pattern.search(description):
        return True
    else:
        return False
