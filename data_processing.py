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
    bank_dataframe = bank_dataframe[~bank_dataframe['Description'].apply(regexSearch_Simmons)] #Exclude simmons statements from transactions
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

    known_transactions_dataframe = categorized_df[categorized_df['Category'] != "Unknown"]
    unknown_transactions_dataframe = categorized_df[categorized_df['Category'] == "Unknown"]

    known_transactions_dictionary = {}
    unknown_transactions_dictionary = {}

    for index, row in known_transactions_dataframe.iterrows():
        description = row['Description']
        amount = row['Amount']
        category = transaction_dict.get(description)

        if category in known_transactions_dictionary:
            known_transactions_dictionary[category] += amount
        else:
            known_transactions_dictionary[category] = amount

    for index, row in unknown_transactions_dataframe.iterrows():
        description = row['Description']
        amount = row['Amount']

        if description in unknown_transactions_dictionary:
            unknown_transactions_dictionary[description] += amount
        else:
            unknown_transactions_dictionary[description] = amount       

    # Sort the known dictionary by value in descending order
    known_transactions_dictionary = {k: v for k, v in sorted(known_transactions_dictionary.items(), key=lambda item: item[1], reverse=True)}

    for category, amount in known_transactions_dictionary.items():
        # Round to 2 decimal places
        known_transactions_dictionary[category] = round(amount, 2)
    
    return known_transactions_dictionary, unknown_transactions_dictionary

def createDataTable():
    bank_dataframe = read_bank_data("bk_download(27).csv")
    categorized_df = categorize_transactions(bank_dataframe)

    known_transactions = categorized_df[categorized_df['Category'] != "Unknown"]

    positive_cash_flow, negative_cash_flow, net_cash_flow, income_to_expense_ratio = calculate_financial_metrics(known_transactions)

    headerDictionary = {
        'positiveCashFlow': positive_cash_flow,
        'negativeCashFlow': negative_cash_flow,
        'netCashFlow': net_cash_flow,
        'income_to_expense_ratio': income_to_expense_ratio
    }

    header_df = pd.DataFrame([headerDictionary])
    header_data = header_df.to_dict('records')
    header_columns = [{"name": col, "id": col} for col in header_df.columns]

    categories_sum = known_transactions.groupby('Category')['Amount'].sum().reset_index()
    categories_sum['Percentage'] = (categories_sum['Amount'] / positive_cash_flow * 100).round(2)

    categories_columns = [{"name": col, "id": col} for col in categories_sum.columns]
    categories_data = categories_sum.to_dict('records')

    return header_columns, header_data, categories_columns, categories_data


def regexSearch_Simmons(description):
    return bool(re.search(r'(?i)simmons?', description))