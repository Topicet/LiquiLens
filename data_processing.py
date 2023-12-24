#Handles all the data reading and manipulation tasks. Uses Pandas to categorize transactions and calculate financial metrics.
import os
import pandas as pd
import re
from datetime import datetime
from transactionDictionary import transaction_dict


def read_bank_data(file_name):
    file_path = os.path.join(f"C:\\Users\\Nick\\Documents\\Finances\\Main\\Data\\{datetime.now().strftime('%B')}", file_name)
    return pd.read_csv(file_path)

def categorize_transactions(bank_dataframe):
    bank_dataframe = bank_dataframe[~bank_dataframe['Description'].apply(regexSearch_Simmons)]
    bank_dataframe = bank_dataframe[bank_dataframe['Status'] != "Pending"]
    bank_dataframe['Category'] = bank_dataframe['Description'].apply(lambda x: transaction_dict.get(x, "Unknown"))
    return bank_dataframe

def calculate_financial_metrics(bank_dataframe):
    positive_cash_flow = bank_dataframe[bank_dataframe['Amount'] > 0]['Amount'].sum()
    negative_cash_flow = bank_dataframe[bank_dataframe['Amount'] < 0]['Amount'].sum()

    net_cash_flow = positive_cash_flow + negative_cash_flow
    income_to_expense_ratio = abs(negative_cash_flow / positive_cash_flow)

    return positive_cash_flow, negative_cash_flow, net_cash_flow, income_to_expense_ratio

def process_data():
    bank_dataframe = read_bank_data("bk_download(27).csv")
    categorized_df = categorize_transactions(bank_dataframe)

    known_transactions = categorized_df[categorized_df['Category'] != "Unknown"]
    unknown_transactions = categorized_df[categorized_df['Category'] == "Unknown"]

    positive_cash_flow, negative_cash_flow, net_cash_flow, income_to_expense_ratio = calculate_financial_metrics(known_transactions)

    header_dict = {
        'positiveCashFlow': positive_cash_flow,
        'negativeCashFlow': negative_cash_flow,
        'netCashFlow': net_cash_flow,
        'income_to_expense_ratio': income_to_expense_ratio
    }

    header_df = pd.DataFrame([header_dict])

    categories_sum = known_transactions.groupby('Category')['Amount'].sum().reset_index()
    categories_sum['Percentage'] = (categories_sum['Amount'] / positive_cash_flow * 100).round(2)

    return header_df, categories_sum, unknown_transactions.to_dict('records')

def createDataTable():
    return None

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
    header_columns = [{"name": col, "id": col} for col in header_df.columns]
    header_data = header_df.to_dict('records')
    
    # Convert the category amounts dictionary into a DataFrame
    categories_df = pd.DataFrame(list(category_amount_dict.items()), columns=['Category', 'Amount'])
    categories_df['Percentage'] = categories_df['Amount'] / positiveCashFlow * 100  # Calculate percentage

    categories_columns = [{"name": col, "id": col} for col in categories_df.columns]
    categories_data = categories_df.to_dict('records')

    return header_columns, header_data, categories_columns, categories_data



def regexSearch_Simmons(description):
    return re.search(r'(?i)simmons?', description)

